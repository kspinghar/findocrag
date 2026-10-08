# FinDocRAG evaluation report

- QA set: `qa_set.jsonl`: 39 items (29 answerable, 10 unanswerable)
- Answer model: `claude-haiku-4-5` | Judge model: `claude-haiku-4-5`
- Embeddings: `BAAI/bge-small-en-v1.5` | top_k=6 | chunks: 800/100 tokens

## Scorecard

| Metric | Score | Notes |
|---|---|---|
| Correctness (LLM judge, answerable) | 81.0% | 23 full / 1 partial / 5 wrong |
| Groundedness (LLM judge, answers + abstention explanations) | 97.6% | share of claims supported by retrieved context |
| Citation validity (programmatic) | 100.0% | 44/44 citations resolve to retrieved (company, page) |
| Figure-in-cited-page rate (programmatic) | 97.2% | answers with figures where a figure appears verbatim in a cited page |
| Abstention recall | 100.0% | unanswerable questions correctly refused |
| Abstention precision | 76.9% | 3 false abstention(s) on answerable questions |

## Failure cases

| # | Type | Question | Issue |
|---|---|---|---|
| 12 | answerable | How many employees did DNB have at the end of 2025? | abstained instead of answering |
| 13 | answerable | What was Hydro's revenue in 2025? | abstained instead of answering |
| 16 | answerable | How much primary aluminium did Hydro produce in 2025? | abstained instead of answering |
| 17 | answerable | How many employees did Hydro have at the end of 2025? | correctness 0: The system answer provides 31,618 employees as the year-end 2025 figure, which contradicts the reference answer of 33,400 employees. This is a significant discrepancy of approximately 1,782 employees and represents a factually incorrect answer to the core question asked. |
| 18 | answerable | What was Equinor's total power generation (Equinor share) in 2025? | unsupported claims: the remainder from gas-to-power generation |
| 22 | answerable | How many employees did the Equinor Group have in 2025? | correctness 0.5: The system answer provides 24,140 permanent employees, which matches the reference's permanent employee count. However, the reference states the total employee count is 24,620, while the system answer states 'around 24,600 employees.' This is approximately correct but not precisely matching the reference figure of 24,620. The system answer also includes additional information abou |
| 29 | answerable | How much alumina did Hydro produce in 2025? | correctness 0: The system answer states 6.1 million tonnes of alumina, which contradicts the reference answer of 5,458 thousand tonnes (5.458 million tonnes). The figures do not match - 6.1 million tonnes is significantly higher than the correct figure of 5.458 million tonnes. This is a factual error in the core substance of the question. / unsupported claims: produced 6.1 million tonnes of alumin |

## Method notes

- Correctness and groundedness use an LLM judge (`claude-haiku-4-5`, temperature 0, structured JSON output).
- Citation validity and figure support are purely programmatic checks against the chunk page metadata, with no model involved.
- Abstention is detected when the answer starts with the configured abstention sentence; any explanation after it is judged for groundedness and its citations are checked like any other answer.
- Statements of absence ("X is not stated") are not counted as claims by the groundedness judge.
- All LLM calls are cached in `eval/.cache/`; delete it to force a fresh run.