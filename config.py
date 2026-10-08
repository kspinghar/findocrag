"""Central configuration for FinDocRAG.

Everything tunable lives here. Paths are resolved relative to the repo root
so the app works both locally and on Hugging Face Spaces.
"""
from __future__ import annotations

from pathlib import Path

# --- Paths ---------------------------------------------------------------
ROOT_DIR = Path(__file__).parent
DATA_DIR = ROOT_DIR / "data"
REPORTS_DIR = DATA_DIR / "reports"
INDEX_DIR = DATA_DIR / "index"
EVAL_DIR = ROOT_DIR / "eval"
QA_SET_PATH = EVAL_DIR / "qa_set.jsonl"
EVAL_REPORT_PATH = EVAL_DIR / "report.md"
EVAL_CACHE_DIR = EVAL_DIR / ".cache"

# --- Documents -----------------------------------------------------------
# filename stem -> display name used in citations
COMPANIES: dict[str, str] = {
    "equinor_2025": "Equinor",
    "dnb_2025": "DNB",
    "hydro_2025": "Hydro",
}

# --- Chunking ------------------------------------------------------------
CHUNK_SIZE_TOKENS = 800
CHUNK_OVERLAP_TOKENS = 100

# --- Embeddings / retrieval ----------------------------------------------
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"
# bge models recommend a query instruction prefix for retrieval
BGE_QUERY_PREFIX = "Represent this sentence for searching relevant passages: "
TOP_K = 8

# Retrieval strategy. Baseline (8 Oct 2026) was "dense", TOP_K=6, no rerank.
# "hybrid" merges dense and BM25 keyword rankings with reciprocal rank fusion.
RETRIEVAL_MODE = "hybrid"  # "dense" | "bm25" | "hybrid"
RRF_K = 60  # standard RRF constant
FILTER_BY_COMPANY = True  # if the question names exactly one company, search only its report
RERANK = True  # LLM picks the TOP_K most useful chunks from the hybrid candidates
RERANK_CANDIDATES = 30

# --- LLM -----------------------------------------------------------------
# Cheapest current Haiku-class model ($1/$5 per MTok). Change here to swap.
ANSWER_MODEL = "claude-haiku-4-5"
JUDGE_MODEL = "claude-haiku-4-5"
RERANK_MODEL = "claude-haiku-4-5"
MAX_ANSWER_TOKENS = 1024
MAX_JUDGE_TOKENS = 512

# Exact abstention string the answerer must emit when unsupported.
ABSTAIN_STRING = "Not stated in the provided documents."
