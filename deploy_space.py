"""Push the app to the Hugging Face Space. Uploads only what the app needs.

Needs a prior `hf auth login`. The token is read from the local Hugging Face
login and is never printed. The Anthropic API key is NOT uploaded: add it in the
Space settings as a secret named ANTHROPIC_API_KEY.

Usage:
    python deploy_space.py
"""
from __future__ import annotations

from pathlib import Path

from huggingface_hub import HfApi

ROOT = Path(__file__).resolve().parent
SPACE_ID = "kalspi/findocrag"
SPACE_HARDWARE = "zero-a10g"

# Source PDFs, tests and the answer-key worksheets stay on GitHub.
APP_FILES = [
    "app.py",
    "config.py",
    "src/*.py",
    "data/index/chunks.jsonl",
    "data/index/index.faiss",
    "eval/report.md",
    "eval/report_baseline.md",
    "eval/report_heldout.md",
]


def main() -> None:
    api = HfApi()
    # Free Hugging Face accounts can no longer create Gradio Spaces on cpu-basic.
    # They can host up to two on ZeroGPU hardware, so that is requested here.
    # The app itself only uses the CPU. With a PRO account, switch to "cpu-basic".
    api.create_repo(SPACE_ID, repo_type="space", space_sdk="gradio", space_hardware=SPACE_HARDWARE,
                    private=False, exist_ok=True)
    api.upload_folder(
        repo_id=SPACE_ID,
        repo_type="space",
        folder_path=str(ROOT),
        allow_patterns=APP_FILES,
        commit_message="Deploy app, index and evaluation reports",
    )
    for name in ("README.md", "requirements.txt"):
        api.upload_file(
            repo_id=SPACE_ID,
            repo_type="space",
            path_or_fileobj=str(ROOT / "space" / name),
            path_in_repo=name,
            commit_message=f"Space {name}",
        )
    print(f"Deployed to https://huggingface.co/spaces/{SPACE_ID}")


if __name__ == "__main__":
    main()
