# FinDocRAG answer-key verification worksheet

Generated from `data/index/chunks.jsonl` (the same text the retriever sees) so you can verify without opening the PDFs.

**How to use.** For each item, read the evidence, then set the verdict. Edit this file in place.

- `KEEP` means the draft reference answer is correct as written.
- `FIX: <new answer>` means the figure or wording is wrong. Write the corrected answer.
- `DROP` means the question is unanswerable from these documents, or too ambiguous to score.

When done, tell Claude Code to apply the verdicts and write `eval/qa_set.jsonl` with `"verified": true`.

Note: `PAGE` numbers are PDF page indices from the parser, which may differ from the printed page numbers in the report.

---

## Part 1: answerable questions (30)

### Q1. What was Equinor's average equity oil and gas production per day in 2025?

**Draft answer:** 2,137 mboe per day (thousand barrels of oil equivalent per day).

**Expected source:** Equinor pp. 4, 41

**Where these figures actually appear in the document:**

- `2,137` in Equinor: pp. 4, 6, 37, 39, 40, 41, 49

**Evidence from the expected pages:**

> **[Equinor p.4]** Key figures
4 Key figures INTRODUCTION CONTENTS ABOUT US
OUR 
PERFORMANCE
SUSTAINABILITY 
STATEMENT
FINANCIAL 
STATEMENTS
ADDITIONAL 
INFORMATION
Equinor 2025 Annual report
Operational
2,137
MBOE/D
Equity oil & gas production 
per day in 2025
48%
RRR
Oil & gas reserves 
replacement ratio for 2025
5.65
TWh
Total power generation, 
Equinor share in 2025
3.67
TWh
Renewable power generation, 
Equinor share in 2025
More key figures in 2.1 Operati...

> **[Equinor p.41]** ...faks
Block 17
Aasta Hansteen
Visund
Johan Castberg
Åsgard
Skarv
Peregrino
Ormen Lange
Gina Krog
Caesar Tonga
Average equity production by country in 2025 (mboe/day)
1410
434
99
67
40
35
24
17 11
Norway USA Angola Brazil
Algeria UK Argentina Canada
Libya
Group
2,137
mboe/day
2025 was marked by record-
high production.
NCS production increased 
compared to 2024 as new 
fields and new wells more than 
offset natural decline.
Johan Sverdrup also delivered 
above expectations in 2025 as 
a result of production 
optimisa...

**Verdict:** `KEEP` / `FIX: ` / `DROP`

---

### Q2. How much renewable power did Equinor generate in 2025 (Equinor share)?

**Draft answer:** 3.67 TWh, an increase from 2.93 TWh in 2024.

**Expected source:** Equinor pp. 4, 46

**Where these figures actually appear in the document:**

- `2024` in Equinor: pp. 5, 14, 36, 39, 40, 41, 42, 43 (+148 more)
- `2.93` in Equinor: pp. 46, 49
- `3.67` in Equinor: pp. 4, 22, 46, 49

**Evidence from the expected pages:**

> **[Equinor p.4]** ...EMENT
FINANCIAL 
STATEMENTS
ADDITIONAL 
INFORMATION
Equinor 2025 Annual report
Operational
2,137
MBOE/D
Equity oil & gas production 
per day in 2025
48%
RRR
Oil & gas reserves 
replacement ratio for 2025
5.65
TWh
Total power generation, 
Equinor share in 2025
3.67
TWh
Renewable power generation, 
Equinor share in 2025
More key figures in 2.1 Operational 
performance
Financial
27.6
USD BILLION
Adjusted operating 
income*
18.0
USD BILLION
Cash flow from operations 
after tax* (CFFO)
9
USD BILLION
Capital 
distributio...

> **[Equinor p.46]** Operational performance 
for renewables, flexible 
power and low-carbon 
solutions
Group
Growth in the renewable energy portfolio drove the increase in 
Equinor’s total power generation compared to 2024. The ramp-up of 
Dogger Bank A and the addition of new onshore power plants in 
Scandinavia and Brazil in 2025 contributed to a 25% increase in 
renewable power generation, while gas-to-power generation 
remained stable compared to the previous year.
46 2...

**Verdict:** `KEEP` / `FIX: ` / `DROP`

---

### Q3. What cash dividend per share did Equinor's board propose for the fourth quarter of 2025?

**Draft answer:** USD 0.39 per share (raised by 2 cents from the USD 0.37 quarterly dividend).

**Expected source:** Equinor pp. 226, 65

**Where these figures actually appear in the document:**

- `0.37` in Equinor: **NOT FOUND anywhere in the parsed text**
- `0.39` in Equinor: pp. 226, 270

**Evidence from the expected pages:**

> **[Equinor p.226]** ...). Dividend declared in 2025 relates to the fourth quarter of 2024 and to the first three quarters of 2025.
On 3 February 2026, the board of directors proposed to the annual general meeting on 12 May 2026 a cash 
dividend for the fourth quarter of 2025 of USD 0.39 per share. The Equinor share will trade ex-dividend 13 May 2026 
on the Oslo Børs and 15 May 2026 for ADR holders on the New York Stock Exchange. Record date will be 15 May 
2026 and payment date will be 27 May 2026.
At 31 December
(in USD million) 2025 2...

> **[Equinor p.65]** Capital distribution
Equinor’s ambition is to grow its annual cash dividend, measured in 
USD per share, in alignment with long-term underlying earnings. In 
addition to cash dividends, Equinor may also engage in share 
b u y - b a c k s  a s  p a r t  o f  i t s  o v e r a l l  c a p i t a l  d i s t r i b u t i o n  s t r a t e g y .
Equinor aims to deliver competitive capital distribution throughout 
market cycles, with cash dividends serving as a firm and steadily 
increasing component, while share buy-backs pr...

**Verdict:** `KEEP` / `FIX: ` / `DROP`

---

### Q4. What were Equinor's scope 1 greenhouse gas emissions from its own operations in 2025?

**Draft answer:** 7.8 million tonnes CO2e, a 5% decrease from 2024, primarily due to divestments in the international portfolio.

**Expected source:** Equinor pp. 114

**Where these figures actually appear in the document:**

- `2024` in Equinor: pp. 5, 14, 36, 39, 40, 41, 42, 43 (+148 more)
- `7.8` in Equinor: pp. 50, 68, 106, 113, 114, 194, 219, 309

**Evidence from the expected pages:**

> **[Equinor p.114]** Scope 1
Power and heat generation represents the largest 
source of GHG emissions (scope 1) from our own 
operations. In 2025, our total scope 1 GHG emissions 
from own operations amounted to 7.8 million tonnes 
CO2e, a change of -5% from 2024. This reduction is 
primarily a result of divestments in the international 
portfolio.
Equinor receives a share of free quotas under the EU 
Emission Trading System (EU ETS). The share of free 
quotas is expected to be significantly reduced in the 
future...

> **[Equinor p.114]** ...trality 
involving the use of carbon credits.
114 E1 - Climate change INTRODUCTION CONTENTS ABOUT US
OUR 
PERFORMANCE
SUSTAINABILITY 
STATEMENT
FINANCIAL 
STATEMENTS
ADDITIONAL 
INFORMATION
Equinor 2025 Annual report
Generation of contractual instruments
2025 2024 2025 2025
Contractual instrument
Contractual instruments 
(MWh)
Contractual instruments 
(MWh)
Share of contractual 
instrument generation (%)
Electricity sales bundled 
with attributes related to 
contractual instruments (%)
Guarantees of Origin (GOs)1 2...

**Verdict:** `KEEP` / `FIX: ` / `DROP`

---

### Q5. What was Equinor's upstream CO2 intensity in 2025?

**Draft answer:** 6.3 kg CO2 per boe, up from 6.2 kg CO2/boe in 2024.

**Expected source:** Equinor pp. 74, 4

**Where these figures actually appear in the document:**

- `2024` in Equinor: pp. 5, 14, 36, 39, 40, 41, 42, 43 (+148 more)
- `6.2` in Equinor: pp. 49, 74, 108, 204
- `6.3` in Equinor: pp. 4, 42, 73, 74, 105, 108, 199, 279

**Evidence from the expected pages:**

