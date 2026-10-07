# FinDocRAG — grounded QA over annual reports, with a real eval harness

> **Status: work in progress.** Eval results will lead this README once the
> harness has run (see roadmap below).

A small grounded question-answering demo over 3 public annual reports
(Equinor, DNB, Norsk Hydro — 2025), with a 40-question human-verified
evaluation set. Answers are grounded strictly in the source PDFs with inline
citations `[Company, p.X]`; when the answer is not in the documents the system
says **"Not stated in the provided documents."** rather than guessing.

The point of this project is the **evaluation harness**, not the RAG plumbing:
it measures correctness, groundedness, citation validity, and correct
abstention against a human-verified answer key.

## Evaluation results

_To be filled in by `python -m src.evaluate` (Phase 4) — see `eval/report.md`._

## Architecture

```
PDFs → pypdf parse → ~800-token chunks (page metadata) → bge-small embeddings
     → FAISS index → top-k retrieval → Claude (Haiku) grounded answer + citations
```

- **Embeddings:** local `BAAI/bge-small-en-v1.5` (no embedding API)
- **Vector store:** FAISS, persisted to `data/index/`
- **LLM:** Anthropic API, `claude-haiku-4-5` (configurable in `config.py`)
- **UI:** Gradio, two tabs — Ask and Evaluation

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows; source .venv/bin/activate on Unix
pip install -r requirements.txt
cp .env.example .env           # then add your ANTHROPIC_API_KEY
```

Place the three report PDFs in `data/reports/`:
`equinor_2025.pdf`, `dnb_2025.pdf`, `hydro_2025.pdf` (they are not committed
due to size — download from each company's investor-relations site).

## Usage

```bash
python -m src.ingest       # parse, chunk, embed, build FAISS index
python -m src.retrieve "What was Equinor's revenue in 2024?"   # inspect retrieval
python -m src.evaluate     # run the eval set, write eval/report.md
python app.py              # launch the Gradio UI
pytest                     # unit tests
```

## Honest scope

This is a small grounded-QA demo over 3 annual reports with a 40-question
human-verified eval set. It is not a production document-intelligence system:
no table-aware parsing, no reranker, no multi-hop reasoning, single language,
three documents. Abstention is treated as a feature and measured.
