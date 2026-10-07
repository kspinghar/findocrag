# FinDocRAG: remaining work, Claude Code handoff (18 Sep 2026)

Paste the block below into Claude Code with this folder (`C:\Users\khali\Projects\findocrag`) as the working directory.

Do the phases in order. Stop after each phase and report before starting the next.

---

## PASTE FROM HERE

You are continuing an existing project in the current directory. Do not scaffold a new folder.

Context: Phases 1 to 4 are built and ran once as a dry run on 10 Aug 2026. `src/ingest.py`, `src/retrieve.py`, `src/answer.py` and `src/evaluate.py` are complete. The FAISS index exists at `data/index/` (1377 chunks over 3 annual report PDFs). `eval/qa_candidates.jsonl` holds 40 draft questions, all with `"verified": false`. `app.py` is a stub. There is no git repository.

The point of this project is an honest evaluation harness. Never invent, round, or improve a number. Every metric that ends up in the README must come from an actual run of `python -m src.evaluate` against a human-verified answer key.

### Phase A: version control first

1. `git init`, confirm `.gitignore` already excludes `.env`, `.venv/`, `data/index/`, `data/reports/*.pdf`, `eval/.cache/`, `__pycache__/`, `.pytest_cache/`.
2. Also gitignore `eval/verification_worksheet.md` only if it contains no verdicts yet; if it has verdicts, commit it, it is evidence that the key was verified by hand.
3. Commit everything currently in the tree as the baseline: "Phases 1-4: ingest, retrieve, grounded answer, eval harness".
4. Do not create the GitHub remote yet.

### Phase B: build the verified answer key

Input: `eval/verification_worksheet.md`, which the user has filled in with a verdict under each question.

1. Read the worksheet. Each question has a `**Verdict:**` line set to one of `KEEP`, `FIX: <corrected answer>`, `DROP`, or for unanswerable items `MOVE TO ANSWERABLE: <answer>`.
2. If any verdict line is still the unedited template (`KEEP` / `FIX: ` / `DROP` all present on one line), stop and list those question ids. Do not guess.
3. Write `eval/qa_set.jsonl` with the same schema as `qa_candidates.jsonl` (`id`, `type`, `question`, `reference_answer`, `expected_sources`, `verified`), applying the verdicts: KEEP copies the draft answer, FIX replaces `reference_answer` with the corrected text, DROP omits the item, MOVE flips `type` to `answerable` and sets the answer. Set `"verified": true` on every item written.
4. Renumber nothing. Keep original ids so the worksheet and the report stay cross-referenceable.
5. Print a summary: N answerable, N unanswerable, N dropped, N corrected.
6. Commit: "Add human-verified 40-question answer key".

### Phase C: the honest baseline run

1. Delete `eval/.cache/` so nothing is reused from the dry run.
2. Run `python -m src.evaluate` with no `--allow-unverified` flag. It must find `eval/qa_set.jsonl` via `config.QA_SET_PATH` and refuse nothing.
3. Save the resulting `eval/report.md` and commit it verbatim as "Baseline eval run on verified key". This is the baseline. It does not get overwritten later.
4. Then triage the failures and report to me, do not fix anything yet:
   - False abstentions (the dry run had 3: DNB employee count, Hydro revenue, Hydro primary aluminium production). Diagnose whether the expected page was retrieved at all. Print the top-6 retrieved (company, page) for each failing question next to the expected pages. If the expected page never enters the top 6, it is a retrieval failure, not an answering failure.
   - Wrong answers (the dry run had 2 on Hydro figures). Check whether the correct figure was present in the retrieved context. If it was, it is an answering failure.
5. Report the split: how many failures are retrieval, how many are answering. Recommend at most two concrete changes.

### Phase D: one improvement round, measured

1. Implement only the changes I approve from Phase C.
2. Re-run the eval and write the new report to `eval/report.md`, keeping the baseline as `eval/report_baseline.md`.
3. The README will show both numbers, before and after, with what changed. This is the differentiator: a project that reports its own regression honestly is worth more than one claiming 100 percent.
4. Do not iterate further on the eval set. Repeated tuning against the same 40 questions is overfitting and I will not claim those numbers.

