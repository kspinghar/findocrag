# FinDocRAG answer key: suggested verdicts (pre-check)

Source: `eval/verification_worksheet.md` + `eval/qa_candidates.jsonl`. These verdicts use only the worksheet evidence. They are suggestions for the human reviewer and are not final.

Parser note: the worksheet's "NOT FOUND" lines for `2,218` (Q7) and `7, 2026` (Q15), and the single-page hit for `240,000` (Q26), are artefacts of the format. The PDFs use a space as the thousands separator ("2 218", "240 000"), and the text is present on the expected pages.

| Q# | Question (short) | Draft answer | Suggested verdict | Reason (page / evidence) |
|---|---|---|---|---|
| 1 | Equinor equity production/day 2025 | 2,137 mboe/d | KEEP | p.4 "2,137 MBOE/D Equity oil & gas production per day in 2025"; p.41 "Group 2,137 mboe/day" |
| 2 | Equinor renewable power 2025 | 3.67 TWh, up from 2.93 | KEEP | p.4 "3.67 TWh Renewable power generation, Equinor share"; p.46 chart "2.93 / 3.67" for 2024/2025 (shown in Q18's p.46 snippet) |
| 3 | Equinor Q4 2025 dividend proposed | USD 0.39 (raised 2c from 0.37) | FIX: USD 0.39 per share (proposed 3 Feb 2026 to AGM on 12 May 2026) | p.226 "cash dividend for the fourth quarter of 2025 of USD 0.39 per share". `0.37` is **not found anywhere** in the parsed text, so drop the "raised by 2 cents from 0.37" clause |
| 4 | Equinor scope 1 GHG 2025 | 7.8 Mt CO2e, -5%, divestments | KEEP | p.114 "total scope 1 GHG emissions from own operations amounted to 7.8 million tonnes CO2e, a change of -5% from 2024 ... divestments in the international portfolio" |
| 5 | Equinor upstream CO2 intensity 2025 | 6.3 kg/boe, up from 6.2 | UNSURE | 6.3 is confirmed on p.4 ("6.3 KG/BOE Upstream CO2 intensity"). The 2024 figure of 6.2 is not visible in any p.74 snippet; the scan only says `6.2` occurs on p.74. Check p.74, or trim to "6.3 kg CO2/boe" |
| 6 | Equinor expected reserves YE2025 | 8,353 mmboe vs 8,857; -504 | KEEP | p.71 "8,353[12] million boe at year-end 2025, compared to 8,857 million boe at the end of 2024 ... net decrease of 504 million boe" (the "12" is a footnote marker) |
| 7 | DNB profit for the year 2025 | NOK 43,586m, down 2,218m / 4.8% | KEEP | p.52 "Profit for the year amounted to NOK 43 586 million, down NOK 2 218 million, or 4.8 per cent, from 2024" (the full sentence appears in Q24's p.52 snippet) |
| 8 | DNB CET1 ratio YE2025 | 17.9% (19.4% in 2024) | UNSURE | No snippet shows the CET1 sentence. p.55 gives indirect support only: "expectation ... 16.3 per cent ... CET1 capital ratio was thus 1.6 percentage point above", which gives 17.9. The 19.4 comparator is not shown. Check p.54/55 |
| 9 | DNB dividend proposed for 2025 | NOK 18.00, NOK 26.2bn, 62% payout | KEEP | p.63 "dividend of NOK 18.00 per share for 2025 ... total of NOK 26.2 billion ... payout ratio of 62 per cent of the Group's profits, or 86 per cent incl[uding buy-backs]"; also p.55 and p.6 |
| 10 | DNB ROE 2025 | 15.9% vs 17.5% | KEEP | p.52 "Return on equity was 15.9 per cent in 2025, compared with 17.5 per cent in the year-earlier period" (Q24 snippet) |
| 11 | DNB Carnegie price and completion date | SEK 13.8bn; completed 6 Mar 2025 | UNSURE | Both snippets are cut off before the price and the date. `13.8` occurs only on p.214, but its context is not shown. p.214 also shows "Total consideration ... settled in cash 14 447" (NOK m) and says "Contributions from Carnegie ... included as from 1 March 2025", which may conflict with "6 March". Check p.214 |
| 12 | DNB employees end-2025 | 11,649 (11,515 in 2024), sustainability-statement figure | DROP (or reword Q) | p.74 "At the end of 2025, DNB had a total of 11 649 employees (11 515 in 2024)[10]" is verbatim, but the draft itself says the accounts give a different figure, so there are two defensible answers. Keep it only if the question is reworded to name the sustainability statement/headcount definition. Read footnote 10 on p.74 |
| 13 | Hydro revenue 2025 | Revenue NOK 207,971m; total rev and income 213,281m | KEEP (make 207,971 the scored figure) | p.140 income statement "Revenue ... 207 971 203 636"; "Total revenue and income 213 281". The question is well defined because "Revenue" is the IFRS line item. The dry-run abstention looks like a retrieval/generation failure, not a key error |
| 14 | Hydro net income 2025 | NOK 8,304m; 6,717m to shareholders; EPS 3.41 | KEEP | p.140 "Net income (loss) 8 304 ... attributable to Hydro shareholders 6 717 ... earnings per share ... 3.41" |
| 15 | Hydro dividend proposed for 2025 | NOK 3.00, ~NOK 5.9bn, 60% adj. NI, AGM 7 May 2026 | KEEP | p.35 "NOK 5.9 billion ... 60 percent of 2025 adjusted net income per share and a dividend of NOK 3.0 per share ... Annual General Meeting on May 7, 2026"; p.65 table "Dividend per share 3.00" |
| 16 | Hydro primary aluminium production 2025 | 1,556 kt, up from 1,527 | FIX: 1,556 thousand tonnes (1,527 in 2024), per the production volumes table in the sustainability statement (ESRS E5-5) | Verbatim on p.256 "Primary aluminium production 1 556 1 527". The snippet does not state the ownership basis (100% consolidated, equity share, or excluding equity-accounted smelters). The Aluminium Metal business-area section may report a different total, which could explain the dry-run abstention. Human must check the scope |
| 17 | Hydro employees end-2025 | 33,400 (headcount incl. temporary), down from 33,798 | FIX: 33,400 employees (head count), down from 33,798 in 2024 | p.259 "Number of employees (head count) ... Total employees 33 400 33 798" is verbatim. "Including temporary employees" is not supported by the snippet; remove it, or confirm it on p.259 |
| 18 | Equinor total power generation 2025 | 5.65 TWh incl. Hywind Tampen, vs 4.92 | KEEP | p.4 "5.65 TWh Total power generation, Equinor share"; p.46 "5.65[1] TWh vs 4.92[1] TWh ... 1) Including Hywind Tampen" |
| 19 | Equinor RRR 2025 | 48%, 3-yr avg 100% | KEEP | p.71 "The 2025 reserves replacement ratio was 48% and the corresponding three-year average was 100%"; p.4 "48% RRR" |
| 20 | Equinor organic capex 2025 | USD 13.1bn | KEEP | p.54 "In 2025, our organic capital expenditure* was USD 13.1 billion" |
| 21 | Equinor scope 1+2 operated GHG vs 2015 | 10.1 Mt, same as 2024, -34% vs 2015 | KEEP | p.74 "absolute scope 1+2 operated greenhouse gas emissions were the same as in 2024, with a total of 10.1 million tonnes CO2e ... 34% reduction from our 2015 baseline" |
| 22 | Equinor Group employees 2025 | 24,620 total (24,140 permanent) | KEEP | p.138 "Number of all employees (Headcount) ... 24,620"; "permanent ... 24,140"; p.17 "around 24,600". The draft names both definitions explicitly, so it is scoreable |
| 23 | DNB total income 2025 | NOK 90,649m, record, +4.8% | KEEP | p.52 "total income rose by 4.8 per cent from 2024 to an all-time high level of NOK 90 649 million" |
| 24 | DNB EPS 2025 | NOK 28.45 vs 29.34 | KEEP | p.52 "earnings per share were NOK 28.45, down from NOK 29.34 in 2024" |
| 25 | DNB leverage ratio YE2025 | 6.6% vs 6.9% | UNSURE | The p.55 snippet does not include the leverage-ratio sentence. The scan only shows that `6.6` and `6.9` occur on p.55. Check p.55 |
| 26 | DNB personal and corporate customers | ~2.4m personal, 240,000 corporate | KEEP | p.74 "At the end of 2025, DNB had about 2.4 million personal customers and 240 000 corporate customers" |
| 27 | DNB Carnegie goodwill | NOK 8,579m (synergies, workforce, deferred tax) | KEEP | p.214 "The goodwill of NOK 8 579 million comprises the value of expected synergies ..., assembled workforce and deferred tax on excess values" |
| 28 | Hydro net debt YE2025 | NOK 9.7bn vs 16.0bn | KEEP | p.35 "Hydro's net debt was NOK 9.7 billion at the end of 2025, compared to net debt of NOK 16.0 billion at the end of 2024" (adjusted net debt of 18.2bn is a separate measure, correctly excluded) |
| 29 | Hydro alumina production 2025 | 5,458 kt vs 5,359 | KEEP (add same source qualifier as Q16) | Verbatim on p.256 "Alumina production 5 458 5 359". Same table as Q16, so the same ownership-basis question applies; the business-area section may give a 100% figure |
| 30 | Hydro share price YE2025 | NOK 78.20 | KEEP | p.64 "share price closed at NOK 78.2 at the end of 2025"; p.65 "Share price year-end, Oslo (NOK) 78.20" |
| 31 | DNB profit guidance for 2027 | ABSTAIN | UNSURE (lean KEEP) | The scan used only "profit, guidance, issued", not "2027", "target" or "ambition". If DNB states 2027 financial targets (e.g. ROE/cost-income), a model may answer from them. Search DNB for "2027" |
| 32 | Hydro total revenue 2010 | ABSTAIN | KEEP | No hit. The multi-year tables seen go back to 2021 only (p.65, p.256, p.259) |
| 33 | CEO of Telenor | ABSTAIN | UNSURE (lean KEEP) | The scan matched 4/4 keywords including "Telenor" on DNB p.34/35 (board bios), so Telenor is named in the corpus. Read those bios to make sure none says "CEO of Telenor" (current or former) |
| 34 | Equinor employees in China | ABSTAIN | KEEP | p.139 country table lists Brazil/Norway/UK/USA/Other. The footnote's "Other countries" list does not include China |
| 35 | DNB Sweden mortgage market share | ABSTAIN | KEEP | p.23 gives market shares for Norway only (mortgages 24%); no Swedish figure surfaced |
| 36 | Equinor dividend for FY2015 | ABSTAIN | KEEP | No dividend history back to 2015 surfaced. Optional check: the scan did not use "2015" as a keyword, and "2015" occurs on ~14 Equinor pages (mostly emissions baseline) |
| 37 | Equinor proved reserves YE2015 | ABSTAIN | KEEP | The reserve charts on p.71 cover 2023-2025 only. Same optional "2015" check as Q36 |
| 38 | Brent close on 31 Dec 2025 | ABSTAIN | KEEP | Only a derivatives passage surfaced (p.189). Low risk, but the market-overview pages may quote Brent prices (likely averages, not a closing price); quick "Brent" search advised |
| 39 | Users of Hydro's mobile banking app | ABSTAIN | KEEP | No passage matched; the premise is false (wrong entity) |
| 40 | Nordea CET1 2025 | ABSTAIN | UNSURE (lean KEEP) | "Nordea" is matched on DNB p.18 (The share) and p.341 (largest shareholders). Check that p.18 has no peer comparison showing Nordea's capital ratios |

## Items the human must look at closely

- **Q3 FIX**: `0.37` does not appear anywhere in the parsed text. Remove the "raised by 2 cents" clause.
- **Q5 UNSURE**: confirm 6.2 kg/boe for 2024 on p.74, or trim to 6.3 only.
- **Q8 UNSURE**: no snippet shows the CET1 sentence (17.9 is only implied by 16.3 + 1.6). Also confirm 19.4 for 2024.
- **Q11 UNSURE**: SEK 13.8bn and the "6 March 2025" date are not visible. The snippet says Carnegie is consolidated "from 1 March 2025" and shows the NOK consideration as 14,447m. Verify the date and currency on p.214.
- **Q12 DROP / reword**: DNB headcount has two defensible figures (sustainability statement vs accounts, which the draft itself admits). This explains the dry-run "false abstention". Either reword the question to pin the definition or drop it. Read footnote 10 on p.74.
- **Q13 scope**: the key is correct (Revenue = 207,971). Make sure the scorer treats 207,971 as the answer, with 213,281 as secondary. The dry-run abstention is a pipeline issue, not a key issue.
- **Q16 FIX (scope)** and **Q29 (same table)**: the p.256 production table does not state its consolidation basis. Check the Aluminium Metal / Bauxite and Alumina business-area pages for differently scoped totals. If they differ, qualify both answers with "per sustainability statement production table".
- **Q17 FIX**: "including temporary employees" is not supported by the snippet. The 33,400 headcount itself is verbatim on p.259.
- **Q25 UNSURE**: the leverage ratio sentence is not in the snippet. Verify 6.6% / 6.9% on p.55.
- **Q31, Q33, Q40 UNSURE (unanswerables)**: the keyword scans either missed the key term ("2027") or hit the named entity in the corpus (Telenor on DNB p.34/35, Nordea on DNB p.18). Check these quickly before confirming abstention.
- **Low-priority optional checks**: Q36/Q37 ("2015" not scanned as a keyword) and Q38 ("Brent" in the market overview).

Tally (40): KEEP 29 (22 answerable incl. Q13 and Q29 with notes, plus 7 unanswerable), FIX 3 (Q3, Q16, Q17), DROP 1 (Q12), UNSURE 7 (Q5, Q8, Q11, Q25, Q31, Q33, Q40).

## Addendum: UNSURE items resolved against chunks.jsonl (7 Oct 2026)

| Q# | Resolved suggestion | Exact text found |
|---|---|---|
| 5 | KEEP | Equinor p.74: "Upstream CO2 intensity increased to 6.3 kg CO2/boe in 2025 from 6.2 kg CO2/boe in 2024" |
| 8 | KEEP | DNB p.54: "CET1 capital ratio was 17.9 per cent at the end of 2025, down from 19.4 per cent at the end of 2024" |
| 11 | KEEP | DNB p.214: "completed on 6 March 2025. The purchase price was a cash consideration of SEK 13.8 billion" (accounting effect from 1 March) |
| 12 | KEEP: 11,649 permanent and temporary employees (11,515 in 2024) | Same figure on DNB p.74, p.152 ("11 649 permanent and temporary employees") and p.157 table. Remove any note about a conflicting figure |
| 25 | KEEP | DNB p.55: "The leverage ratio was 6.6 per cent at the end of 2025, down from 6.9 per cent in 2024" |
| 3 | FIX: USD 0.39 per share | "0.37" does not occur anywhere in the Equinor text |
| 16 / 29 | KEEP with scope note, or DROP 16 | Business-area pages do not state a different total; p.256 table is the only source |
| 31 | KEEP (unanswerable) | DNB p.31 has financial targets 2025 to 2027 (ROE, cost/income, CET1) but no profit guidance figure |
| 33 | KEEP (unanswerable) | Telenor appears only in DNB board bios (a board member chairs Telenor's board; another was in Telenor management). No CEO named |
| 38 | KEEP (unanswerable) | Only the 2025 average Brent price (69.1 USD/bbl, Equinor p.49/p.56) is given, not the 31 Dec closing price |
| 40 | KEEP (unanswerable) | Nordea appears only as a peer in DNB p.18 share chart footnotes |
