"""Grounded RAG answering: retrieve top-k chunks, prompt the LLM to answer
ONLY from that context with [Company, p.X] citations, abstain when unsupported.

CLI:  python -m src.answer "your question"
"""
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass, field
from functools import lru_cache

from dotenv import load_dotenv

import config
from src.retrieve import RetrievedChunk, get_retriever

SYSTEM_PROMPT = f"""You answer questions about company annual reports (Equinor, DNB, and Norsk Hydro, 2025) using ONLY the document excerpts provided in the user message.

Rules:
1. Ground every statement in the excerpts. Use no outside knowledge, no estimates, no general knowledge about these companies.
2. Cite the source of every factual claim inline as [Company, p.X], where Company and X (the page number) come from the header line of the excerpt you used. Cite only excerpts you actually relied on.
3. If the excerpts do not contain the information needed to answer, reply with exactly this sentence and nothing else: {config.ABSTAIN_STRING}
4. If the excerpts only partially answer the question, answer the supported part and say what is not stated.
5. Be concise: a direct answer in one to three sentences, with figures quoted exactly as written in the excerpts (keep units and currency).
"""

# Matches inline citations like [Equinor, p.252]; page group is digits only.
CITATION_RE = re.compile(r"\[([^\[\],]+?),\s*p\.\s*(\d+)\]")


@dataclass
class Citation:
    """A single (company, page) reference parsed from the answer text."""

    company: str
    page: int


@dataclass
class AnswerResult:
    """Everything the UI and the eval harness need about one QA turn."""

    question: str
    answer: str
    citations: list[Citation] = field(default_factory=list)
    chunks: list[RetrievedChunk] = field(default_factory=list)
    abstained: bool = False


def parse_citations(text: str) -> list[Citation]:
    """Extract [Company, p.X] citations, deduplicated, in order of appearance."""
    seen: set[tuple[str, int]] = set()
    citations: list[Citation] = []
    for company, page in CITATION_RE.findall(text):
        key = (company.strip(), int(page))
        if key not in seen:
            seen.add(key)
            citations.append(Citation(company=key[0], page=key[1]))
    return citations


def build_context(chunks: list[RetrievedChunk]) -> str:
    """Format retrieved chunks as clearly-delimited, citable excerpts."""
    blocks: list[str] = []
    for i, c in enumerate(chunks, 1):
        blocks.append(f"--- Excerpt {i} [{c.company}, p.{c.page}] ---\n{c.text}")
    return "\n\n".join(blocks)


@lru_cache(maxsize=1)
def get_client():
    """Anthropic client; reads ANTHROPIC_API_KEY from .env / environment."""
    import anthropic

    load_dotenv()
    return anthropic.Anthropic()


def answer(question: str, top_k: int = config.TOP_K) -> AnswerResult:
    """Retrieve context and produce a grounded, cited answer (or abstain)."""
    chunks = get_retriever().search(question, top_k=top_k)
    context = build_context(chunks)

    response = get_client().messages.create(
        model=config.ANSWER_MODEL,
        max_tokens=config.MAX_ANSWER_TOKENS,
        temperature=0.0,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"{context}\n\nQuestion: {question}",
            }
        ],
    )
    text = "".join(b.text for b in response.content if b.type == "text").strip()
    # Prefix match: the model sometimes appends an explanation of what IS
    # stated after the abstention sentence — that is still an abstention.
    abstained = text.startswith(config.ABSTAIN_STRING)

    return AnswerResult(
        question=question,
        answer=text,
        citations=[] if abstained else parse_citations(text),
        chunks=chunks,
        abstained=abstained,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Ask a grounded question.")
    parser.add_argument("question")
    parser.add_argument("-k", type=int, default=config.TOP_K)
    args = parser.parse_args()

    result = answer(args.question, top_k=args.k)
    print(f"Q: {result.question}\n")
    print(f"A: {result.answer}\n")
    if result.abstained:
        print("(abstained)")
    else:
        cites = ", ".join(f"[{c.company}, p.{c.page}]" for c in result.citations)
        print(f"Citations: {cites or '(none found in answer)'}")
    print("\nRetrieved:")
    for i, c in enumerate(result.chunks, 1):
        print(f"  #{i} score={c.score:.3f} [{c.company}, p.{c.page}]")


if __name__ == "__main__":
    main()