> **[Equinor p.74]** ...nd set out key decarbonisation and transition 
ambitions. This section provides an overview of the 
progress achieved so far.
Continued leadership in upstream carbon 
efficiency
In 2025 absolute scope 1+2 operated greenhouse 
gas emissions were the same as in 2024, with a total 
of 10.1 million tonnes CO2e. This equates to a 34% 
reduction from our 2015 baseline13, progressing 
toward our 2030 ambition of a 50% net reduction. 
Reductions in emissions were achieved by 
electrification projects and energy efficiency...

> **[Equinor p.74]** low carbon solutions in 
2025 was USD 2.9 billion, compared to USD 2.2 billion 
in 2024. The main contributor was the Empire Wind 
project with additional contributions to equity 
accounted investments including Dogger Bank, Bałtyk 
2 & 3 and our onshore renewables portfolio. If 
financial investments in Ørsted are included, total 
investmen...

> **[Equinor p.4]** ...low from operations 
after tax* (CFFO)
9
USD BILLION
Capital 
distribution
14.5%
ROACE
Return on average capital 
employed, adjusted*
More key figures in 2.2 Financial 
performance
Sustainability
0.21
SIF
Serious incident frequency 
(per million hours worked)
6.3
KG/BOE
Upstream CO2 
intensity 
34%
EMISSIONS REDUCTIONS
Reduction in Scope 1+2 
operated emissions since 2015
4%
NCI REDUCTIONS
Net carbon intensity 
reduction since 2019
* For items marked with an asterisk throughout this report, see section 5.5 Use and...

**Verdict:** `KEEP` / `FIX: ` / `DROP`

---

### Q6. How large were Equinor's expected oil and gas reserves at year-end 2025?

**Draft answer:** 8,353 million boe, compared to 8,857 million boe at the end of 2024 (a net decrease of 504 million boe).

**Expected source:** Equinor pp. 71

**Where these figures actually appear in the document:**

- `8,857` in Equinor: pp. 71
- `8,353` in Equinor: pp. 71
- `2024` in Equinor: pp. 5, 14, 36, 39, 40, 41, 42, 43 (+148 more)
- `504` in Equinor: pp. 71, 112, 179, 195, 215, 222, 226, 227 (+4 more)

**Evidence from the expected pages:**

> **[Equinor p.71]** ...l economic planning assumptions (EPA) where 
product prices vary with time. The results are 
presented as equity volumes.
Expected oil and gas reserves were estimated to be 
8,35312 m i l l i o n  b o e  a t  y e a r - e n d  2 0 2 5 ,  c o m p a r e d  t o  
8,857 million boe at the end of 2024. This represents a 
net decrease of 504 million boe. The total equity 
production in 2025 was 780 million boe, compared to 
757 million boe in 2024.
Of the total expect e d  r e s e r v e s  a t  y e a r - e n d  2 0 2 5 ,...

> **[Equinor p.71]** ...nor’s 
website at www.equinor.com/reports.
71 2.2 Financial performance INTRODUCTION CONTENTS ABOUT US
OUR 
PERFORMANCE
SUSTAINABILITY 
STATEMENT
FINANCIAL 
STATEMENTS
ADDITIONAL 
INFORMATION
Equinor 2025 Annual report
Expected reserves
(in million boe)
8,935 8,857 8,353
5,632 5,689 5,322
3,302 3,169 3,031
RC1 RC2-3
2023 2024 2025
Proved reserves
(in million boe)
5,214 5,571 5,183
3,459 3,572 3,569
1,755 1,999 1,614
Proved developed reserves
Proved undeveloped reserves
2023 2024 2025 12) Volumes related to the dive...

**Verdict:** `KEEP` / `FIX: ` / `DROP`

---

### Q7. What was DNB Group's profit for the year 2025?

**Draft answer:** NOK 43,586 million, down NOK 2,218 million or 4.8 per cent from 2024.

**Expected source:** DNB pp. 52

**Where these figures actually appear in the document:**

- `43,586` in DNB: pp. 8, 208, 210, 216, 292
- `2,218` in DNB: **NOT FOUND anywhere in the parsed text**
- `2024` in DNB: pp. 2, 6, 7, 8, 9, 13, 17, 18 (+196 more)
- `4.8` in DNB: pp. 9, 20, 52, 100, 126, 129

**Evidence from the expected pages:**

> **[DNB p.52]** ...s on three main 
ambitions: the customer chooses us, we deliver sustainable 
value creation and we find the solutions together. Read 
more about the Group’s strategy in the sub-chapter 
Strategy.
Operations in 2025
DNB’s total income rose by 4.8 per cent from 2024 to an 
all-time high level of NOK 90 649 million in 2025, but there 
was a decline in profit due to higher costs, impairment of 
financial instruments and tax expenses. Profit for the year 
amounted to NOK 43 586 million, down NOK 2 218 million, 
or 4.8 p...

**Verdict:** `KEEP` / `FIX: ` / `DROP`

---

### Q8. What was DNB's common equity Tier 1 (CET1) capital ratio at year-end 2025?

**Draft answer:** 17.9 per cent, down from 19.4 per cent in 2024.

**Expected source:** DNB pp. 55, 54

**Where these figures actually appear in the document:**

- `2024` in DNB: pp. 2, 6, 7, 8, 9, 13, 17, 18 (+196 more)
- `17.9` in DNB: pp. 7, 9, 14, 54, 55, 63, 190, 217 (+1 more)
- `19.4` in DNB: pp. 7, 9, 54, 55, 58, 59, 190, 217 (+1 more)

**Evidence from the expected pages:**

> **[DNB p.55]** ...from the supervisory authorities was 
16.3 per cent, including Pillar 2 Guidance. The Group’s 
CET1 capital ratio was thus 1.6 percentage point above the 
supervisory authorities’ expectation. 
The risk exposure amount (REA) increased by NOK 50 billion 
from 2024, to NOK 1 171 billion at year-end 2025. Of 
this, NOK 32 billion was due to operational risk, driven by 
the increase in the Group’s total income in recent years, 
including the effects of the Carnegie acquisition. Total REA 
for credit risk increased by...

> **[DNB p.54]** ..., as well as increased public 
spending to strengthen the defence sector in Europe, with 
an associated rise in interest rates on government bonds.
DNB issued bonds totalling NOK 117 billion in EUR, USD, 
SEK and NOK in 2025, compared with NOK 121 billion 
in 2024. The largest number of issues in 2025 – about 
58 per cent of the total – were linked to covered bonds, 
followed by just under 20 per cent each of senior preferred 
and senior non-preferred bonds. In addition, the Group 
issued lower volumes in the form...

> **[DNB p.54]** in the Group’s 
balance sheet were NOK 3 695 billion at end-December, 
compared with NOK 3 614 billion at end-December 2024. 
The ratio of customer deposits to net loans to customers 
for the customer segments was 72.2 per cent, down from 
74.3 per cent a year earlier.
Capital
The amended Capital Requirements Regulation (CRR3) 
entered into force in Norway on 1 April 2025. The...

**Verdict:** `KEEP` / `FIX: ` / `DROP`

---

### Q9. What dividend per share has DNB's board proposed for 2025?

**Draft answer:** NOK 18.00 per share, a total of NOK 26.2 billion, corresponding to a payout ratio of 62 per cent.

**Expected source:** DNB pp. 63, 55, 6

**Where these figures actually appear in the document:**

- `18.00` in DNB: pp. 6, 9, 19, 52, 55, 63, 287, 298 (+1 more)
- `26.2` in DNB: pp. 15, 63
- `62` in DNB: pp. 6, 8, 9, 19, 20, 53, 54, 57 (+100 more)

**Evidence from the expected pages:**

> **[DNB p.63]** ...be used as a flexible tool for 
allocating excess capital to DNB’s owners. 
DNB is well capitalised and has a 1.6-percentage point 
headroom above the supervisory authorities’ current capital 
level expectation. The Board has thus proposed a dividend 
of NOK 18.00 per share for 2025, for distribution from 
30 April 2026, and this means that DNB Bank ASA will 
distribute a total of NOK 26.2 billion in dividends for 2025. 
This corresponds to a payout ratio of 62 per cent of the 
Group’s profits, or 86 per cent incl...

> **[DNB p.63]** current capital 
level expectation. The Board has thus proposed a dividend 
of NOK 18.00 per share for 2025, for distribution from 
30 April 2026, and this means that DNB Bank ASA will 
distribute a total of NOK 26.2 billion in dividends for 2025. 
This corresponds to a payout ratio of 62 per cent of the 
Group’s profits, or 86 per cent incl...

