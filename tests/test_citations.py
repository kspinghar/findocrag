"""Unit tests for citation parsing in src.answer."""
from src.answer import Citation, parse_citations


def test_single_citation() -> None:
    assert parse_citations("Revenue was USD 62,615 million [Equinor, p.252].") == [
        Citation(company="Equinor", page=252)
    ]


def test_multiple_and_order_preserved() -> None:
    text = "CET1 fell [DNB, p.55] while production rose [Hydro, p.16]."
    assert parse_citations(text) == [
        Citation(company="DNB", page=55),
        Citation(company="Hydro", page=16),
    ]


def test_duplicates_removed() -> None:
    text = "X [DNB, p.55]. Also Y [DNB, p.55]."
    assert parse_citations(text) == [Citation(company="DNB", page=55)]


def test_whitespace_tolerance() -> None:
    assert parse_citations("Z [Equinor,  p. 12].") == [
        Citation(company="Equinor", page=12)
    ]


def test_no_citations() -> None:
    assert parse_citations("Not stated in the provided documents.") == []


def test_ignores_non_citation_brackets() -> None:
    text = "Segment EBITDA [adjusted] grew [Hydro, p.150]."
    assert parse_citations(text) == [Citation(company="Hydro", page=150)]
