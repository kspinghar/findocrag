"""Evaluation harness: run the human-verified QA set, compute metrics,
write eval/report.md.

Metrics
-------
1. Correctness        LLM-as-judge: system answer vs reference (0 / 0.5 / 1).
2. Groundedness       LLM-as-judge: fraction of claims in the answer that are
                      supported by the retrieved context.
3. Citation validity  Programmatic: (a) every cited (company, page) must exist
                      in the retrieved chunks shown to the model; (b) for
                      answers containing figures, at least one figure must
                      appear in a cited page's text.
4. Correct abstention Precision / recall of the exact abstention string on
                      unanswerable vs answerable items.

LLM calls are cached on disk (eval/.cache) keyed by content hash, so re-runs
after a crash or config tweak only pay for what changed.

Run with:  python -m src.evaluate            (uses eval/qa_set.jsonl)
           python -m src.evaluate --qa-set eval/qa_candidates.jsonl --allow-unverified
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import config
from src.answer import AnswerResult, answer, get_client

JUDGE_CORRECTNESS_SCHEMA = {
    "type": "object",
    "properties": {
        "score": {"type": "number", "enum": [0, 0.5, 1]},
        "reason": {"type": "string"},
    },
    "required": ["score", "reason"],
    "additionalProperties": False,
}

JUDGE_GROUNDEDNESS_SCHEMA = {
    "type": "object",
    "properties": {
        "total_claims": {"type": "integer"},
        "supported_claims": {"type": "integer"},
        "unsupported": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["total_claims", "supported_claims", "unsupported"],
    "additionalProperties": False,
}

CORRECTNESS_PROMPT = """You are grading a question-answering system on company annual reports.

Question: {question}

Reference answer (ground truth, human-verified):
{reference}

System answer:
{answer}

Score the system answer against the reference:
- 1: factually matches the reference on the substance asked (figures must match; extra correct context is fine; citation markers are ignored)
- 0.5: partially correct (e.g. right direction but missing/imprecise figure, or answers only part of the question)
- 0: wrong figure, contradicts the reference, or fails to answer the substance

Judge only factual agreement with the reference. Formatting, wording and citation brackets do not matter."""

GROUNDEDNESS_PROMPT = """You are auditing whether an answer is grounded in its source context.

Context excerpts that were provided to the answering system:
{context}

Answer to audit:
{answer}

Split the answer into its distinct factual claims (a figure, a date, a named fact each count as one claim; ignore citation brackets like [Company, p.X]). For each claim, decide whether it is directly supported by the context excerpts. Count conservatively: a claim not traceable to the excerpts is unsupported, even if plausible.