> **[DNB p.55]** ...e buy-
back programmes totalling 2.5 per cent contributed further 
to the reduction in CET1 capital.
DNB’s strong capital position provides a firm foundation for 
continued delivery on the Group’s dividend policy, and the 
Board has proposed a dividend of NOK 18.00 per share for 
2025, for distribution from 30 April. The CET1 capital ratio 
requirement for DNB was 15.3 per cent at the end of 2025, 
while the expectation from the supervisory authorities was 
16.3 per cent, including Pillar 2 Guidance. The Group’s 
C...

> **[DNB p.6]** ...200
250
300
350
400
450
Share dividend and payout ratio
62% 65%
91% 86%
64%
Per centNOK per share
0 
20
40
60
80
100
Dividend (NOK) Share buy-backs (NOK)2 Total payout ratio (per cent)
2021 2022 2023 2024 2025 Target
0
5
10
15
20
25
30
> 50%
12.50
16.00 16.75 18.001
0.99
6.90
2.16
6.79
9.75
1 The Board of Directors has proposed a dividend of NOK 18.00 per share for 2025. 
2 Share buy-backs approved by both the Annual General Meetings and Finanstilsynet (the Norwegian Financial Supervisory Authority).
Contents
6
DNB...

**Verdict:** `KEEP` / `FIX: ` / `DROP`

---

### Q10. What was DNB's return on equity in 2025?

**Draft answer:** 15.9 per cent, compared with 17.5 per cent in 2024.

**Expected source:** DNB pp. 52

**Where these figures actually appear in the document:**

- `2024` in DNB: pp. 2, 6, 7, 8, 9, 13, 17, 18 (+196 more)
- `15.9` in DNB: pp. 7, 9, 11, 52, 216, 219
- `17.5` in DNB: pp. 7, 9, 52, 59, 216

**Evidence from the expected pages:**

> **[DNB p.52]** ...s on three main 
ambitions: the customer chooses us, we deliver sustainable 
value creation and we find the solutions together. Read 
more about the Group’s strategy in the sub-chapter 
Strategy.
Operations in 2025
DNB’s total income rose by 4.8 per cent from 2024 to an 
all-time high level of NOK 90 649 million in 2025, but there 
was a decline in profit due to higher costs, impairment of 
financial instruments and tax expenses. Profit for the year 
amounted to NOK 43 586 million, down NOK 2 218 million, 
or 4.8 p...

**Verdict:** `KEEP` / `FIX: ` / `DROP`

---

### Q11. How much did DNB pay to acquire Carnegie, and when was the transaction completed?

**Draft answer:** A cash consideration of SEK 13.8 billion; the transaction was completed on 6 March 2025.

**Expected source:** DNB pp. 214

**Where these figures actually appear in the document:**

- `2025` in DNB: pp. 1, 2, 3, 5, 6, 7, 8, 9 (+345 more)
- `13.8` in DNB: pp. 214

**Evidence from the expected pages:**

> **[DNB p.214]** Note G2 Aquisitions
220   /   DNB GROUP – ANNUAL REPORT 2025 
Note G2 Aquisitions 
Acquisition of Carnegie Group 
On 21 October 2024, DNB announced an agreement to acquire all the shares of Carnegie Holding AB, the parent company of the Carnegie 
Group. Following the fulfilment of all conditions precedent, includin...

> **[DNB p.214]** ...quire the Carnegie Group, and NOK 167 million was recognised in the income statement for 
acquisition‑related costs, of which NOK 45 million was recognised in 2024. Contributions from Carnegie to the DNB Group’s income statements 
are included as from 1 March 2025. If the business combination had taken place at the beginning of the year, the total income would be NOK 91 
323 million and the pre-tax operating profit for the Group would have been NOK 53 543 million at end-December 2025.   
 
Acquisition of Eksportfin...

**Verdict:** `KEEP` / `FIX: ` / `DROP`

---

### Q12. How many employees did DNB have at the end of 2025?

**Draft answer:** 11,649 employees (11,515 in 2024), per the sustainability statement (differs from the accounts figure).

**Expected source:** DNB pp. 74

**Where these figures actually appear in the document:**

- `11,515` in DNB: pp. 157
- `11,649` in DNB: pp. 74, 152, 157
- `2024` in DNB: pp. 2, 6, 7, 8, 9, 13, 17, 18 (+196 more)

**Evidence from the expected pages:**

> **[DNB p.74]** ...ected industries 
and sectors such as energy, seafood, shipping and health, 
as well as technology and telecom. Loans to customers in 
different sectors (industry segments) are shown in note G12 
to the annual accounts. 
At the end of 2025, DNB had a total of 11 649 employees 
(11 515 in 2024)10. The distribution between geographical 
locations is shown in the table below. DNB has a presence in 
a total of 19 countries.
Geographical location
Number of 
employees 2025
Number of 
employees 2024
Norway 9 280 9 861
Eur...

> **[DNB p.74]** customers and investments 
from shareholders. Technology and data are obtained and 
developed through collaboration with technology partners 
and in internal innovation projects. Human resources are 
recruited and developed using comprehensive training 
programmes and career development opportunities. Another 
input factor that is required to conduct operations is energy, 
water and commodities needed to operate office premises. 
The Group’s operating income comes mainly from net interest 
income and fees and commi...

**Verdict:** `KEEP` / `FIX: ` / `DROP`

---

### Q13. What was Hydro's revenue in 2025?

**Draft answer:** Revenue of NOK 207,971 million; total revenue and income of NOK 213,281 million.

**Expected source:** Hydro pp. 140

**Where these figures actually appear in the document:**

- `213,281` in Hydro: pp. 140
- `207,971` in Hydro: pp. 37, 106, 140, 151, 153, 175, 291

**Evidence from the expected pages:**

> **[Hydro p.140]** ...in NOK million (except per share amounts). Years ended December 31 Notes 2025 2024
Revenue 1.4, 5.1  207 971  203 636 
Share of profit (loss) in equity accounted investments 1.4, 5.1  121  (516) 
Other income, net 5.2  5 189  5 543 
Total revenue and income  213 281  208 663 
Raw material and energy expense 5.3  133 116  129 349 
Employee benefits expense 9.2  28 060  26 946 
Depreciation and amortization expense 2.4  10 328  10 131 
Impairment of non-current assets 2.5  1 148  39 
Other expenses  26 228  25 712...

**Verdict:** `KEEP` / `FIX: ` / `DROP`

---

### Q14. What was Hydro's net income in 2025?

**Draft answer:** NOK 8,304 million, of which NOK 6,717 million attributable to Hydro shareholders; earnings per share NOK 3.41.

**Expected source:** Hydro pp. 140

**Where these figures actually appear in the document:**

- `6,717` in Hydro: pp. 140, 143
- `8,304` in Hydro: pp. 34, 37, 140, 142, 152, 234
- `3.41` in Hydro: pp. 37, 65, 140

**Evidence from the expected pages:**

> **[Hydro p.140]** ...et  (680)  (7 625) 
Income (loss) before tax  13 721  8 862 
Income taxes 10.1  (5 417)  (3 822) 
Net income (loss)  8 304  5 040 
Net income (loss) attributable to non-controlling interests  1 587  (750) 
Net income (loss) attributable to Hydro shareholders  6 717  5 790 
Basic and diluted earnings per share attributable to Hydro shareholders 7.6  3.41  2.90 
The accompanying notes are an integral part of the consolidated financial statements
Consolidated statement of other comprehensive income
Amounts in NOK mill...

**Verdict:** `KEEP` / `FIX: ` / `DROP`

---

### Q15. What dividend has Hydro's board proposed for 2025?

**Draft answer:** NOK 3.00 per share, about NOK 5.9 billion in total, representing 60 percent of 2025 adjusted net income; subject to AGM approval on May 7, 2026.

**Expected source:** Hydro pp. 35, 64, 65

**Where these figures actually appear in the document:**

- `7, 2026` in Hydro: **NOT FOUND anywhere in the parsed text**
- `2025` in Hydro: pp. 1, 2, 3, 4, 5, 6, 7, 8 (+284 more)
- `3.00` in Hydro: pp. 65, 185, 202, 215
- `5.9` in Hydro: pp. 5, 33, 35, 65, 196, 257, 305

**Evidence from the expected pages:**

