# Where Massachusetts Attorney General settlement money goes

When the Massachusetts Attorney General announces a settlement, the announcement says what it was worth. It rarely says where each dollar went afterward. This repository collects what the public record does say, with a source for every figure, and lists the records that would answer the rest.

**Status: preliminary.** Built on 2026-10-12 from public sources by reading, not from any insider data. Every dollar amount in the registers carries a verbatim quote from the document it came from, and the quotes and amounts were checked by script. The readings were made by a model and were not checked against the underlying settlement documents, except where a finding says so. A completeness audit followed the first sweep and changed the headline; [`findings/05-completeness-audit.md`](findings/05-completeness-audit.md) records how. Errors and corrections are welcome.

**Dashboard:** https://duncanburns2013-dot.github.io/ma-ag-settlement-flows/ (built from the registers in `data/`)

**Browse the data:** [all registers (`data/`)](https://github.com/duncanburns2013-dot/ma-ag-settlement-flows/tree/main/data) · [completeness audit](findings/05-completeness-audit.md) · [public records requests](PUBLIC-RECORDS-REQUESTS.md) · repository: https://github.com/duncanburns2013-dot/ma-ag-settlement-flows

## What it found
- **Where the announced money goes.** Of 478 single-state settlements with a stated total, announced 2015 to 2026 ($2.05 billion), the releases give a dollar destination for 68% of the dollars: 11.3% to the harmed, 40.4% to the Commonwealth (7.8% called penalties, fines, fees or costs; 32.6% paid to the Commonwealth with no stated purpose), 4.5% to state agencies recovering their own losses, 6.9% to designated programs and 4.9% non-cash relief. The other 32.0% comes as a total with no split. One settlement, a $600 million tobacco payment to the General Fund, is 29% of the total and 90% of the "no stated purpose" money; without it, 15.9% goes to the harmed and 45.3% has no split. The full breakdown, with and without that payment and for the 198 settlements whose stated amounts add up to the total, is in the [audit note](findings/05-completeness-audit.md#where-the-money-goes-as-the-releases-state-it). A stated destination is what the release says, not proof of what was delivered. [Inside the 11.3% to the harmed](findings/06-to-the-harmed.md): only 3.3% of those dollars is described as already paid or credited, and for 62.6% the release does not say how it reaches people.
- **Settlement by settlement.** 56% of the 478 state a dollar amount for at least one destination, and 42% give amounts that add up to the total. Totals of $1 million and over (143 settlements, $1.94 billion) are 31% no split; totals under $1 million (335 settlements, $104 million) are 52% no split.
- **Often the Attorney General decides.** In 34 settlement rows (from 170 readable settlement documents), the document gives the Attorney General sole discretion over allocation, among consumers, the General Fund, the Local Consumer Aid Fund and consumer-protection programs, with no amount committed to consumers; 19 more give discretion over part of the money. The count is a floor, because scanned documents were read by OCR. The Local Consumer Aid Fund shows $95 under its own name in the state's spending data.
- **Settlement money funds the office's own grant programs and part of its budget.** 75 grant announcements name 513 organizations, most with no amount stated per grantee; 280 of the 513 have employee donations, lobbying or an official's disclosed tie on record by exact name. Separately, $46 million of the $620 million the Comptroller's data records for the office since fiscal 2015 came from retained-revenue lines (False Claims, civil penalties). [Grantees and ties](data/grantees-political-money-ties.tsv).
- **Multistate settlements**: Massachusetts's stated share of 96 distinct matters is $1.97 billion, counted at stated maximums: 55% opioid abatement, 29% mixed (mostly the Meta settlement), 5% state agencies, 4% no stated use, 3% paid to the Commonwealth, 3% restitution to consumers. [Details](findings/04-multistate-and-opioid.md).
- **State accounts and who is paid from them**: the Attorney General's trust accounts, the opioid fund and a mortgage settlement trust paid $230 million to 1,078 payees. Payments to 47 payees whose names look like individuals are listed in [`data/payments-to-individuals.tsv`](data/payments-to-individuals.tsv) with CTHRU's expense category and account for each (70% of the dollars are coded consultant services; about 30% come from trust lines not named for a settlement). The data does not record the case or service, and a name there is not evidence of anything about a payment.

## What it could not find
Whether the discretionary money reached consumers. That needs the office's own accounting, which the public record does not hold. [`PUBLIC-RECORDS-REQUESTS.md`](PUBLIC-RECORDS-REQUESTS.md) lists ten requests, each tied to the dataset that raises the question.

## Contents
- `findings/`: six notes in order (scoping, first pass, single-state sweep, multistate and opioid, completeness audit, to the harmed). Note 03 covers the first sweep only and is superseded by note 05.
- `docs/index.html`: a single-page dashboard of the combined record, built from the registers by `method/build_dashboard_data.py`; it works opened from disk.
- `data/`: the registers, tab-separated. Each row links to its source.
  - `single-state-settlements-destinations.tsv`: the first sweep's 143 releases, what each says about where the money goes, with quotes.
  - `audit-releases-read.tsv`: the 668 releases the audit read, same layout plus multistate fields and a status column.
  - `criminal-cases-flagged.tsv`: counted rows that are criminal cases.
  - `harmed-money-classified.tsv`: the 91 settlements with money stated to the harmed, classified by two readers from the release text: what the money is, who receives it, whether it was paid or only ordered or expected, and whether the release says how it reaches people.
  - `multistate-ma-share.tsv`: 259 releases and Massachusetts's stated share; 131 are single-state matters, tagged with the audit row that counts them.
  - `settlement-documents-discretion-clauses.tsv`, `settlement-documents-discretion-clauses-pass2.tsv`: the allocation clauses as read.
  - `ag-grant-programs-and-grantees.tsv`, `ag-grant-announcements-list.tsv`: the grant programs and grantees.
  - `state-fund-payees-cthru.tsv`, `payments-to-individuals.tsv`: who the state's settlement accounts paid.
  - `ag-spending-by-appropriation-type-fy2015-2027.tsv`, `ag-retained-revenue-and-trust-lines-fy2015-2027.tsv`, `ag-retained-revenue-share-by-fiscal-year.tsv`: the office's own spending by funding line.
  - `grantees-political-money-ties.tsv`, `state-fund-recipients-political-money-ties.tsv`: employee donations, lobbying and officials' disclosures matched by exact name.
  - `blind-reread-comparison.tsv`: a second reader's independent reading of 45 random releases, against the first.
  - `ag-news-archive-2015-2026.tsv`: the 2,863 Attorney General releases swept; `releases-missing-from-live-listing.tsv`: 84 more found on the Internet Archive.
- `method/`: the scripts used. `cthru.py` and `payees.py` query the Comptroller's open data and run as they are. `ties.py` and the scripts that import it read donation, lobbying and disclosure tables and matcher modules that are not published here, so read them as documentation of the method. `summary_numbers.py` reprints the headline shares from the built data.

## Sources
The Attorney General's press releases and linked settlement documents on mass.gov; the Internet Archive's copies of releases the live archive lacks; the Comptroller's CTHRU spending data; Office of Campaign and Political Finance and Federal Election Commission contribution files; Secretary of the Commonwealth lobbying disclosures; State Ethics Commission Statements of Financial Interest. Donation matches count confirmed employer matches only. Lobbying is what the organization paid lobbying firms or its own lobbyists, as filed.

## Limits
- Announcements state what a settlement is worth, not what was collected or delivered. Settlements the office never announced are not in the record, and this repository found no public count of the office's total settlements.
- The sweep covers the Attorney General's mass.gov archive from January 2015 to October 2026; earlier releases are not included. The archive listing lacks at least 67 releases (61 from September 2017 to March 2018); those were recovered where the Internet Archive had them. Releases outside both are unread. Settlements under $100,000 were not systematically searched for.
- Some counted rows are criminal cases (35 with totals, $25 million), administrative citations (40, $15 million) or merger approval agreements (4, $129 million). The dashboard tags them and offers toggles. Eight totals come from release titles alone.
- Matching a recipient to political money is by exact normalized name; two organizations with the same name would be confused. A tie is a record that exists, not a finding about any recipient.
- A 45-release second reading matched the first on 64 of the 66 amounts both readers recorded, but one reader left 10 of 36 category amounts unrecorded; the audit note gives the detail.