Report total_claims, supported_claims, and list each unsupported claim verbatim."""


@dataclass
class ItemResult:
    """Per-item evaluation outcome."""

    item: dict[str, Any]
    result: AnswerResult
    correctness: float | None = None
    correctness_reason: str = ""
    groundedness: float | None = None
    unsupported_claims: list[str] = field(default_factory=list)
    citations_total: int = 0
    citations_resolvable: int = 0
    figure_supported: bool | None = None
    abstain_expected: bool = False
    abstained: bool = False


# --- caching ---------------------------------------------------------------

def _cache_path(kind: str, key: str) -> Path:
    config.EVAL_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    return config.EVAL_CACHE_DIR / f"{kind}-{key}.json"


def _cache_key(*parts: str) -> str:
    return hashlib.sha256("||".join(parts).encode("utf-8")).hexdigest()[:24]


def cached_json_call(kind: str, key: str, fn) -> dict[str, Any]:
    path = _cache_path(kind, key)
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    value = fn()
    path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")
    return value


# --- LLM judge -------------------------------------------------------------

def judge_json(prompt: str, schema: dict[str, Any]) -> dict[str, Any]:
    """One structured-output judge call; response is guaranteed valid JSON."""
    response = get_client().messages.create(
        model=config.JUDGE_MODEL,
        max_tokens=config.MAX_JUDGE_TOKENS,
        temperature=0.0,
        messages=[{"role": "user", "content": prompt}],
        output_config={"format": {"type": "json_schema", "schema": schema}},
    )
    text = next(b.text for b in response.content if b.type == "text")
    return json.loads(text)


# --- metric helpers --------------------------------------------------------

NUMBER_RE = re.compile(r"\d[\d,.\s]*\d|\d")


def _norm_ws(s: str) -> str:
    return re.sub(r"\s+", " ", s.replace(" ", " "))


def _answer_figures(text: str) -> list[str]:
    """Numeric strings in the answer body (citation brackets stripped)."""
    body = re.sub(r"\[[^\]]*\]", " ", text)
    figures = []
    for m in NUMBER_RE.finditer(body):
        fig = m.group().strip(" .,")
        if len(fig.replace(",", "").replace(" ", "")) >= 2:  # skip bare single digits
            figures.append(fig)
    return figures


def check_citations(res: AnswerResult) -> tuple[int, int, bool | None]:
    """Programmatic citation validity.

    Returns (total citations, resolvable citations, figure_supported):
    - resolvable: the cited (company, page) pair is among the retrieved chunks
      the model actually saw.
    - figure_supported: True if at least one numeric figure from the answer
      appears verbatim in the text of a cited page (None if the answer has no
      figures or no citations).
    """
    retrieved = {(c.company, c.page): _norm_ws(c.text) for c in res.chunks}
    total = len(res.citations)
    resolvable = sum(1 for c in res.citations if (c.company, c.page) in retrieved)

    figures = _answer_figures(res.answer)
    if not figures or total == 0:
        return total, resolvable, None
    cited_text = " ".join(
        retrieved.get((c.company, c.page), "") for c in res.citations
    )
    supported = any(_norm_ws(f) in cited_text for f in figures)
    return total, resolvable, supported


# --- main loop -------------------------------------------------------------

def load_qa_set(path: Path, allow_unverified: bool) -> list[dict[str, Any]]:
    items = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    unverified = [i["id"] for i in items if not i.get("verified")]
    if unverified and not allow_unverified:
        raise SystemExit(
            f"Refusing to evaluate: {len(unverified)} items are not human-verified "
            f"(ids {unverified[:10]}...). Use --allow-unverified for a dry run."
        )
    return items


def evaluate_item(item: dict[str, Any]) -> ItemResult:
    question = item["question"]
    key = _cache_key(config.ANSWER_MODEL, str(config.TOP_K), question)

    def _run() -> dict[str, Any]:
        r = answer(question)
        return {
            "answer": r.answer,
            "abstained": r.abstained,
            "citations": [{"company": c.company, "page": c.page} for c in r.citations],
            "chunks": [
                {"score": c.score, "company": c.company, "doc": c.doc,
                 "page": c.page, "text": c.text, "id": c.chunk_id}
                for c in r.chunks
            ],
        }

    raw = cached_json_call("answer", key, _run)
    from src.answer import Citation
    from src.retrieve import RetrievedChunk

    # Recompute abstention from the answer text (prefix match) rather than
    # trusting the cached flag, so detection fixes apply to cached runs too.
    raw["abstained"] = raw["answer"].strip().startswith(config.ABSTAIN_STRING)
    res = AnswerResult(
        question=question,
        answer=raw["answer"],
        citations=[Citation(**c) for c in raw["citations"]],
        chunks=[RetrievedChunk(score=c["score"], company=c["company"], doc=c["doc"],
                               page=c["page"], text=c["text"], chunk_id=c["id"])
                for c in raw["chunks"]],
        abstained=raw["abstained"],
    )

    out = ItemResult(item=item, result=res,
                     abstain_expected=item["type"] == "unanswerable",
                     abstained=res.abstained)

    if item["type"] == "answerable" and not res.abstained:
        cj = cached_json_call(
            "correctness",
            _cache_key(config.JUDGE_MODEL, question, item["reference_answer"], res.answer),
            lambda: judge_json(
                CORRECTNESS_PROMPT.format(question=question,
                                          reference=item["reference_answer"],
                                          answer=res.answer),
                JUDGE_CORRECTNESS_SCHEMA,
            ),
        )
        out.correctness = float(cj["score"])
        out.correctness_reason = cj["reason"]
    elif item["type"] == "answerable" and res.abstained:
        out.correctness = 0.0
        out.correctness_reason = "System abstained on an answerable question."

    if not res.abstained:
        context = "\n\n".join(
            f"[{c.company}, p.{c.page}] {c.text}" for c in res.chunks
        )
        gj = cached_json_call(
            "groundedness",
            _cache_key(config.JUDGE_MODEL, res.answer, str(len(res.chunks))),
            lambda: judge_json(
                GROUNDEDNESS_PROMPT.format(context=context, answer=res.answer),
                JUDGE_GROUNDEDNESS_SCHEMA,
            ),
        )
        total = max(gj["total_claims"], 1)
        out.groundedness = min(gj["supported_claims"], total) / total
        out.unsupported_claims = gj["unsupported"]
        out.citations_total, out.citations_resolvable, out.figure_supported = check_citations(res)

    return out


def compute_summary(results: list[ItemResult]) -> dict[str, Any]:
    answerable = [r for r in results if r.item["type"] == "answerable"]
    unanswerable = [r for r in results if r.item["type"] == "unanswerable"]

    correctness = [r.correctness for r in answerable if r.correctness is not None]
    groundedness = [r.groundedness for r in results if r.groundedness is not None]

    cit_total = sum(r.citations_total for r in results)
    cit_ok = sum(r.citations_resolvable for r in results)
    fig_checked = [r for r in results if r.figure_supported is not None]
    fig_ok = sum(1 for r in fig_checked if r.figure_supported)

    true_abstain = sum(1 for r in unanswerable if r.abstained)
    false_abstain = sum(1 for r in answerable if r.abstained)
    all_abstain = true_abstain + false_abstain

    return {
        "n_items": len(results),
        "n_answerable": len(answerable),
        "n_unanswerable": len(unanswerable),
        "correctness_mean": sum(correctness) / len(correctness) if correctness else None,
        "correctness_full": sum(1 for c in correctness if c == 1.0),
        "correctness_partial": sum(1 for c in correctness if c == 0.5),
        "correctness_zero": sum(1 for c in correctness if c == 0.0),
        "groundedness_mean": sum(groundedness) / len(groundedness) if groundedness else None,
        "citations_total": cit_total,
        "citations_resolvable": cit_ok,
        "citation_validity": cit_ok / cit_total if cit_total else None,
        "figure_support_rate": fig_ok / len(fig_checked) if fig_checked else None,
        "abstention_recall": true_abstain / len(unanswerable) if unanswerable else None,
        "abstention_precision": true_abstain / all_abstain if all_abstain else None,
        "false_abstentions": false_abstain,
    }


def _fmt(x: float | None, pct: bool = True) -> str:
    if x is None:
        return "n/a"
    return f"{x:.1%}" if pct else f"{x:.3f}"


def write_report(results: list[ItemResult], summary: dict[str, Any], qa_path: Path) -> None:
    lines: list[str] = []
    lines.append("# FinDocRAG evaluation report\n")
    lines.append(f"- QA set: `{qa_path.name}` — {summary['n_items']} items "
                 f"({summary['n_answerable']} answerable, {summary['n_unanswerable']} unanswerable)")
    lines.append(f"- Answer model: `{config.ANSWER_MODEL}` | Judge model: `{config.JUDGE_MODEL}`")
    lines.append(f"- Embeddings: `{config.EMBEDDING_MODEL}` | top_k={config.TOP_K} | "
                 f"chunks: {config.CHUNK_SIZE_TOKENS}/{config.CHUNK_OVERLAP_TOKENS} tokens\n")

    lines.append("## Scorecard\n")
    lines.append("| Metric | Score | Notes |")
    lines.append("|---|---|---|")
    lines.append(f"| Correctness (LLM judge, answerable) | {_fmt(summary['correctness_mean'])} | "
                 f"{summary['correctness_full']} full / {summary['correctness_partial']} partial / "
                 f"{summary['correctness_zero']} wrong |")
    lines.append(f"| Groundedness (LLM judge, non-abstained) | {_fmt(summary['groundedness_mean'])} | "
                 f"share of claims supported by retrieved context |")
    lines.append(f"| Citation validity (programmatic) | {_fmt(summary['citation_validity'])} | "
                 f"{summary['citations_resolvable']}/{summary['citations_total']} citations resolve "
                 f"to retrieved (company, page) |")
    lines.append(f"| Figure-in-cited-page rate (programmatic) | {_fmt(summary['figure_support_rate'])} | "
                 f"answers with figures where a figure appears verbatim in a cited page |")
    lines.append(f"| Abstention recall | {_fmt(summary['abstention_recall'])} | "
                 f"unanswerable questions correctly refused |")
    lines.append(f"| Abstention precision | {_fmt(summary['abstention_precision'])} | "
                 f"{summary['false_abstentions']} false abstention(s) on answerable questions |\n")

    failures = [
        r for r in results
        if (r.correctness is not None and r.correctness < 1.0)
        or (r.groundedness is not None and r.groundedness < 1.0)
        or (r.abstain_expected and not r.abstained)
        or (not r.abstain_expected and r.abstained)
    ]
    lines.append("## Failure cases\n")
    if not failures:
        lines.append("None — every item scored full marks on every metric.\n")
    else:
        lines.append("| # | Type | Question | Issue |")
        lines.append("|---|---|---|---|")
        for r in failures:
            issues = []
            if r.abstain_expected and not r.abstained:
                issues.append("answered instead of abstaining")
            if not r.abstain_expected and r.abstained:
                issues.append("abstained instead of answering")
            if r.correctness is not None and r.correctness < 1.0 and not r.abstained:
                issues.append(f"correctness {r.correctness:g}: {r.correctness_reason}")
            if r.groundedness is not None and r.groundedness < 1.0:
                issues.append(f"unsupported claims: {'; '.join(r.unsupported_claims[:3])}")
            q = r.item["question"]
            issue_text = " | ".join(issues).replace("|", "/")[:400]
            lines.append(f"| {r.item['id']} | {r.item['type']} | {q} | {issue_text} |")
        lines.append("")

    lines.append("## Method notes\n")
    lines.append("- Correctness and groundedness use an LLM judge "
                 f"(`{config.JUDGE_MODEL}`, temperature 0, structured JSON output).")
    lines.append("- Citation validity and figure support are purely programmatic checks "
                 "against the chunk page metadata — no model involved.")
    lines.append("- Abstention is detected by exact match of the configured abstention string.")
    lines.append("- All LLM calls are cached in `eval/.cache/`; delete it to force a fresh run.")

    config.EVAL_REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the FinDocRAG evaluation harness.")
    parser.add_argument("--qa-set", type=Path, default=config.QA_SET_PATH)
    parser.add_argument("--allow-unverified", action="store_true",
                        help="Evaluate items not yet human-verified (dry runs only).")
    args = parser.parse_args()

    items = load_qa_set(args.qa_set, allow_unverified=args.allow_unverified)
    print(f"Evaluating {len(items)} items from {args.qa_set} ...")

    results: list[ItemResult] = []
    for i, item in enumerate(items, 1):
        r = evaluate_item(item)
        results.append(r)
        tag = "ABSTAIN" if r.abstained else f"corr={r.correctness if r.correctness is not None else '-'}"
        print(f"  [{i:2d}/{len(items)}] id={item['id']:2d} {item['type']:12s} {tag}")

    summary = compute_summary(results)
    write_report(results, summary, args.qa_set)

    print("\n--- Summary ---")
    for k, v in summary.items():
        print(f"  {k}: {v}")
    print(f"\nReport written to {config.EVAL_REPORT_PATH}")


if __name__ == "__main__":
    main()