> **[Hydro p.35]** ...er competitive shareholder returns compared to 
alternative investments in comparable companies. Considering Hydro’s strong 
financial performance, the Board of Directors has proposed to distribute NOK 
5.9 billion in dividends, which represents 60 percent of 2025 adjusted net 
income per share and a dividend of NOK 3.0 per share. The final shareholder 
distribution for 2025 is subject to approval by the Annual General Meeting on 
May 7, 2026.
Net debt1
Hydro’s net debt was NOK 9.7 billion at the end of 2025, compa...

> **[Hydro p.64]** The Hydro share
Introduction
Hydro’s share price closed at NOK 78.2 at the end of 2025. The return ex. 
dividend1 for 2025 was a positive NOK 14.8 or a positive 23.3 percent. Hydro 
paid its 2024 dividend of 2.25 NOK per share in May 2025. No new share 
buyback program was approved during the year. The share buyback program 
initiated in Se...

> **[Hydro p.64]** share 
price for the year.
2 Total shareholder return includes the opening share price, dividends and closing share price.
3 TSR calculated including reinvesting dividends. Hydro and all peers shown in same currency 
(USD).
4 Peer group includes Nalco, Rusal, Alcoa, Century Aluminium, Hindalco, Chalco, Grupa Kety, 
Constellium, Kaiser, ProfilGruppen, Tredegar Corporation. Source: Refinitiv retrieves.

> **[Hydro p.65]** ...to be considered and approved by the 
Annual General Meeting. Authorizations are granted for a specific time period 
and for a specific share price interval during which share buybacks can be 
made, in accordance with applicable regulation.
Common share data  2025  2024  2023  2022  2021 
Share price high, Oslo (NOK)1  79.12  75.10  84.04  89.95  71.46 
Share price low, Oslo (NOK)1  50.60  53.24  56.63  51.49  36.99 
Share price average, Oslo (NOK)  64.59  64.26  68.85  69.34  55.94 
Share price year-end, Oslo (NOK...

> **[Hydro p.65]** price high and low based on intraday, not only closing price.
2 Alternative performance measures (APMs) are described in the appendices.
3 2025 dividend per share proposed by Board of Directors, dependent on approval from the Annual General Meeting May 7, 2026.
4 Dividend per share divided by adjusted earnings per share from continuing operations.
5 Average dividend per share divided by average a...

**Verdict:** `KEEP` / `FIX: ` / `DROP`

---

### Q16. How much primary aluminium did Hydro produce in 2025?

**Draft answer:** 1,556 thousand tonnes (1.556 million tonnes), up from 1,527 thousand tonnes in 2024.

**Expected source:** Hydro pp. 256

**Where these figures actually appear in the document:**

- `1.556` in Hydro: pp. 256
- `1,527` in Hydro: pp. 256
- `1,556` in Hydro: pp. 256
- `2024` in Hydro: pp. 3, 5, 6, 15, 21, 23, 26, 27 (+141 more)

**Evidence from the expected pages:**

> **[Hydro p.256]** ...in the Extrusions business area.
Reference: ESRS E5-5.
Production volumes
thousand tonnes 2025 2024 2023 2022 2021
Bauxite production  10 496  10 506  10 897  11 012  10 926 
Alumina production  5 458  5 359  5 626  5 586  5 894 
Primary aluminium production  1 556  1 527  1 536  1 636  1 688 
    Hydro REDUXA  470  418  349  421 
Recycling casthouse production  1 895  1 751  1 787  1 664 
    Hydro CIRCAL  58  57  51  50 
Extruded products  1 013  1 024 1116¹⁾  1 670  1 687 
E5.3 Resource outflows –Non-mineral was...

> **[Hydro p.256]** . Changing methodologies over time 
also creates challenges in comparing consolidated waste data from one year to another. 
Waste treatment operations can occur both onsite and offsite treatment. In many cases, waste is managed by third 
parties, which are required to adhere to the Hydro Supplier Code of Conduct
. All Hydro locations are required to 
ensure safe transport of hazardous waste in accordance with global and local regulations, and evaluate critical waste 
receivers and include these in a supplier develo...

**Verdict:** `KEEP` / `FIX: ` / `DROP`

---

### Q17. How many employees did Hydro have at the end of 2025?

**Draft answer:** 33,400 employees (head count including temporary employees), down from 33,798 in 2024.

**Expected source:** Hydro pp. 259

**Where these figures actually appear in the document:**

- `33,798` in Hydro: pp. 259
- `33,400` in Hydro: pp. 259
- `2024` in Hydro: pp. 3, 5, 6, 15, 21, 23, 26, 27 (+141 more)

**Evidence from the expected pages:**

> **[Hydro p.259]** ...7 (2021); ESRS S1-6.
Number of employees (head count), by gender
Gender 2025 2024 2023 2022 2021
Male  25 336  25 724  26 901  26 805  26 781 
Female  8 062  8 073  7 589  7 126  6 282 
Other  0  0  0  0  0 
Not reported  2  1  4  0  0 
Total employees 33 400 33 798 34 494 33 931 33 063
 Number of employees (head count), by country
Country 2025 2024 2023 2022 2021
Brazil 7 100 7 059 6 915 6 827 6 643
Norway 4 438 4 858 4 683 4 485 4 245
USA 5 536 5 606 5 993 6 164 5 932
Other 16 326 16 275 16 903 16 455 16 243
Tota...

**Verdict:** `KEEP` / `FIX: ` / `DROP`

---

### Q18. What was Equinor's total power generation (Equinor share) in 2025?

**Draft answer:** 5.65 TWh (including Hywind Tampen), up from 4.92 TWh in 2024.

**Expected source:** Equinor pp. 4, 46

**Where these figures actually appear in the document:**

- `4.92` in Equinor: pp. 46, 49
- `2024` in Equinor: pp. 5, 14, 36, 39, 40, 41, 42, 43 (+148 more)
- `5.65` in Equinor: pp. 4, 7, 46, 49

**Evidence from the expected pages:**

> **[Equinor p.4]** ...CONTENTS ABOUT US
OUR 
PERFORMANCE
SUSTAINABILITY 
STATEMENT
FINANCIAL 
STATEMENTS
ADDITIONAL 
INFORMATION
Equinor 2025 Annual report
Operational
2,137
MBOE/D
Equity oil & gas production 
per day in 2025
48%
RRR
Oil & gas reserves 
replacement ratio for 2025
5.65
TWh
Total power generation, 
Equinor share in 2025
3.67
TWh
Renewable power generation, 
Equinor share in 2025
More key figures in 2.1 Operational 
performance
Financial
27.6
USD BILLION
Adjusted operating 
income*
18.0
USD BILLION
Cash flow from operatio...

> **[Equinor p.46]** ...tart up.
Renewable power generation (TWh)
Equinor share
1.66 1.56 1.65
1.94
2.93
3.67
2020 2021 2022 2023 2024 2025
MMP
Power generation from CCGTs 
remained at similar levels to the 
previous year.
Power generation Equinor share
2025
Group
5.651
TWh
VS
Group
4.921
TWh
2024
1) Including Hywind Tampen renewable-power generation of 0.17 TWh in 2025 and 0.13 TWh in 2024. Hywind Tampen is owned by E&P Norway and operated by REN.

**Verdict:** `KEEP` / `FIX: ` / `DROP`

---

### Q19. What was Equinor's reserves replacement ratio for 2025?

**Draft answer:** 48%, with a three-year average of 100%.

**Expected source:** Equinor pp. 4, 71

**Where these figures actually appear in the document:**

- `100` in Equinor: pp. 3, 16, 31, 39, 45, 47, 50, 63 (+45 more)
- `48` in Equinor: pp. 4, 25, 41, 48, 49, 50, 58, 64 (+65 more)

**Evidence from the expected pages:**

> **[Equinor p.4]** Key figures
4 Key figures INTRODUCTION CONTENTS ABOUT US
OUR 
PERFORMANCE
SUSTAINABILITY 
STATEMENT
FINANCIAL 
STATEMENTS
ADDITIONAL 
INFORMATION
Equinor 2025 Annual report
Operational
2,137
MBOE/D
Equity oil & gas production 
per day in 2025
48%
RRR
Oil & gas reserves 
replacement ratio for 2025
5.65
TWh
Total power generation, 
Equinor share in 2025
3.67
TWh
Renewable power generation, 
Equinor share in 2025
More key figures in 2.1 Operational 
performance
Financial
27.6
USD BILLION
Adjusted oper...

