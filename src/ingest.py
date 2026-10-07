"""Ingestion pipeline: parse PDFs -> chunk -> embed -> build & persist FAISS index.

Run with:  python -m src.ingest

Chunks are built within page boundaries so every chunk maps to exactly one
page — this keeps citations exact and makes the eval's citation-validity
check programmatic. Pages longer than CHUNK_SIZE_TOKENS are split with a
sliding window of CHUNK_OVERLAP_TOKENS overlap.
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

import faiss
import numpy as np
from pypdf import PdfReader

import config

# Pages with less extracted text than this are retried with pdfplumber,
# then skipped if still empty (covers image-only or decorative pages).
MIN_PAGE_CHARS = 25


@dataclass
class Chunk:
    """One retrievable unit of text, tied to a single page of one report."""

    id: int
    company: str
    doc: str
    page: int  # 1-based page number, as printed by PDF readers
    chunk_idx: int  # position of this chunk within its page
    text: str


def _extract_pages(pdf_path: Path) -> list[tuple[int, str]]:
    """Extract (page_number, text) for every page; pdfplumber as fallback."""
    reader = PdfReader(pdf_path)
    pages: list[tuple[int, str]] = []
    fallback_pages: list[int] = []

    for i, page in enumerate(reader.pages):
        text = (page.extract_text() or "").strip()
        if len(text) < MIN_PAGE_CHARS:
            fallback_pages.append(i)
        pages.append((i + 1, text))

    if fallback_pages:
        import pdfplumber

        with pdfplumber.open(pdf_path) as pdf:
            for i in fallback_pages:
                text = (pdf.pages[i].extract_text() or "").strip()
                if len(text) >= MIN_PAGE_CHARS:
                    pages[i] = (i + 1, text)

    return [(n, t) for n, t in pages if len(t) >= MIN_PAGE_CHARS]


def chunk_text(text: str, tokenizer, chunk_size: int, overlap: int) -> list[str]:
    """Split text into chunks of ~chunk_size tokens with ~overlap token overlap.

    Token boundaries come from the embedding model's tokenizer so chunk sizes
    match what the embedder actually sees. Chunks are sliced from the original
    string via offset mappings (never decoded from token ids), preserving the
    source casing and number formatting exactly.
    """
    encoding = tokenizer(text, add_special_tokens=False, return_offsets_mapping=True)
    offsets: list[tuple[int, int]] = encoding["offset_mapping"]
    if len(offsets) <= chunk_size:
        return [text]

    chunks: list[str] = []
    step = chunk_size - overlap
    start = 0
    while start < len(offsets):
        window = offsets[start : start + chunk_size]
        chunks.append(text[window[0][0] : window[-1][1]])
        if start + chunk_size >= len(offsets):
            break
        start += step
    return chunks


def build_chunks(tokenizer) -> list[Chunk]:
    """Parse every configured report into page-bound chunks."""
    chunks: list[Chunk] = []
    for stem, company in config.COMPANIES.items():
        pdf_path = config.REPORTS_DIR / f"{stem}.pdf"
        if not pdf_path.exists():
            raise FileNotFoundError(f"Missing report: {pdf_path}")
        pages = _extract_pages(pdf_path)
        n_before = len(chunks)
        for page_no, text in pages:
            for idx, piece in enumerate(
                chunk_text(text, tokenizer, config.CHUNK_SIZE_TOKENS, config.CHUNK_OVERLAP_TOKENS)
            ):
                chunks.append(
                    Chunk(
                        id=len(chunks),
                        company=company,
                        doc=stem,
                        page=page_no,
                        chunk_idx=idx,
                        text=piece,
                    )
                )
        print(f"{company}: {len(pages)} pages with text -> {len(chunks) - n_before} chunks")
    return chunks


def main() -> None:
    from sentence_transformers import SentenceTransformer

    print(f"Loading embedding model {config.EMBEDDING_MODEL} ...")
    model = SentenceTransformer(config.EMBEDDING_MODEL)
    tokenizer = model.tokenizer

    print("Parsing and chunking reports ...")
    chunks = build_chunks(tokenizer)
    print(f"Total: {len(chunks)} chunks")

    print("Embedding chunks (normalized, cosine via inner product) ...")
    embeddings = model.encode(
        [c.text for c in chunks],
        batch_size=64,
        show_progress_bar=True,
        normalize_embeddings=True,
    ).astype(np.float32)

    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)

    config.INDEX_DIR.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(config.INDEX_DIR / "index.faiss"))
    with open(config.INDEX_DIR / "chunks.jsonl", "w", encoding="utf-8") as f:
        for c in chunks:
            f.write(json.dumps(asdict(c), ensure_ascii=False) + "\n")

    print(f"Wrote {config.INDEX_DIR / 'index.faiss'} ({index.ntotal} vectors) "
          f"and chunks.jsonl")


if __name__ == "__main__":
    main()
