"""Gradio UI for FinDocRAG: "Ask" and "Evaluation" tabs.

Run locally with:  python app.py
"""
from __future__ import annotations

import datetime as _dt
import html
import logging
import os
import re
import threading
from pathlib import Path

import gradio as gr

import config

# Hosting note. The public demo runs on Hugging Face ZeroGPU hardware, the free option
# for Gradio Spaces. ZeroGPU refuses to start an app that has no @spaces.GPU function.
# This app only uses the CPU, so the placeholder below is never called and uses no GPU
# time. Locally the `spaces` package is not installed.
try:
    import spaces
except ImportError:
    spaces = None

if spaces is not None:

    @spaces.GPU
    def _zerogpu_placeholder() -> None:
        return None


GITHUB_URL = "https://github.com/kspinghar/findocrag"
MAX_QUESTION_CHARS = 400
# Every question costs two API calls (rerank + answer), so the public demo has a daily cap.
MAX_QUESTIONS_PER_DAY = int(os.environ.get("MAX_QUESTIONS_PER_DAY", "300"))
_usage = {"day": None, "count": 0}
_usage_lock = threading.Lock()


def _take_quota() -> bool:
    today = _dt.date.today()
    with _usage_lock:
        if _usage["day"] != today:
            _usage["day"], _usage["count"] = today, 0
        if _usage["count"] >= MAX_QUESTIONS_PER_DAY:
            return False
        _usage["count"] += 1
        return True

EXAMPLES = [
    "What was Equinor's adjusted operating income in 2025?",
    "What was DNB's return on equity in 2025?",
    "How many employees did Hydro have at the end of 2025?",
    "What dividend per share did the DNB board propose for 2025?",
    # Deliberately unanswerable: shows the system refusing and explaining why.
    "What was the closing price of Brent crude oil on 31 December 2025?",
    "How many employees did Hydro have in India at the end of 2025?",
]

CSS = """
/* Mid-tone colours on translucent backgrounds read well in both light and dark mode. */
.badge {display:inline-block;padding:4px 10px;border-radius:999px;font-weight:600;font-size:0.9em;margin-bottom:8px}
.badge-ok {background:rgba(46,160,67,0.18) !important;color:#2ea043 !important}
.badge-abstain {background:rgba(210,153,34,0.20) !important;color:#d29922 !important}
.answer {font-size:1.05em;line-height:1.55}
.cite {background:rgba(56,139,253,0.16) !important;color:#4493f8 !important;border-radius:4px;padding:0 4px;font-size:0.9em;white-space:nowrap}
.chunk {border:1px solid rgba(128,128,128,0.35);border-radius:8px;padding:10px 12px;margin:8px 0;font-size:0.9em}
.chunk-head {font-weight:600;color:#4493f8 !important;margin-bottom:4px}
.chunk-cited {border-color:#4493f8;border-width:2px}
"""


def _render_answer(text: str, abstained: bool) -> str:
    body = html.escape(text).replace("\n", "<br>")
    body = re.sub(r"\[([^\[\],]+?),\s*p\.\s*(\d+)\]", r'<span class="cite">\1, p.\2</span>', body)
    body = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", body)
    badge = ('<span class="badge badge-abstain">Abstained: not stated in the reports</span>'
             if abstained else '<span class="badge badge-ok">Answered from the reports</span>')
    return f'{badge}<div class="answer">{body}</div>'


def _render_chunks(chunks, cited: set[tuple[str, int]]) -> str:
    if not chunks:
        return "<p>No passages retrieved.</p>"
    parts = []
    for i, c in enumerate(chunks, 1):
        is_cited = (c.company, c.page) in cited
        text = html.escape(" ".join(c.text.split()))
        parts.append(
            f'<div class="chunk{" chunk-cited" if is_cited else ""}">'
            f'<div class="chunk-head">#{i} &middot; {html.escape(c.company)}, page {c.page}'
            f'{" &middot; cited in the answer" if is_cited else ""}</div>{text}</div>'
        )
    return "".join(parts)


def ask(question: str):
    question = (question or "").strip()
    if not question:
        return "<p>Type a question about the 2025 annual reports of Equinor, DNB or Hydro.</p>", ""
    if len(question) > MAX_QUESTION_CHARS:
        return f"<p>Please keep the question under {MAX_QUESTION_CHARS} characters.</p>", ""
    if not _take_quota():
        return ("<p>The demo has reached its daily question limit. Please try again tomorrow, "
                f'or run it yourself from <a href="{GITHUB_URL}">GitHub</a>.</p>'), ""
    try:
        from src.answer import answer
        result = answer(question)
    except FileNotFoundError:
        return "<p>The search index is missing. Run <code>python -m src.ingest</code> first.</p>", ""
    except Exception as exc:  # show a short message in the UI; full traceback goes to the logs
        logging.exception("Question failed: %s", question)
        hint = " Check the API key." if "auth" in type(exc).__name__.lower() or "api_key" in str(exc).lower() else ""
        return f"<p>Something went wrong ({html.escape(type(exc).__name__)}).{hint} Please try again.</p>", ""
    cited = {(c.company, c.page) for c in result.citations}
    return _render_answer(result.answer, result.abstained), _render_chunks(result.chunks, cited)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else f"_{path.name} not found._"