> **[Equinor p.71]** ...illion boe were proved undeveloped reserves.
Reserves replacement
The reserves replacement ratio is defined as the net 
amount of proved reserves added for a given period 
divided by produced volumes in the same period.
The 2025 reserves replacement ratio was 48% and 
t h e  c o r r e s p o n d i n g  t h r e e - y e a r  a v e r a g e  w a s  1 0 0 % ,  
compared to 151% and 110%, respectively, at the end 
of 2024.
The organic reserves replacement ratio, excluding 
sales and purchases, was 61% in 2025 compared to...

> **[Equinor p.71]** given period 
divided by produced volumes in the same period.
The 2025 reserves replacement ratio was 48% and 
t h e  c o r r e s p o n d i n g  t h r e e - y e a r  a v e r a g e  w a s  1 0 0 % ,  
compared to 151% and 110%, respectively, at the end 
of 2024.
The organic reserves replacement ratio, excluding 
sales and purchases, was 61% in 2025 compared to...

**Verdict:** `KEEP` / `FIX: ` / `DROP`

---

### Q20. How large was Equinor's organic capital expenditure in 2025?

**Draft answer:** USD 13.1 billion.

**Expected source:** Equinor pp. 54

**Where these figures actually appear in the document:**

- `13.1` in Equinor: pp. 54, 311

**Evidence from the expected pages:**

> **[Equinor p.54]** ...gh-graded project portfolio. 
Equinor plans to allocate organic capital 
expenditure* as follows: around 60% to the NCS, 
30% to international oil and gas projects, and 
10%8 to our integrated power business. In 2025, 
our organic capital expenditure* was USD 13.1 
billion.
Strong balance sheet
Ensuring a solid balance sheet and necessary 
financial flexibility is important to support a 
dynamic strategy through economic and 
market cycles. We also aim to maintain a credit 
rating within the single A category on a...

**Verdict:** `KEEP` / `FIX: ` / `DROP`

---

### Q21. What were Equinor's absolute scope 1+2 operated GHG emissions in 2025, and how do they compare to the 2015 baseline?

**Draft answer:** 10.1 million tonnes CO2e, the same as 2024, equal to a 34% reduction from the 2015 baseline.

**Expected source:** Equinor pp. 74

**Where these figures actually appear in the document:**

- `2024` in Equinor: pp. 5, 14, 36, 39, 40, 41, 42, 43 (+148 more)
- `10.1` in Equinor: pp. 74, 105, 108, 113, 244
- `2015` in Equinor: pp. 4, 16, 73, 74, 77, 101, 102, 105 (+6 more)
- `34` in Equinor: pp. 4, 20, 34, 40, 41, 43, 49, 50 (+73 more)

**Evidence from the expected pages:**

> **[Equinor p.74]** ...nd set out key decarbonisation and transition 
ambitions. This section provides an overview of the 
progress achieved so far.
Continued leadership in upstream carbon 
efficiency
In 2025 absolute scope 1+2 operated greenhouse 
gas emissions were the same as in 2024, with a total 
of 10.1 million tonnes CO2e. This equates to a 34% 
reduction from our 2015 baseline13, progressing 
toward our 2030 ambition of a 50% net reduction. 
Reductions in emissions were achieved by 
electrification projects and energy efficiency...

> **[Equinor p.74]** low carbon solutions in 
2025 was USD 2.9 billion, compared to USD 2.2 billion 
in 2024. The main contributor was the Empire Wind 
project with additional contributions to equity 
accounted investments including Dogger Bank, Bałtyk 
2 & 3 and our onshore renewables portfolio. If 
financial investments in Ørsted are included, total 
investmen...

**Verdict:** `KEEP` / `FIX: ` / `DROP`

---

### Q22. How many employees did the Equinor Group have in 2025?

**Draft answer:** 24,620 employees in total (24,140 permanent).

**Expected source:** Equinor pp. 138, 139, 17

**Where these figures actually appear in the document:**

- `24,140` in Equinor: pp. 138, 139, 140
- `24,620` in Equinor: pp. 138

**Evidence from the expected pages:**

> **[Equinor p.138]** ...rimary source system.
Number of Equinor Group employees by employment type
2025 Male Female Not disclosed Total
Number of all employees (Headcount) 16,552 7,996 72 24,620
Number of permanent employees including part time 
employees (Headcount) 16,270 7,798 72 24,140
Number of temporary employees (Headcount) 282 198 0 480
Number of non-guaranteed hours employees (Headcount) 0 0 0 0
Number of permanent, full-time employees (Headcount) 16,064 7,409 72 23,545
Number of permanent, part-time employees (Headcount) 206 389...

> **[Equinor p.139]** ...EA only.
Number of permanent employees by country
Country Unit 2025 20242
Brazil Headcount 734 1,034
Norway Headcount 21,161 21,426
UK Headcount 629 934
USA Headcount 576 660
Other countries1 Headcount 1,040 1,101
Total number of permanent employees Headcount 24,140 25,155
Methodologies: Sourced from SAP HR. 
1) Other countries Include Algeria, Angola, Argentina, Australia, Belgium, Canada, Denmark, Germany, India, Japan, Libya, 
Netherlands, Poland, Russian Federation, Singapore, South Korea, Tanzania. 
2) The 202...

> **[Equinor p.17]** 1.5 Our business
Equinor employs around 
24,600 employees in more 
than 20 countries.
17 1.5 Our business INTRODUCTION CONTENTS ABOUT US
OUR 
PERFORMANCE
SUSTAINABILITY 
STATEMENT
FINANCIAL 
STATEMENTS
ADDITIONAL 
INFORMATION
Equinor 2025 Annual report
KEY ACTIVITIES
E&P = Exploration and production
REN = Renewable
M&T = Marketing & trading
R&P = Refining & processing
LC = Low carbon 
OPERATOR OF ASSETS
Brazil E&P REN M&T
Norway E&P REN M&T R&P LC
Poland REN
UK E&P REN M&T LC
USA E&P REN M&T
The overview includes p...

**Verdict:** `KEEP` / `FIX: ` / `DROP`

---

### Q23. What was DNB's total income in 2025?

**Draft answer:** NOK 90,649 million, an all-time high, up 4.8 per cent from 2024.

**Expected source:** DNB pp. 52

**Where these figures actually appear in the document:**

- `90,649` in DNB: pp. 8, 103, 192, 208, 216
- `2024` in DNB: pp. 2, 6, 7, 8, 9, 13, 17, 18 (+196 more)
- `4.8` in DNB: pp. 9, 20, 52, 100, 126, 129

**Evidence from the expected pages:**

> **[DNB p.52]** ...s on three main 
ambitions: the customer chooses us, we deliver sustainable 
value creation and we find the solutions together. Read 
more about the Group’s strategy in the sub-chapter 
Strategy.
Operations in 2025
DNB’s total income rose by 4.8 per cent from 2024 to an 
all-time high level of NOK 90 649 million in 2025, but there 
was a decline in profit due to higher costs, impairment of 
financial instruments and tax expenses. Profit for the year 
amounted to NOK 43 586 million, down NOK 2 218 million, 
or 4.8 p...

**Verdict:** `KEEP` / `FIX: ` / `DROP`

---

### Q24. What were DNB's earnings per share in 2025?

**Draft answer:** NOK 28.45, down from NOK 29.34 in 2024.

**Expected source:** DNB pp. 52

**Where these figures actually appear in the document:**

- `29.34` in DNB: pp. 9, 52, 124, 208, 292
- `28.45` in DNB: pp. 9, 52, 208, 292, 315
- `2024` in DNB: pp. 2, 6, 7, 8, 9, 13, 17, 18 (+196 more)

**Evidence from the expected pages:**

> **[DNB p.52]** ...ofit for the year 
amounted to NOK 43 586 million, down NOK 2 218 million, 
or 4.8 per cent, from 2024. Return on equity was 
15.9 per cent in 2025, compared with 17.5 per cent in the 
year-earlier period, and earnings per share were NOK 28.45, 
down from NOK 29.34 in 2024. 
Net interest income increased by NOK 541 million, mainly 
due to positive effects from growth in lending and deposit 
volumes. There was an average increase in performing loans 
of 4.5 per cent from 2024, and a 4.1 per cent increase in 
average...

**Verdict:** `KEEP` / `FIX: ` / `DROP`

---

### Q25. What was DNB's leverage ratio at the end of 2025?

**Draft answer:** 6.6 per cent, down from 6.9 per cent in 2024.

