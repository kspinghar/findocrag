# FinDocRAG evaluation report

- QA set: `qa_set.jsonl` — 39 items (29 answerable, 10 unanswerable)
- Answer model: `claude-haiku-4-5` | Judge model: `claude-haiku-4-5`
- Retrieval: `hybrid`, company filter, LLM rerank of top 30 candidates (`claude-haiku-4-5`)
- Embeddings: `BAAI/bge-small-en-v1.5` | top_k=8 | chunks: 800/100 tokens

## Scorecard

| Metric | Score | Notes |
|---|---|---|
| Retrieval hit rate (programmatic, answerable) | 100.0% | 29/29 questions where a verified source page was among the retrieved chunks |
| Correctness (LLM judge, answerable) | 100.0% | 29 full / 0 partial / 0 wrong |
| Groundedness (LLM judge, answers + abstention explanations) | 96.6% | share of claims supported by retrieved context |
| Citation validity (programmatic) | 100.0% | 48/48 citations resolve to retrieved (company, page) |
| Figure-in-cited-page rate (programmatic) | 100.0% | answers with figures where a figure appears verbatim in a cited page |
| Abstention recall | 100.0% | unanswerable questions correctly refused |
| Abstention precision | 100.0% | 0 false abstention(s) on answerable questions |

## Failure cases

| # | Type | Question | Issue |
|---|---|---|---|
| 18 | answerable | What was Equinor's total power generation (Equinor share) in 2025? | unsupported claims: the remainder from gas-to-power generation |
| 29 | answerable | How much alumina did Hydro produce in 2025? | unsupported claims: This can also be expressed as 6.1 million tonnes as stated in the business area summary |
| 31 | unanswerable | What profit guidance has DNB issued for 2027? | unsupported claims: no forward-looking profit guidance for 2027 |
| 34 | unanswerable | How many employees did Equinor have in China at the end of 2025? | unsupported claims: China is only mentioned as a location where Equinor has "M&T" (Marketing & Trading) "partnerships and presence" activities |
| 36 | unanswerable | What dividend per share did Equinor pay for fiscal year 2015? | unsupported claims: Equinor paid USD 3.00 per share (or USD 1.81 per share on a different measurement basis) in 2024 |

## Method notes

- Correctness and groundedness use an LLM judge (`claude-haiku-4-5`, temperature 0, structured JSON output).
- Citation validity and figure support are purely programmatic checks against the chunk page metadata — no model involved.
- Abstention is detected when the answer starts with the configured abstention sentence; any explanation after it is judged for groundedness and its citations are checked like any other answer.
- Statements of absence ("X is not stated") are not counted as claims by the groundedness judge.
- All LLM calls are cached in `eval/.cache/`; delete it to force a fresh run.