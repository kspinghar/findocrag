"""Retrieval over the persisted index: dense, BM25 keyword, or hybrid, with an
optional LLM rerank of the hybrid candidates.

Why hybrid: the baseline used dense (embedding) search only. Its failures were
almost all table pages (income statement, headcount table, production table),
which embed poorly because they are mostly numbers, yet contain the exact words
of the question ("Revenue", "employees", "alumina production"). BM25 keyword
search finds those pages; the two rankings are merged with reciprocal rank
fusion (RRF), and a cheap LLM rerank then picks the most useful chunks from the
merged candidates.

CLI (inspect chunks):  python -m src.retrieve "your question" [-k 8]
"""
from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from functools import lru_cache

import faiss
import numpy as np

import config


@dataclass
class RetrievedChunk:
    """A chunk returned by retrieval. `score` is cosine similarity for dense
    search and the fused RRF score for hybrid search."""

    score: float
    company: str
    doc: str
    page: int
    text: str
    chunk_id: int


_STOPWORDS = set(
    "the a an of in on for to and or what was were did does how many much is are "
    "at by with from its it as be this that which who".split()
)


def tokenize(text: str) -> list[str]:
    """Lowercase alphanumeric tokens without stopwords, for BM25."""
    return [w for w in re.findall(r"[a-z0-9]+", text.lower()) if w not in _STOPWORDS]


def company_in_query(query: str) -> str | None:
    """The single company named in the query, if exactly one is named."""
    named = [name for name in config.COMPANIES.values() if name.lower() in query.lower()]
    return named[0] if len(named) == 1 else None


RERANK_PROMPT = """You select the document excerpts needed to answer a question about company annual reports.

Question: {question}

Excerpts:
{excerpts}

Return the numbers of the excerpts most likely to contain the specific facts or figures needed to answer the question, most useful first, at most {k}. Prefer excerpts that contain the actual figure (tables, key-figure pages, financial statements) over excerpts that only discuss the topic. If none are relevant, return the {k} closest."""

RERANK_SCHEMA = {
    "type": "object",
    "properties": {"ids": {"type": "array", "items": {"type": "integer"}}},
    "required": ["ids"],
    "additionalProperties": False,
}


class Retriever:
    """Loads the persisted FAISS index, chunk metadata and a BM25 index."""

    def __init__(self) -> None:
        index_path = config.INDEX_DIR / "index.faiss"
        chunks_path = config.INDEX_DIR / "chunks.jsonl"
        if not index_path.exists() or not chunks_path.exists():
            raise FileNotFoundError(
                "Index not found — run `python -m src.ingest` first."
            )
        self.index = faiss.read_index(str(index_path))
        with open(chunks_path, encoding="utf-8") as f:
            self.chunks: list[dict] = [json.loads(line) for line in f]
        self.companies = np.array([c["company"] for c in self.chunks])

        from rank_bm25 import BM25Okapi
        from sentence_transformers import SentenceTransformer

        self.bm25 = BM25Okapi([tokenize(c["text"]) for c in self.chunks])
        self.model = SentenceTransformer(config.EMBEDDING_MODEL)

    # --- rankings -------------------------------------------------------------
    def _mask(self, query: str) -> np.ndarray:
        company = company_in_query(query) if config.FILTER_BY_COMPANY else None
        if company is None:
            return np.ones(len(self.chunks), dtype=bool)
        return self.companies == company

    def _dense_ranking(self, query: str, mask: np.ndarray) -> list[tuple[int, float]]:
        embedding = self.model.encode(
            [config.BGE_QUERY_PREFIX + query], normalize_embeddings=True
        ).astype(np.float32)
        scores, ids = self.index.search(embedding, len(self.chunks))
        return [(int(i), float(s)) for s, i in zip(scores[0], ids[0]) if i >= 0 and mask[i]]

    def _bm25_ranking(self, query: str, mask: np.ndarray) -> list[tuple[int, float]]:
        scores = self.bm25.get_scores(tokenize(query))
        order = np.argsort(-scores)
        return [(int(i), float(scores[i])) for i in order if mask[i]]

    def _hybrid_ranking(self, query: str, mask: np.ndarray, depth: int = 100) -> list[tuple[int, float]]:
        fused: dict[int, float] = {}
        for ranking in (self._dense_ranking(query, mask), self._bm25_ranking(query, mask)):
            for rank, (i, _) in enumerate(ranking[:depth]):
                fused[i] = fused.get(i, 0.0) + 1.0 / (config.RRF_K + rank)
        return sorted(fused.items(), key=lambda x: -x[1])

    def _rerank(self, query: str, candidates: list[tuple[int, float]], top_k: int) -> list[tuple[int, float]]:
        from src.answer import get_client

        excerpts = "\n\n".join(
            f"[{n}] ({self.chunks[i]['company']}, p.{self.chunks[i]['page']})\n{self.chunks[i]['text']}"
            for n, (i, _) in enumerate(candidates, 1)
        )
        response = get_client().messages.create(
            model=config.RERANK_MODEL,
            max_tokens=256,
            temperature=0.0,
            messages=[{"role": "user", "content": RERANK_PROMPT.format(
                question=query, excerpts=excerpts, k=top_k)}],
            output_config={"format": {"type": "json_schema", "schema": RERANK_SCHEMA}},
        )
        text = next(b.text for b in response.content if b.type == "text")
        picked: list[tuple[int, float]] = []
        for n in json.loads(text)["ids"]:
            if 1 <= n <= len(candidates) and candidates[n - 1] not in picked:
                picked.append(candidates[n - 1])
        # Fill up from the fused order if the reranker returned fewer than top_k.
        for cand in candidates:
            if len(picked) >= top_k:
                break
            if cand not in picked:
                picked.append(cand)
        return picked[:top_k]

    # --- public ------------------------------------------------------------------
    def search(self, query: str, top_k: int = config.TOP_K) -> list[RetrievedChunk]:
        """Return the top_k chunks for the query using config.RETRIEVAL_MODE."""
        mask = self._mask(query)
        if config.RETRIEVAL_MODE == "dense":
            ranked = self._dense_ranking(query, mask)[:top_k]
        elif config.RETRIEVAL_MODE == "bm25":
            ranked = self._bm25_ranking(query, mask)[:top_k]
        else:
            ranked = self._hybrid_ranking(query, mask)
            if config.RERANK:
                ranked = self._rerank(query, ranked[: config.RERANK_CANDIDATES], top_k)
            else:
                ranked = ranked[:top_k]

        return [
            RetrievedChunk(
                score=score,
                company=self.chunks[i]["company"],
                doc=self.chunks[i]["doc"],
                page=self.chunks[i]["page"],
                text=self.chunks[i]["text"],
                chunk_id=self.chunks[i]["id"],
            )
            for i, score in ranked
        ]


@lru_cache(maxsize=1)
def get_retriever() -> Retriever:
    """Shared singleton so the app/eval load the index and model once."""
    return Retriever()


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect top-k retrieval results.")
    parser.add_argument("query", help="Natural-language question")
    parser.add_argument("-k", type=int, default=config.TOP_K, help="Number of chunks")
    args = parser.parse_args()

    for i, r in enumerate(get_retriever().search(args.query, top_k=args.k), 1):
        preview = " ".join(r.text.split())[:300]
        print(f"#{i}  score={r.score:.3f}  [{r.company}, p.{r.page}]")
        print(f"    {preview}")
        print()


if __name__ == "__main__":
    main()