**Expected source:** DNB pp. 55

**Where these figures actually appear in the document:**

- `2024` in DNB: pp. 2, 6, 7, 8, 9, 13, 17, 18 (+196 more)
- `6.9` in DNB: pp. 6, 7, 9, 18, 19, 55, 158, 217 (+1 more)
- `6.6` in DNB: pp. 7, 9, 55, 67, 217

**Evidence from the expected pages:**

> **[DNB p.55]** ...from the supervisory authorities was 
16.3 per cent, including Pillar 2 Guidance. The Group’s 
CET1 capital ratio was thus 1.6 percentage point above the 
supervisory authorities’ expectation. 
The risk exposure amount (REA) increased by NOK 50 billion 
from 2024, to NOK 1 171 billion at year-end 2025. Of 
this, NOK 32 billion was due to operational risk, driven by 
the increase in the Group’s total income in recent years, 
including the effects of the Carnegie acquisition. Total REA 
for credit risk increased by...

**Verdict:** `KEEP` / `FIX: ` / `DROP`

---

### Q26. How many personal and corporate customers did DNB have at the end of 2025?

**Draft answer:** About 2.4 million personal customers and 240,000 corporate customers.

**Expected source:** DNB pp. 74

**Where these figures actually appear in the document:**

- `240,000` in DNB: pp. 14
- `2.4` in DNB: pp. 11, 14, 19, 37, 55, 57, 74, 103 (+8 more)

**Evidence from the expected pages:**

> **[DNB p.74]** ...ge international companies. This includes mortgages 
and corporate loans, savings and investment solutions, and 
payment solutions, through the mobile banking app, the online 
bank, customer service centres and bank offices. At the end 
of 2025, DNB had about 2.4 million personal customers and 
240 000 corporate customers. 
Norway is the Group’s main market, and the loan portfolio 
largely reflects the Norwegian economy. In addition, the 
Group has a strong position in the Nordic region and an 
international presen...

> **[DNB p.74]** customers and investments 
from shareholders. Technology and data are obtained and 
developed through collaboration with technology partners 
and in internal innovation projects. Human resources are 
recruited and developed using comprehensive training 
programmes and career development opportunities. Another 
input factor that is required to conduct operations is energy, 
water and commodities needed to operate office premises. 
The Group’s operating income comes mainly from net interest 
income and fees and commi...

**Verdict:** `KEEP` / `FIX: ` / `DROP`

---

### Q27. How much goodwill did DNB recognise from the Carnegie acquisition?

**Draft answer:** NOK 8,579 million, comprising expected synergies, assembled workforce and deferred tax on excess values.

**Expected source:** DNB pp. 214

**Where these figures actually appear in the document:**

- `8,579` in DNB: pp. 214

**Evidence from the expected pages:**

> **[DNB p.214]** ...s     293 
Other non-financial assets     4 759 
Total assets      20 786 
Liabilities        
Deposits from customers      11 850 
Other liabilities      3 068 
Total liabilities      14 918 
       
Net identifiable assets acquired      5 869 
Goodwill      8 579 
Total consideration for 100 per cent of shares, settled in cash     14 447 
 
DNB has identified intangible assets and accounted for these separately in the final purchase price allocation. These comprise NOK 644 million 
relating to trademarks, NOK 1 4...

> **[DNB p.214]** be carried out over a period of 7 to 15 years. The brand name is considered to have an indefinite useful life. 
 
The goodwill of NOK 8 579 million comprises the value of expected synergies arising from the acquisition, assembled workforce and deferred 
tax on excess values. The goodwill amount is not expected to be deductible for income tax purposes.   
 
DNB used external advisers in the p...

**Verdict:** `KEEP` / `FIX: ` / `DROP`

---

### Q28. What was Hydro's net debt at the end of 2025?

**Draft answer:** NOK 9.7 billion, down from NOK 16.0 billion at the end of 2024.

**Expected source:** Hydro pp. 35

**Where these figures actually appear in the document:**

- `2024` in Hydro: pp. 3, 5, 6, 15, 21, 23, 26, 27 (+141 more)
- `16.0` in Hydro: pp. 35, 238
- `9.7` in Hydro: pp. 3, 34, 35, 237, 257

**Evidence from the expected pages:**

> **[Hydro p.35]** ...of NOK 3.0 per share. The final shareholder 
distribution for 2025 is subject to approval by the Annual General Meeting on 
May 7, 2026.
Net debt1
Hydro’s net debt was NOK 9.7 billion at the end of 2025, compared to net debt 
of NOK 16.0 billion at the end of 2024. The net debt decrease was mainly 
driven by a positive free cash flow, partially offset by shareholder distributions 
and new lease. 
Adjusted net debt1
Hydro’s adjusted net debt was NOK 18.2 billion at the end of 2025, compared 
to NOK 24.1 billion at t...

**Verdict:** `KEEP` / `FIX: ` / `DROP`

---

### Q29. How much alumina did Hydro produce in 2025?

**Draft answer:** 5,458 thousand tonnes, up from 5,359 thousand tonnes in 2024.

**Expected source:** Hydro pp. 256

**Where these figures actually appear in the document:**

- `5,359` in Hydro: pp. 256
- `5,458` in Hydro: pp. 256
- `2024` in Hydro: pp. 3, 5, 6, 15, 21, 23, 26, 27 (+141 more)

**Evidence from the expected pages:**

> **[Hydro p.256]** ...luding output from casting of 
extrusion ingot production in the Extrusions business area.
Reference: ESRS E5-5.
Production volumes
thousand tonnes 2025 2024 2023 2022 2021
Bauxite production  10 496  10 506  10 897  11 012  10 926 
Alumina production  5 458  5 359  5 626  5 586  5 894 
Primary aluminium production  1 556  1 527  1 536  1 636  1 688 
    Hydro REDUXA  470  418  349  421 
Recycling casthouse production  1 895  1 751  1 787  1 664 
    Hydro CIRCAL  58  57  51  50 
Extruded products  1 013  1 024 111...

> **[Hydro p.256]** . Changing methodologies over time 
also creates challenges in comparing consolidated waste data from one year to another. 
Waste treatment operations can occur both onsite and offsite treatment. In many cases, waste is managed by third 
parties, which are required to adhere to the Hydro Supplier Code of Conduct
. All Hydro locations are required to 
ensure safe transport of hazardous waste in accordance with global and local regulations, and evaluate critical waste 
receivers and include these in a supplier develo...

**Verdict:** `KEEP` / `FIX: ` / `DROP`

---

### Q30. What was Hydro's share price at the end of 2025?

**Draft answer:** NOK 78.20 at year-end 2025 on the Oslo Stock Exchange.

**Expected source:** Hydro pp. 64, 65

**Where these figures actually appear in the document:**

- `78.20` in Hydro: pp. 65, 152
- `2025` in Hydro: pp. 1, 2, 3, 4, 5, 6, 7, 8 (+284 more)

**Evidence from the expected pages:**

> **[Hydro p.64]** The Hydro share
Introduction
Hydro’s share price closed at NOK 78.2 at the end of 2025. The return ex. 
dividend1 for 2025 was a positive NOK 14.8 or a positive 23.3 percent. Hydro 
paid its 2024 dividend of 2.25 NOK per share in May 2025. No new share 
buyback program was approved during the year. The share buyback program 
initiated in Se...

> **[Hydro p.64]** share 
price for the year.
2 Total shareholder return includes the opening share price, dividends and closing share price.
3 TSR calculated including reinvesting dividends. Hydro and all peers shown in same currency 
(USD).
4 Peer group includes Nalco, Rusal, Alcoa, Century Aluminium, Hindalco, Chalco, Grupa Kety, 
Constellium, Kaiser, ProfilGruppen, Tredegar Corporation. Source: Refinitiv retrieves.

> **[Hydro p.65]** ...5  2024  2023  2022  2021 
Share price high, Oslo (NOK)1  79.12  75.10  84.04  89.95  71.46 
Share price low, Oslo (NOK)1  50.60  53.24  56.63  51.49  36.99 
Share price average, Oslo (NOK)  64.59  64.26  68.85  69.34  55.94 
Share price year-end, Oslo (NOK)  78.20  62.54  68.40  73.32  69.52 
Earnings per share from continuing operations  3.41  2.90  1.77  11.76  5.92 
Adjusted earnings per share from continuing operations2  5.02  4.50  4.26  10.70  6.77 
Dividend per share (NOK)3, 6  3.00  2.25  2.50  5.65  6.85...

