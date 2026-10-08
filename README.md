# FinDocRAG: grounded Q&A over annual reports, with an honest evaluation

FinDocRAG answers questions about the 2025 annual reports of **Equinor, DNB and Norsk Hydro** (977 pages in total).
Every answer cites the report page it comes from, written as `[Company, p.X]`. When the reports do not contain the
answer, the system says **"Not stated in the provided documents."** and then explains, with citations, what related
information the reports do contain (for example an average instead of a closing price, or a different year).

The point of the project is the **evaluation**, not the retrieval plumbing. Every score below comes from a real run of
`python -m src.evaluate` against an answer key that was verified by hand against the source pages.

## Results

| Metric | Held-out set (20 unseen questions) | Development set (39 questions) | Development baseline |
|---|---|---|---|
| Retrieval hit rate (verified page retrieved) | **100%** (15/15) | 100% (29/29) | not measured (metric added later) |
| Correctness (LLM judge) | **93.3%** (14/15) | 100% (29/29) | 81.0% |
| Groundedness (LLM judge) | **99.1%** | 96.6% | 97.6% |
| Citation validity (programmatic) | **100%** (24/24) | 100% (48/48) | 100% (44/44) |
| Figure appears on cited page (programmatic) | **95.0%** | 100% | 97.2% |
| Abstention recall (unanswerable questions refused) | **100%** (5/5) | 100% (10/10) | 100% |
| Abstention precision (refusals that were right) | **83.3%** | 100% | 76.9% |

**Read the held-out column first.** The development set was used to find failures and choose fixes, so its after-score
is optimistic. The held-out set was written and verified after all changes and run **once** with the system frozen.
Full reports: [`eval/report_heldout.md`](eval/report_heldout.md), [`eval/report.md`](eval/report.md),
[`eval/report_baseline.md`](eval/report_baseline.md).

## How the evaluation works

**Answer key.** 40 draft questions were checked one by one against highlighted crops of the report pages. One was
dropped and four were corrected, giving 39 items (29 answerable, 10 that must be refused). After the baseline run, one
reference answer (Q29, Hydro alumina production) was widened because the report states the figure on two different
bases on two pages. Every decision is recorded in [`eval/VERDICTS.md`](eval/VERDICTS.md).

**Held-out set.** 20 further questions (15 answerable, 5 unanswerable, several of them deliberate traps such as a
country revenue row that looks like a headcount) were written after the improvement round, verified the same way, and
run a single time.

**Metrics.**
- *Correctness*: an LLM judge (`claude-haiku-4-5`, temperature 0, JSON schema output) scores each answer against the
  reference as 1, 0.5 or 0.
- *Groundedness*: the judge splits the answer into factual claims and checks each against the retrieved passages.
  Abstention explanations are judged too, so an invented explanation is penalised like an invented answer. Statements
  of absence ("X is not stated") are not counted as claims.
- *Citation validity*: every `[Company, p.X]` must point to a page that was actually retrieved. No model involved.
- *Figure on cited page*: at least one figure in the answer must appear verbatim on a cited page. No model involved.
- *Retrieval hit rate*: a verified source page must be among the retrieved passages. No model involved.
- *Abstention recall and precision*: whether the system refuses exactly the questions it should.

All model calls are cached under `eval/.cache/`, keyed on the model, the prompts and the retrieval settings, so a
changed prompt can never reuse a stale result.

## What changed between baseline and final

The baseline used embedding search only (top 6 passages). Triage showed that 5 of the 6 answerable failures were
**retrieval** misses: the right page was never retrieved. Those pages were tables (an income statement, headcount and
production tables), which embed poorly because they are mostly numbers, yet contain the exact words of the question.
One improvement round, measured before and after:

1. **Hybrid search**: BM25 keyword ranking fused with the embedding ranking (reciprocal rank fusion).
2. **Company filter**: when a question names exactly one company, only that report is searched.
3. **LLM rerank**: `claude-haiku-4-5` picks the 8 most useful passages from the top 30 fused candidates.

No further tuning was done against either question set.

## Architecture

```
PDFs ─ pypdf parse ─ 800-token chunks with page metadata (1,377 chunks)
                         ├─ bge-small-en-v1.5 embeddings ─ FAISS
                         └─ BM25 keyword index
question ─ company filter ─ dense + BM25 rankings ─ RRF fusion ─ top 30
         ─ LLM rerank ─ top 8 passages ─ Claude answer with [Company, p.X] citations
                                        (or abstain + cited explanation)
```

- Embeddings: local `BAAI/bge-small-en-v1.5` (no embedding API)
- Vector store: FAISS; keyword search: `rank-bm25`
- Answer, rerank and judge model: `claude-haiku-4-5` via the Anthropic API (set in `config.py`)
- UI: Gradio, with an **Ask** tab and an **Evaluation** tab

## Known limitations

- **Charts.** Values that exist only in a chart lose the link between year and value when the PDF is converted to text.
  This caused the one held-out failure (DNB's 2018 dividend): the right page was retrieved, and the system abstained
  rather than guess.
- **Lenient judge.** On one development question the judge accepted an answer that wrongly treated two production
  figures on different bases as the same number. Groundedness caught it (0.67); correctness did not.
- **Small scale.** Three reports, one language, 59 verified questions. No table-aware parsing, no multi-hop reasoning.
  This is a demonstration of grounded answering and honest measurement, not a production document system.

## Run it

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows; source .venv/bin/activate on macOS/Linux
pip install -r requirements.txt
cp .env.example .env             # then add your ANTHROPIC_API_KEY
python app.py                    # Gradio UI at http://127.0.0.1:7860
```

The prebuilt index (`data/index/`) is included, so the app and the evaluation run without the source PDFs.

```bash
python -m src.retrieve "What was Hydro's revenue in 2025?"     # inspect retrieval
python -m src.answer "What was DNB's return on equity in 2025?"  # one answer
python -m src.evaluate                                           # development set -> eval/report.md
python -m src.evaluate --qa-set eval/heldout_set.jsonl --report eval/report_heldout.md
pytest                                                           # unit tests
```

To rebuild the index from scratch, download the three 2025 annual reports from each company's investor relations site,
save them as `data/reports/equinor_2025.pdf`, `dnb_2025.pdf` and `hydro_2025.pdf`, and run `python -m src.ingest`.

## Repository layout

```
app.py                  Gradio UI
config.py               all settings (models, retrieval mode, top_k, paths)
src/ingest.py           PDF parsing, chunking, embedding, FAISS index
src/retrieve.py         dense, BM25 and hybrid retrieval, company filter, LLM rerank
src/answer.py           grounded answering, citation parsing, abstention
src/evaluate.py         the evaluation harness and report writer
eval/qa_set.jsonl       development answer key (39 verified items)
eval/heldout_set.jsonl  held-out answer key (20 verified items)
eval/VERDICTS.md        how every item was verified or corrected
eval/report*.md         baseline, development and held-out reports
data/index/             prebuilt chunks and FAISS index
tests/                  unit tests for chunking and citation parsing
```

## Author

Khalid Spinghar, MSc Artificial Intelligence student at Kristiania University of Applied Sciences, Oslo.
[GitHub](https://github.com/kspinghar) | [Hugging Face](https://huggingface.co/kalspi)
