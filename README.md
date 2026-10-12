# Where Massachusetts Attorney General settlement money goes

When the Massachusetts Attorney General announces a settlement, the announcement says what it was worth. It rarely says where each dollar went afterward. This repository collects what the public record does say, with a source for every figure, and lists the records that would answer the rest.

**Status: preliminary.** Built on 2026-10-12 from public sources by reading, not from any insider data. Every dollar amount in the registers carries a verbatim quote from the document it came from, and the quotes and amounts were checked by script. The readings were made by a model and were not checked against the underlying settlement documents. Errors and corrections are welcome; see the limits in each finding.

## What it found
- **Most settlement dollars have no stated destination.** Of 100 single-state settlements of $1 million or more announced from 2015 to 2026 ($755 million), the announcement says where $225 million (30%) goes: 16% to the harmed, 7% to the state as penalties and costs, 5.5% to state agencies recovering their own losses, 1.4% to designated programs. The other 70% comes as a total with no split. [Details](findings/03-single-state-sweep.md).
- **Where a split is stated, most of it goes to the harmed**: 56% in the 40 settlements whose stated parts add up to the headline, 20% to the state, 19% to state agencies, 5% to designated programs.
- **Often the Attorney General decides.** In 15 of 43 settlements with a readable settlement document ($281 million headline), the document gives the Attorney General sole discretion over allocation, among consumers, the General Fund, the Local Consumer Aid Fund and consumer-protection programs, with no amount committed to consumers. The Local Consumer Aid Fund shows $95 under its own name in the state's spending data. [Details](findings/02-first-pass.md).
- **Settlement money funds the office's own grant programs**: 24 award announcements, $25.8 million, 305 named organizations, most with no amount stated per grantee. 179 of the 305 have employee donations, lobbying or an official's disclosed tie on record by exact name. [Grantees and ties](data/grantees-political-money-ties.tsv).
- **Multistate settlements**: Massachusetts's stated share of 90 distinct matters is $1.97 billion: 55% opioid abatement, 29% mixed (mostly the Meta settlement), 5% state agencies, 4% no stated use, 3% paid to the Commonwealth, 3% restitution to consumers. [Details](findings/04-multistate-and-opioid.md).
- **State accounts and who is paid from them**: the Attorney General's trust accounts, the opioid fund and a mortgage settlement trust paid $230 million to 1,078 payees. Payments to 47 payees whose names look like individuals are listed with their amounts in [`data/payments-to-individuals.tsv`](data/payments-to-individuals.tsv); the spending data does not say what they were for.

## What it could not find
Whether the discretionary money reached consumers. That needs the office's own accounting, which the public record does not hold. [`PUBLIC-RECORDS-REQUESTS.md`](PUBLIC-RECORDS-REQUESTS.md) lists nine requests, each tied to the dataset that raises the question.

## Contents
- `findings/`: four notes in order (scoping, first pass, single-state sweep, multistate and opioid).
- `data/`: the registers, tab-separated. Each row links to its source.
  - `single-state-settlements-destinations.tsv`: 143 releases, what each says about where the money goes, with quotes.
  - `multistate-ma-share.tsv`: 259 releases and Massachusetts's stated share.
  - `settlement-documents-discretion-clauses.tsv`: the allocation clauses as read.
  - `ag-grant-programs-and-grantees.tsv`, `ag-grant-announcements-list.tsv`: the grant programs and grantees.
  - `state-fund-payees-cthru.tsv`, `payments-to-individuals.tsv`: who the state's settlement accounts paid.
  - `grantees-political-money-ties.tsv`, `state-fund-recipients-political-money-ties.tsv`: employee donations, lobbying and officials' disclosures matched by exact name.
  - `ag-news-archive-2015-2026.tsv`: the 2,863 Attorney General releases swept.
- `method/`: the scripts used. They ran inside a larger project (its donation, lobbying and disclosure tables), so read them as documentation of the method; they do not run on their own.

## Sources
The Attorney General's press releases and linked settlement documents on mass.gov; the Comptroller's CTHRU spending data; Office of Campaign and Political Finance and Federal Election Commission contribution files; Secretary of the Commonwealth lobbying disclosures; State Ethics Commission Statements of Financial Interest. Donation matches count confirmed employer matches only. Lobbying is what the organization paid lobbying firms or its own lobbyists, as filed.

## Limits
- Announcements state what a settlement is worth, not what was collected or delivered.
- The sweep covers the Attorney General's mass.gov archive from January 2015 to October 2026; earlier releases are not included. Single-state settlements are those with a headline of $1 million or more.
- Matching a recipient to political money is by exact normalized name; two organizations with the same name would be confused. A tie is a record that exists, not a finding about any recipient.
- Fourteen scanned settlement documents were not read.