def _scorecard(path: Path) -> str:
    """Just the scorecard table from a report."""
    text = _read(path)
    m = re.search(r"## Scorecard\s*\n(.*?)(\n## |\Z)", text, re.S)
    if not m:
        return text
    rows = []
    for line in m.group(1).strip().splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 3:
            continue
        metric, score, notes = cells[0], cells[1], cells[2]
        if set(metric) <= set("-: "):
            rows.append("|---|---|")
            continue
        # Keep the metric and score, plus the raw counts from the notes column.
        counts = re.match(r"^(\d+/\d+|\d+ full / \d+ partial / \d+ wrong|\d+ false abstention)", notes)
        rows.append(f"| {metric} | {score}{(' (' + counts.group(1) + ')') if counts else ''} |")
    return "\n".join(rows)


EVAL_INTRO = f"""
### How the system is tested

Every answer is checked against a **human-verified answer key**: each reference answer was confirmed against the
source page of the report before any scoring. There are two sets:

- **Development set** (39 questions, 29 answerable and 10 that must be refused). Used to find failures and improve the
  system. Because the fixes were chosen after seeing these failures, its score is optimistic.
- **Held-out set** (20 new questions, 15 answerable and 5 that must be refused). Written and verified after all
  changes, then run **once** with the system frozen. **This is the honest number.**

Correctness and groundedness are scored by an LLM judge (`{config.JUDGE_MODEL}`). Citation validity, figure checks and
retrieval hit rate are purely programmatic.
"""

EVAL_LIMITS = """
### Known limitations

- **Charts.** Values that exist only in a chart lose their year-to-value alignment when the PDF is converted to text.
  This caused the one held-out failure (DNB's 2018 dividend): the right page was found, and the system abstained
  instead of guessing.
- **Lenient judge.** On one development question the judge accepted an answer that wrongly treated two production
  figures on different bases as the same. The groundedness check caught it (0.67), the correctness check did not.
- **Small scale.** Three reports, one language, 59 verified questions in total. This is a demo of grounded answering and
  honest evaluation, not a production document system.
"""


def build_app() -> gr.Blocks:
    with gr.Blocks(title="FinDocRAG") as demo:
        gr.Markdown(
            "# FinDocRAG\n"
            "Ask questions about the **2025 annual reports of Equinor, DNB and Norsk Hydro**. "
            "Every answer cites the report page it comes from. When the reports do not contain the answer, "
            "the system says so and explains what related information they do contain. "
            f"[Code, method and full evaluation on GitHub]({GITHUB_URL})."
        )
        with gr.Tab("Ask"):
            question = gr.Textbox(label="Your question", placeholder="e.g. What was Hydro's net debt at the end of 2025?",
                                  lines=2, max_lines=4)
            submit = gr.Button("Ask", variant="primary")
            answer_html = gr.HTML()
            with gr.Accordion("Retrieved passages (check the grounding yourself)", open=False):
                chunks_html = gr.HTML()
            gr.Examples(EXAMPLES, inputs=question, label="Try an example (the last two are deliberately unanswerable)")
            submit.click(ask, inputs=question, outputs=[answer_html, chunks_html], concurrency_limit=2)
            question.submit(ask, inputs=question, outputs=[answer_html, chunks_html], concurrency_limit=2)

        with gr.Tab("Evaluation"):
            gr.Markdown(EVAL_INTRO)
            with gr.Row():
                with gr.Column():
                    gr.Markdown("#### Held-out set (unseen, system frozen)\n" + _scorecard(config.EVAL_DIR / "report_heldout.md"))
                with gr.Column():
                    gr.Markdown("#### Development set (after improvements)\n" + _scorecard(config.EVAL_REPORT_PATH))
            with gr.Accordion("Development set: baseline before improvements", open=False):
                gr.Markdown("Dense search only, top 6 passages, no reranking.\n\n"
                            + _scorecard(config.EVAL_DIR / "report_baseline.md"))
            gr.Markdown(EVAL_LIMITS)
            with gr.Accordion("Full held-out report", open=False):
                gr.Markdown(_read(config.EVAL_DIR / "report_heldout.md"))
            with gr.Accordion("Full development report", open=False):
                gr.Markdown(_read(config.EVAL_REPORT_PATH))
    return demo


def main() -> None:
    build_app().queue(default_concurrency_limit=2).launch(css=CSS)


if __name__ == "__main__":
    main()