> **[Hydro p.65]** price high and low based on intraday, not only closing price.
2 Alternative performance measures (APMs) are described in the appendices.
3 2025 dividend per share proposed by Board of Directors, dependent on approval from the Annual General Meeting May 7, 2026.
4 Dividend per share divided by adjusted earnings per share from continuing operations.
5 Average dividend per share divided by average a...

**Verdict:** `KEEP` / `FIX: ` / `DROP`

---

## Part 2: unanswerable questions (10)

For these the correct behaviour is abstention. Confirm the documents really do not answer them. The keyword scan below shows the closest passages, so you can catch a question that is in fact answerable.

### Q31. What profit guidance has DNB issued for 2027?

**Expected behaviour:** abstain.

**Keywords scanned:** profit, guidance, issued

**Scan restricted to:** DNB

**Closest passages found:**

> **[DNB p.54, 2/3 keywords]** primarily be attributed to specific customers in connection 
with restructuring.
Tax
The DNB Group’s tax expense for the full year 2025 was 
NOK 9 894 million, or 18.5 per cent of the pre-tax operating 
profit. 
The tax expense was affected by increased deductions of 
debt interest in operations outside Norway and an increase 
in tax-exempt income, as well as higher non-deductible 
expenses, compared with the forecast for the year.
Funding, liquidity and balance sheet 
The Group’s short-term funding programmes are...

> **[DNB p.55, 2/3 keywords]** The Group’s CET1 capital decreased by NOK 7.6 billion to 
NOK 209.7 billion at year-end 2025. Retained earnings 
contributed positively by NOK 13.4 billion, and dividends 
from DNB Livsforsikring increased the CET1 capital by 
NOK 3.0 billion. The acquisition of Carnegie reduced the 
CET1 capital by NOK 10.9 billion, while three share buy-
back programmes totalling 2.5 per cent contributed further 
to the reduction in CET1 capital.
DNB’s strong capital position provides a firm foundation for 
continued delivery on...

> **[DNB p.115, 2/3 keywords]** this, it is important to enable emissions reductions and not use 
carbon credits in the short term. However, DNB acknowledges 
that it will be more difficult to eliminate emissions from some 
activities in the long term, and that carbon credits are a 
possible solution for these residual emissions.
Metrics and targets 
Targets and tracking
ESRS E1-4 Targets related to climate change mitigation and 
adaptation
The targets that have been set for the climate are closely 
linked to the Group’s strategy and sustainabili...

**Verdict:** `KEEP` (genuinely unanswerable) / `DROP` / `MOVE TO ANSWERABLE: `

---

### Q32. What was Hydro's total revenue in 2010?

**Expected behaviour:** abstain.

**Keywords scanned:** Hydro's, total, revenue

**Scan restricted to:** Hydro

**Closest passages found:**

> **[Hydro p.169, 3/3 keywords]** Hydro’s associates
The following associate is considered material for Hydro:
Lyse Kraft DA, a power producer headquartered in Stavanger, operates power plants in the southwest of Norway and 
holds ownership interests in two arrangements in nearby areas. Hydro owns 25.6 percent of the company, while Lyse AS 
holds a controlling ownership share of 74.4 percent. 
The annual production of Lyse Kraft DA amounts to about 9.5 TWh, which is contributed in kind to the owners 
corresponding to ownership sha
re. The owners ar...

> **[Hydro p.174, 3/3 keywords]** Section 5 - Income and expenses
Note 5.1   Revenue from contracts with customers
§ Accounting policies for revenue recognition
Hydro accounts for revenue in accordance with IFRS 15 Revenue from Contracts with Customers.
IFRS 15 requires us to, for each contract with a customer, identify the performance obligations, determine the 
transaction price, allocate the transaction price to performance obligations to the extent the contract covers more than 
one performance obligation, determine whether revenue should be re...

> **[Hydro p.193, 3/3 keywords]** Gains and losses
Realized and unrealized gains and losses from financial instruments and contracts accounted for as financial instruments are included in several line items in the income statement. Below is a reconciliation of the effects from Hydro's financial instruments 
in the income statements:
Amounts in NOK million
Derivatives at 
FVTPL
Derivatives 
identified as 
hedging 
instruments
Debt 
instruments at 
amortized cost
Financial 
instruments at 
FVTPL
Equity 
instruments at 
FVOCI
Financial 
liabilities at...

**Verdict:** `KEEP` (genuinely unanswerable) / `DROP` / `MOVE TO ANSWERABLE: `

---

### Q33. Who is the chief executive officer of Telenor?

**Expected behaviour:** abstain.

**Keywords scanned:** chief, executive, officer, Telenor

**Closest passages found:**

> **[DNB p.34, 4/4 keywords]** The Board of Directors of DNB Bank ASA
As at 10 March 2026
The Board of Directors is the Group’s supreme governing body. Through 
the Group Chief Executive Officer (CEO), the Board is responsible for 
ensuring a sound organisation of the business activities. The Board has 
three sub-committees: the Risk Management Committee, the Audit 
Committee and the Compensation and Organisation Committee.  
Olaug Svarva  
Born 1957 | Woman | Norwegian
Role on the Board: Chair of the 
Board of Directors of DNB since 
2018. Chai...

> **[DNB p.35, 4/4 keywords]** Petter-Børre Furberg 
Born 1967 | Man | Norwegian
Role on the Board: Member of 
the Board of DNB since 2023. 
Member of the Compensation 
and Organisation Committee.
Other key roles: CEO of 
Posten Bring since 2024 and 
member of the Board of the 
Employers’ Association Spekter 
since 2024.
Background: Master’s degree 
in Economics and Business 
Administration (Siviløkonom) 
from NHH Norwegian School 
of Economics and Authorised 
Financial Analyst (AFA) and 
Certified European Financial 
Analyst (CEFA). Member of...

> **[Equinor p.25, 3/4 keywords]** 1.7 Governance and risk management
Corporate governance
Our corporate governance framework is designed to 
ensure transparency and accountability in both 
decision-making and daily operations. Good 
corporate governance is essential for building a 
sound and sustainable company and for ensuring that 
we run our business in a justifiable and profitable 
manner for the benefit of employees, shareholders, 
partners, customers and society.
As a public limited liability company with shares listed 
in Oslo and New York,...

**Verdict:** `KEEP` (genuinely unanswerable) / `DROP` / `MOVE TO ANSWERABLE: `

---

### Q34. How many employees did Equinor have in China at the end of 2025?

**Expected behaviour:** abstain.

**Keywords scanned:** employees, Equinor, have, China

**Scan restricted to:** Equinor

**Closest passages found:**

> **[Equinor p.7, 2/3 keywords]** Our power business continued to expand, delivering 
5.65 TWh of production, including a 25% increase in 
renewable power generation.
Despite lower commodity prices than expected, we 
report strong cash flow, an industry-leading return on 
average capital employed* of 14.5% and USD 9 billion 
in capital distribution.
Strategic progress across the portfolio
We continued to allocate capital to areas where 
Equinor can create the most value: the NCS, focused 
international oil and gas growth, and building an 
integrate...

> **[Equinor p.7, 2/3 keywords]** . We will continue to 
prioritise competitive shareholder distribution 
supported by long-term value creation.
Everyone that goes to work for Equinor every day, as 
employees or suppliers, plays an important role in 
producing energy the world needs and our customers 
want, in a safe manner. We can be proud of 
everything we have achieved together in 2025, and 
we want to thank everyone for their important 
contributions throughout 2025. 
To our shareholders – thank you for your continued 
trust and support.
Jon Er...

> **[Equinor p.14, 2/3 keywords]** 1.3 The world in which we operate
Equinor is a trusted energy provider in a 
challenging market and uncertain world. We 
remain committed to long-term value creation 
while being a secure and reliable energy 
provider. 
We operate in a world where geopolitical uncertainty and shifting 
priorities impact the energy industry. As globalism and protectionism 
shape trade and countries balance energy security, affordability and 
climate goals, we remain focused on being a reliable energy provider 
and adapting to these...

**Verdict:** `KEEP` (genuinely unanswerable) / `DROP` / `MOVE TO ANSWERABLE: `

---

### Q35. What was DNB's market share of mortgage lending in Sweden in 2025?

**Expected behaviour:** abstain.

