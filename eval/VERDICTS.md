# Answer key verification record

The 40 draft questions in `qa_candidates.jsonl` were checked by Khalid Spinghar on 7 and 8 October 2026 against the source report pages (one page per question, with the relevant figures highlighted, generated from the PDFs). `qa_set.jsonl` is the result and is the only file the evaluator scores against.

| Verdict | Questions |
|---|---|
| KEEP | 1, 2, 4 to 11, 13 to 15, 18 to 28, 30, and all unanswerable items 31 to 40 |
| FIX | 12 (DNB employees: 11,649 permanent and temporary), 16 and 29 (Hydro production, scoped to the sustainability statement production table), 17 (Hydro head count 33,400; "including temporary employees" removed) |
| DROP | 3 (Equinor Q4 dividend: the comparison figure in the draft could not be found in the report) |

Result: 39 items, 29 answerable and 10 unanswerable. Original ids are kept so this record, the worksheet and the reports cross-reference.

## Post-baseline key correction (8 October 2026)

- **Q29 (Hydro alumina production).** The baseline marked the system's answer of 6.1 million tonnes as wrong. Checking the report showed that 6.1 million tonnes is stated on p.14 (Bauxite & Alumina business area overview), while the key's 5,458 thousand tonnes comes from the sustainability statement table on p.256. The report gives two figures on different bases, so the key was too narrow. Approved by Khalid Spinghar: the reference now accepts either figure and lists both pages. This was an error in the key, not a change to the system. `report_baseline.md` is left as it was.
