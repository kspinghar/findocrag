"""Top-k retrieval over the persisted FAISS index, with scores.

CLI (inspect chunks):  python -m src.retrieve "your question" [-k 6]
"""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from functools import lru_cache

import faiss
import numpy as np

import config


@dataclass
class RetrievedChunk:
    """A chunk returned by retrieval, with its cosine similarity score."""

    score: float
    company: str
    doc: str
    page: int
    text: str
    chunk_id: int


class Retriever:
    """Loads the persisted FAISS index + chunk metadata and serves queries."""

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

        from sentence_transformers import SentenceTransformer

        self.model = SentenceTransformer(config.EMBEDDING_MODEL)

    def search(self, query: str, top_k: int = config.TOP_K) -> list[RetrievedChunk]:
        """Return the top_k most similar chunks with cosine scores."""
        embedding = self.model.encode(
            [config.BGE_QUERY_PREFIX + query], normalize_embeddings=True
        ).astype(np.float32)
        scores, ids = self.index.search(embedding, top_k)
        results: list[RetrievedChunk] = []
        for score, idx in zip(scores[0], ids[0]):
            if idx < 0:
                continue
            c = self.chunks[idx]
            results.append(
                RetrievedChunk(
                    score=float(score),
                    company=c["company"],
                    doc=c["doc"],
                    page=c["page"],
                    text=c["text"],
                    chunk_id=c["id"],
                )
            )
        return results


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
