# FinDocRAG evaluation report

- QA set: `heldout_set.jsonl` — 20 items (15 answerable, 5 unanswerable)
- Answer model: `claude-haiku-4-5` | Judge model: `claude-haiku-4-5`
- Retrieval: `hybrid`, company filter, LLM rerank of top 30 candidates (`claude-haiku-4-5`)
- Embeddings: `BAAI/bge-small-en-v1.5` | top_k=8 | chunks: 800/100 tokens

## Scorecard

| Metric | Score | Notes |
|---|---|---|
| Retrieval hit rate (programmatic, answerable) | 100.0% | 15/15 questions where a verified source page was among the retrieved chunks |
| Correctness (LLM judge, answerable) | 93.3% | 14 full / 0 partial / 1 wrong |
| Groundedness (LLM judge, answers + abstention explanations) | 99.1% | share of claims supported by retrieved context |
| Citation validity (programmatic) | 100.0% | 24/24 citations resolve to retrieved (company, page) |
| Figure-in-cited-page rate (programmatic) | 95.0% | answers with figures where a figure appears verbatim in a cited page |
| Abstention recall | 100.0% | unanswerable questions correctly refused |
| Abstention precision | 83.3% | 1 false abstention(s) on answerable questions |

## Failure cases

| # | Type | Question | Issue |
|---|---|---|---|
| 111 | answerable | What dividend per share did DNB pay for 2018? | abstained instead of answering / unsupported claims: dividend paid for 2018 |

## Method notes

- Correctness and groundedness use an LLM judge (`claude-haiku-4-5`, temperature 0, structured JSON output).
- Citation validity and figure support are purely programmatic checks against the chunk page metadata — no model involved.
- Abstention is detected when the answer starts with the configured abstention sentence; any explanation after it is judged for groundedness and its citations are checked like any other answer.
- Statements of absence ("X is not stated") are not counted as claims by the groundedness judge.
- All LLM calls are cached in `eval/.cache/`; delete it to force a fresh run.