"""Unit tests for the chunking logic in src.ingest."""
import pytest

import config
from src.ingest import chunk_text


@pytest.fixture(scope="module")
def tokenizer():
    from transformers import AutoTokenizer

    return AutoTokenizer.from_pretrained(config.EMBEDDING_MODEL)


def test_short_text_is_single_chunk(tokenizer) -> None:
    text = "Equinor reported strong results."
    assert chunk_text(text, tokenizer, chunk_size=800, overlap=100) == [text]


def test_long_text_respects_chunk_size(tokenizer) -> None:
    text = "The annual report describes revenue and emissions. " * 200
    chunks = chunk_text(text, tokenizer, chunk_size=100, overlap=20)
    assert len(chunks) > 1
    for chunk in chunks:
        n_tokens = len(tokenizer.encode(chunk, add_special_tokens=False))
        assert n_tokens <= 100 + 2  # decode/re-encode may shift a token or two


def test_consecutive_chunks_overlap(tokenizer) -> None:
    text = "word" + " alpha beta gamma delta epsilon zeta" * 100
    chunks = chunk_text(text, tokenizer, chunk_size=100, overlap=20)
    assert len(chunks) >= 2
    # The tail of chunk N should reappear at the head of chunk N+1.
    tail = chunks[0][-40:].strip()
    assert tail.split()[0] in chunks[1][:200]


def test_no_text_lost(tokenizer) -> None:
    text = "one two three four five six seven eight nine ten " * 50
    chunks = chunk_text(text, tokenizer, chunk_size=100, overlap=20)
    ids_original = tokenizer.encode(text, add_special_tokens=False)
    ids_last = tokenizer.encode(chunks[-1], add_special_tokens=False)
    # Last chunk must end exactly where the original ends.
    assert ids_original[-len(ids_last):] == ids_last
