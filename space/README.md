---
title: FinDocRAG
emoji: 📑
colorFrom: blue
colorTo: indigo
sdk: gradio
sdk_version: 6.22.0
python_version: "3.10"
app_file: app.py
pinned: false
license: mit
short_description: Cited Q&A over Equinor, DNB and Hydro annual reports
---

# FinDocRAG: grounded Q&A over annual reports, with an honest evaluation

Ask questions about the 2025 annual reports of Equinor, DNB and Norsk Hydro. Every answer cites the report page it
comes from. When the reports do not contain the answer, the system says so and explains what related information they
do contain.

On 20 unseen, human-verified questions: **93.3% correctness**, every unanswerable question refused, every citation
valid. See the Evaluation tab for the full scorecards and known limitations.

Code, method and evaluation: <https://github.com/kspinghar/findocrag>
