# Can Attorney General settlement money be traced to its recipients? Scoping, 2026-10-12

Question: do settlement dollars from the Massachusetts Attorney General's cases reach the people harmed, or go to nonprofit groups? This note records what the data can and cannot show. Every number below was read on 2026-10-12 from the Comptroller's CTHRU spending data (Socrata `pegc-naaa`, fiscal 2010 to date, payroll excluded) or from the Attorney General's releases. It is a scoping note, not a finding about any recipient.

## What an earlier hand-built list held
- 168 Attorney General settlement rows in an earlier hand-built list (not published here; $1.52 billion in headline amounts, 2009 to 2026). They cover only cases against a chosen set of 242 companies, so they are a sample of the office's settlements, not all of them.
- The release note names a restitution or refund component on 56 rows and a fund, grant, nonprofit or donation destination on 34. The destinations are mentioned, not itemized.
- No private class actions: the earlier list holds government penalties only.

## What the state's spending data shows
The Attorney General's office paid out $810.9 million in vendor payments since fiscal 2010, of which $657.3 million is its own payroll. Its trust-type accounts, many named for the settlement that funds them, paid $75.6 million to 853 distinct payees across 107 accounts (27 of the accounts have 10 or more payees). The largest:

| Account (CTHRU appropriation) | Fiscal years | Paid | Notes |
|---|---|---|---|
| Consumer and Community Relief Trust (08107105) | 2013 to 2026 | $26.9M, 85 recipients | Largest recipients: Massachusetts Legal Assistance Corp $9.0M, Mass Assoc for Community Action $4.3M, Worcester Community Housing $2.9M |
| Risperdal Grant (08103220) | 2014 to 2021 | $8.4M, 36 recipients | Largest: Mass General Physician Organization $1.04M, Spectrum Health Systems $0.90M, Berkshire Medical Center $0.50M |
| Merrimack Valley Renewal (08100228) | 2022 to 2027 | $4.7M, 5 recipients | North Andover, Andover, Greater Lawrence Technical, Lawrence, South Middlesex Opportunity Council |
| Accounts named for Medtronic, McKinsey, Google, Johnson & Johnson, GlaxoSmithKline (Avandia), Amgen, HSBC, CVS, Chase, Uber and Lyft and others | various | $0.4M to $2.0M each | not yet listed by recipient |

Other agencies pay out settlement money too. The Opioid Recovery and Remediation Fund paid $145.8 million to 106 payees (fiscal 2023 to 2027): $128.9 million through the Department of Public Health, $15.0 million through Health and Human Services and $1.9 million not yet assigned to a department. Largest payees: Massachusetts League of (name cut off in the data) $13.6M, Rize Massachusetts Foundation $13.5M, Health Resources in Action $8.2M, Boston Medical Center $5.8M, Deloitte Consulting $5.3M, The General Hospital Corporation $5.1M. The Division of Banks and the Treasurer paid $8.8 million to 228 payees from a Mortgage Loan Settlement Trust. (Federal State Opioid Response grants and the "Hutchinson settlement" line, which service departments pay out, also match the words "opioid" or "settlement" in the data; they are not Attorney General settlement funds and are excluded here.)

## What it cannot show
1. **Money paid to the Commonwealth as a penalty goes to the General Fund** and cannot be followed to a recipient by origin. Only money placed in a named trust or fund can be traced.
2. **Restitution to consumers** is paid through claims administrators or credits and does not appear in CTHRU. The state's spending data cannot say how much of a settlement reached the people harmed. That needs each settlement's terms and the administrator's or the office's reports on claims paid, which may require public-records requests.
3. **Private class actions** are a different data set (court dockets and cy pres orders), outside the Attorney General's data.

## What a test of the theory would need
For each settlement: (1) terms, the split between restitution, penalty and designated grants; (2) disbursement, who received the designated money (CTHRU, by account and year); (3) ties, each recipient's employees' donations, lobbying and officials' disclosures, using exact normalized-name matching, confirmed matches only (see the README). A recipient list alone is not evidence of anything: many designated grants are ordered by the settlement terms. Any claim about a named recipient stays record-based.

Tools used: the Comptroller's CTHRU open-data API, employer matching for OCPF and FEC donations, lobbying and disclosure matching, and cash-only counting rules.

## How big a project this is (measured the same day)
- **Recipients:** 1,078 distinct payee names and $230.2 million across the AG trust accounts, the opioid fund and the mortgage trust. Each one needs an identity (alias set), a decision on affiliates and a donation, lobbying and disclosure match: the same manual judgment the earlier 242-company list needed, at about four times the count.
- **Overlap with the earlier list is small:** 4 of its 242 companies match a recipient by exact alias (Boston Medical Center $6.1M, Mercy Hospital $1.4M, Northeast Hospital $1.2M, Northeastern University $0.14M). Mass General receives money under its legal name, The General Hospital Corporation ($5.1M from the opioid fund) and Mass General Physician Organization ($1.04M, Risperdal), which the earlier list's aliases do not yet catch. A name-prefix hit on "Target" is a different company (Target Litigation Consulting) and is not a match.
- **The hard half is open-ended:** each settlement's terms (restitution against penalty against designated grants) and what consumers actually received, which needs the office's own records.
- **The unit of analysis** is the settlement dollar, not the recipient: for each settlement, how much went to (a) restitution or refunds to the harmed, (b) civil penalty to the General Fund, (c) designated trusts and grants, (d) the office's own operations or retained revenue, (e) other. The recipient tables above cover only bucket (c). Buckets (a), (b) and (d) come from each settlement's terms; the Attorney General's own releases often state the split in a sentence ("$X in restitution and a $Y civil penalty"), so the first measurable result is the share of dollars in each bucket across the settlements whose releases state the split, reported with how many releases do not.
- **Conclusion:** a separate project that reuses the matching tooling. The recipient tables came first; the settlement-dollar readings followed in notes 03 and 04.
