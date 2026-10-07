# FinDocRAG evaluation report

- QA set: `qa_candidates.jsonl` — 40 items (30 answerable, 10 unanswerable)
- Answer model: `claude-haiku-4-5` | Judge model: `claude-haiku-4-5`
- Embeddings: `BAAI/bge-small-en-v1.5` | top_k=6 | chunks: 800/100 tokens

## Scorecard

| Metric | Score | Notes |
|---|---|---|
| Correctness (LLM judge, answerable) | 83.3% | 25 full / 0 partial / 5 wrong |
| Groundedness (LLM judge, non-abstained) | 96.3% | share of claims supported by retrieved context |
| Citation validity (programmatic) | 100.0% | 32/32 citations resolve to retrieved (company, page) |
| Figure-in-cited-page rate (programmatic) | 96.3% | answers with figures where a figure appears verbatim in a cited page |
| Abstention recall | 100.0% | unanswerable questions correctly refused |
| Abstention precision | 76.9% | 3 false abstention(s) on answerable questions |

## Failure cases

| # | Type | Question | Issue |
|---|---|---|---|
| 12 | answerable | How many employees did DNB have at the end of 2025? | abstained instead of answering |
| 13 | answerable | What was Hydro's revenue in 2025? | abstained instead of answering |
| 16 | answerable | How much primary aluminium did Hydro produce in 2025? | abstained instead of answering |
| 17 | answerable | How many employees did Hydro have at the end of 2025? | correctness 0: The system answer provides figures (31,618 and 32,000 employees) that do not match the reference answer of 33,400 employees at the end of 2025. Both numbers cited by the system are significantly lower than the correct figure, representing a factual contradiction rather than a partial or correct answer. / unsupported claims: Hydro had 32,000 employees in permanent positions as of the |
| 18 | answerable | What was Equinor's total power generation (Equinor share) in 2025? | unsupported claims: the remainder from other sources |
| 29 | answerable | How much alumina did Hydro produce in 2025? | correctness 0: The system answer states 6.1 million tonnes, which equals 6,100 thousand tonnes. This contradicts the reference answer of 5,458 thousand tonnes. The figure is significantly higher (approximately 12% more) than the correct value, making it factually incorrect. / unsupported claims: Hydro produced 6.1 million tonnes of alumina in 2025 |

## Method notes

- Correctness and groundedness use an LLM judge (`claude-haiku-4-5`, temperature 0, structured JSON output).
- Citation validity and figure support are purely programmatic checks against the chunk page metadata — no model involved.
- Abstention is detected by exact match of the configured abstention string.
- All LLM calls are cached in `eval/.cache/`; delete it to force a fresh run.