**Keywords scanned:** DNB's, market, share, mortgage, lending

**Scan restricted to:** DNB

**Closest passages found:**

> **[DNB p.23, 4/5 keywords]** Market shares in Norway 
Personal customer market
Loans from financial 
institutions
22%
Deposits
28%
Mortgages
24%
Corporate customer market
Loans from financial 
institutions
23%
Deposits
33%
 DNB's market share
Source: Statistics Norway
Contents
23
DNB Group Annual report 2025
> Strategy and governance > Strategy

> **[DNB p.25, 4/5 keywords]** Our international operations contribute significantly to 
DNB’s income. Our global presence enables us to support 
our customers in reaching international markets and 
accessing capital. In addition, our international presence 
gives us a flexible platform for growth, where we build a 
deeper understanding of industries and attract new talent 
through our international network. The Nordics are an 
important market for the corporate customers segment, one 
in which we have achieved attractive and profitable organic...

**Verdict:** `KEEP` (genuinely unanswerable) / `DROP` / `MOVE TO ANSWERABLE: `

---

### Q36. What dividend per share did Equinor pay for fiscal year 2015?

**Expected behaviour:** abstain.

**Keywords scanned:** dividend, share, Equinor, fiscal, year

**Scan restricted to:** Equinor

**Closest passages found:**

> **[Equinor p.14, 3/4 keywords]** 1.3 The world in which we operate
Equinor is a trusted energy provider in a 
challenging market and uncertain world. We 
remain committed to long-term value creation 
while being a secure and reliable energy 
provider. 
We operate in a world where geopolitical uncertainty and shifting 
priorities impact the energy industry. As globalism and protectionism 
shape trade and countries balance energy security, affordability and 
climate goals, we remain focused on being a reliable energy provider 
and adapting to these...

> **[Equinor p.54, 3/4 keywords]** Financial framework 
Equinor’s financial framework is underpinned by key principles that support value creation for shareholders.
54 2.2 Financial performance INTRODUCTION CONTENTS ABOUT US
OUR 
PERFORMANCE
SUSTAINABILITY 
STATEMENT
FINANCIAL 
STATEMENTS
ADDITIONAL 
INFORMATION
Equinor 2025 Annual report
Competitive, growing 
ordinary cash dividend 
through the cycles
I n v e s t i n g  i n  h i g h - v a l u e  p r o j e c t s  i s  e x p e c t e d  t o  
enable Equinor to maintain a competitive 
capital distribut...

> **[Equinor p.66, 3/4 keywords]** Review of cash flows 
Solid financial results from the business during 2025, 
driven by a strong operational performance, 
generated cash flow provided by operating activities 
b e f o r e  t a x e s  p a i d  a n d  w o r k i n g - c a p i t a l  i t e m s  o f  USD 
38,439 million. This represents a slight increase of 
USD 601 million from the previous year despite lower 
liquids prices in 2025.
Taxes paid of USD 20,460 million remained stable 
compared to the previous year outflow of USD 
20,592 million. The pay...

**Verdict:** `KEEP` (genuinely unanswerable) / `DROP` / `MOVE TO ANSWERABLE: `

---

### Q37. What were Equinor's proved oil and gas reserves at year-end 2015?

**Expected behaviour:** abstain.

**Keywords scanned:** Equinor's, proved, reserves, year-end

**Scan restricted to:** Equinor

**Closest passages found:**

> **[Equinor p.210, 3/4 keywords]** The estimated useful lives of property, plant and 
equipment are reviewed on an annual basis, and 
changes in useful lives are accounted for 
prospectively. An item of property, plant and 
equipment is derecognised upon disposal. Any gain or 
loss arising on derecognition of the asset is included in 
Other income or Operating expenses, respectively, in 
the period the item is derecognised.
Monetary or non-monetary grants from 
governments, when related to property, plant and 
equipment and considered reasonably cer...

> **[Equinor p.210, 3/4 keywords]** specific 
circumstances justify a longer time horizon. Specific 
circumstances are for instance fields which have 
large up-front investments in offshore infrastructure, 
such as many fields on the NCS, where drilling of wells 
is scheduled to continue for much longer than five 
years. For unconventional reservoirs where continued 
drilling of new wells is a major part of the investments, 
such as the US onshore assets, the proved reserves 
are always limited to proved well locations scheduled 
to be drilled within...

> **[Equinor p.217, 3/4 keywords]** Measurement
The recoverable amount applied in Equinor’s 
impairment assessments is normally estimated value 
in use. Equinor may also apply the assets’ fair value 
less cost of disposal as the recoverable amount when 
such a value is available, reasonably reliable, and 
based on a recent and comparable transactions.
Value in use is determined using a discounted cash 
flow model. The estimated future cash flows are 
based on Equinor’s most recently approved forecasts 
by management, which are based on reasonable and...

**Verdict:** `KEEP` (genuinely unanswerable) / `DROP` / `MOVE TO ANSWERABLE: `

---

### Q38. What was the closing price of Brent crude oil on 31 December 2025?

**Expected behaviour:** abstain.

**Keywords scanned:** closing, price, Brent, crude, December

**Closest passages found:**

> **[Equinor p.189, 4/5 keywords]** commodity price 
risk portfolio. To manage short-term commodity risk, 
Equinor enters into commodity-based derivative 
contracts, including futures, options, over-the-counter 
(OTC) forward contracts, market swaps and 
contracts for differences related to crude oil, 
petroleum products, natural gas, power and 
emissions. Equinor’s bilateral gas sales portfolio is 
exposed to various price indices with a combination 
of gas price markers. The term of crude oil and 
refined oil products derivatives are usually less t...

**Verdict:** `KEEP` (genuinely unanswerable) / `DROP` / `MOVE TO ANSWERABLE: `

---

### Q39. How many users does Hydro's mobile banking app have?

**Expected behaviour:** abstain.

**Keywords scanned:** users, Hydro's, mobile, banking, have

**Scan restricted to:** Hydro

No passage matched enough keywords. Nothing in the documents appears to answer this.

**Verdict:** `KEEP` (genuinely unanswerable) / `DROP` / `MOVE TO ANSWERABLE: `

---

### Q40. What CET1 capital ratio did Nordea report for 2025?

**Expected behaviour:** abstain.

**Keywords scanned:** capital, ratio, Nordea, report

**Closest passages found:**

> **[DNB p.18, 4/4 keywords]** The share
The total return on the DNB share, including reinvested dividends,  
was 30.6 per cent in 2025. 
In DNB, our overall objective is to create long-term value for our owners, partly through a positive 
development in the share price and partly through a predictable dividend policy. 
At the end of 2025, DNB was the second largest listed company on Oslo Børs (the Oslo Stock Exchange), 
with a market capitalisation of NOK 411 billion. For more information on the DNB share, see ir.dnb.no.  
2025 2024
Total retur...

> **[DNB p.341, 4/4 keywords]** Note P45 Largest shareholders
346   /   DNB GROUP – ANNUAL REPORT 2025 
Note P45 Largest shareholders 
Shareholder structure in DNB Bank ASA as at 31 December 2025 
Shares  Ownership in  
in 1 000  per cent  
Norwegian Government/Ministry of Trade, Industry and Fisheries  502 386 34.4  
DNB Savings Bank Foundation 130 001 8.9  
Folketrygdfondet 95 106 6.5  
BlackRock, Inc. 64 497 4.4  
Vanguard Group Holdings 37 106 2.5  
Deutsche Bank AG Group 34 257 2.3  
DNB Asset Management AS 24 477 1.7  
Storebrand Kapitalfor...

> **[Equinor p.4, 3/4 keywords]** Key figures
4 Key figures INTRODUCTION CONTENTS ABOUT US
OUR 
PERFORMANCE
SUSTAINABILITY 
STATEMENT
FINANCIAL 
STATEMENTS
ADDITIONAL 
INFORMATION
Equinor 2025 Annual report
Operational
2,137
MBOE/D
Equity oil & gas production 
per day in 2025
48%
RRR
Oil & gas reserves 
replacement ratio for 2025
5.65
TWh
Total power generation, 
Equinor share in 2025
3.67
TWh
Renewable power generation, 
Equinor share in 2025
More key figures in 2.1 Operational 
performance
Financial
27.6
USD BILLION
Adjusted operating 
income*
18...

**Verdict:** `KEEP` (genuinely unanswerable) / `DROP` / `MOVE TO ANSWERABLE: `

---