### Phase E: Gradio UI (Phase 5 of the original plan)

Implement `app.py`, two tabs, no placeholder code:

- **Ask tab:** question textbox, top_k slider (default `config.TOP_K`), Submit. Output shows the answer with its inline `[Company, p.X]` citations, a clear "Abstained" badge when `result.abstained` is true, and an expandable panel listing the retrieved chunks (company, page, score, text) so a viewer can check the grounding themselves. Include 4 or 5 example questions as clickable examples, including one deliberately unanswerable one so the abstention behaviour is visible without effort.
- **Evaluation tab:** renders `eval/report.md` as markdown, plus a short paragraph stating that the answer key was verified by hand against the source PDFs, the set size, and the honest-scope caveats from the README. Static read of the file, do not run the eval from the UI.
- Load the retriever lazily and cache it so startup is fast. Handle a missing index with a clear message rather than a traceback.
- `python app.py` must launch locally. Test it.
- Commit: "Phase 5: Gradio UI".

### Phase F: pin dependencies

1. Replace the ranges in `requirements.txt` with the exact versions installed in `.venv` (`pip freeze`, filtered to direct dependencies plus anything needed for the Space to build).
2. Verify a clean install still runs `python -m src.retrieve "test"` and `python app.py`.
3. Commit: "Pin dependencies".

### Phase G: GitHub

1. Create a public repo `findocrag` under github.com/kspinghar using `gh repo create` if the GitHub CLI is authenticated; otherwise print the exact commands for me to run.
2. Before pushing, verify with `git ls-files` that no PDF, no `.env`, and no `.venv` content is tracked. Confirm out loud.
3. Push `main`.

### Phase H: Hugging Face Space

Target: a Gradio Space under huggingface.co/kalspi, matching the user's existing demos.

1. The Space cannot run `ingest.py` (the PDFs are 60 MB and not committed). So the Space needs the prebuilt index. `data/index/` is about 6 MB total (`chunks.jsonl` 3.9 MB, `index.faiss` 2.1 MB), which is fine to commit to the Space repo directly, no LFS needed.
2. Decide and tell me which approach you are taking: a separate Space repo with the index committed, or the same repo with a Space-specific gitignore. Recommend one.
3. `ANTHROPIC_API_KEY` goes in as a Space secret, never in a file. Confirm `app.py` reads it from the environment and degrades with a clear message if absent.
4. Note that `bge-small-en-v1.5` downloads at runtime on the Space (about 130 MB). Make sure the first request does not time out: warm the model at startup.
5. Write the Space README header block (title, emoji, sdk: gradio, sdk_version, app_file, pinned: false).
6. Deploy, then verify the live Space actually answers one question and abstains on one. Report the URL.

### Phase I: README, last

Rewrite the README so it leads with the evaluation results:

1. Replace the "Status: work in progress" banner with links to the live Space and the repo.
2. Fill the "Evaluation results" section with the real scorecard table from `eval/report.md`, plus the before/after from Phase D if there was an improvement round.
3. State explicitly: 40 questions, N answerable and N unanswerable, answer key verified by hand against the source PDFs page by page, all LLM calls at temperature 0, judge model named.
4. Keep the existing "Honest scope" section and add anything the eval exposed.
5. List the known failure cases and why they fail. Do not hide them.
6. Commit and push.

## PASTE TO HERE

---

## Notes for me, not for Claude Code

- Phase B is blocked until `eval/verification_worksheet.md` is filled in. That is my work, roughly 30 to 60 minutes of reading evidence and ticking verdicts.
- Nothing about FinDocRAG goes on a CV until Phase I is done. Until then the claim stays "in progress" with no scores quoted.
- Two of the dry-run failures (Q17 Hydro employees, Q29 Hydro alumina) were checked on 18 Sep: the draft key figures 33,400 and 5,458 both appear verbatim on the expected Hydro pages 259 and 256. So those are genuine system failures, not key errors. Expect the real run to score similarly.
