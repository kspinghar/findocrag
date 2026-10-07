"""Placeholder so pytest passes on the scaffold. Real tests (chunking,
citation parsing) arrive with Phases 2-3."""


def test_config_imports() -> None:
    import config

    assert config.CHUNK_SIZE_TOKENS == 800
    assert config.ABSTAIN_STRING == "Not stated in the provided documents."
