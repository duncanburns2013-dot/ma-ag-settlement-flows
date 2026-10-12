# Public records requests these findings point to

The findings stop where the public record stops. The Attorney General's announcements say what a settlement was worth; they rarely say what happened to each dollar afterwards. The state's spending data shows money leaving named accounts but not, for most settlements, where it was deposited or why. The records below would close those gaps. Each one names the dataset in this repository that raises the question.

Massachusetts calls its version of FOIA the Public Records Law (G.L. c. 66, section 10; G.L. c. 4, section 7, clause 26; 950 CMR 32.00). An agency must respond within 10 business days, and a refusal can be appealed to the Supervisor of Records. Confirm the current text and the agency's records access officer before filing. Federal FOIA does not reach a state agency.

## To the Attorney General's Office (records access officer)

1. **Disbursement accounting for settlements where the Attorney General allocates the payment.** For each settlement in `data/settlement-documents-discretion-clauses.tsv`: the total received, the date and account it was deposited in, and every later disbursement with date, amount and purpose (payments to consumers, the General Fund, the Local Consumer Aid Fund, programs, costs). Raised by: the standard clause giving the Attorney General sole discretion over allocation, in 34 of 170 readable settlement documents (this file lists the first 15; the rest are in `data/settlement-documents-discretion-clauses-pass2.tsv`).
2. **Local Consumer Aid Fund (G.L. c. 12, section 11G).** Annual balance and every disbursement by recipient and amount, fiscal 2015 to date, with the grant agreements. Raised by: the fund appears in settlement documents but shows $95 under its own name in the state's CTHRU data.
3. **Settlement trust accounts.** For each account named in `data/state-fund-payees-cthru.tsv` (for example the Consumer and Community Relief Trust, the Risperdal Grant account and the accounts named for individual companies): the settlement or settlements that funded it, deposits by date and amount, and every disbursement. Raised by: $75.6 million paid to 853 payees from these accounts since fiscal 2010, with the funding settlement not stated in the spending data.
4. **Grant programs funded by settlements** (`data/ag-grant-programs-and-grantees.tsv`). For each program: the settlement dollars allocated to it, applications received, scoring and selection records, award letters with the amount for each grantee, conflict-of-interest and recusal records, and grantee reports. Raised by: 513 named grantee organizations, with a dollar amount stated for only 30 of 1,039 grantee entries in the announcements.
5. **Claims administrators and trustees.** For each settlement where a settlement administrator or trustee was appointed (Uber and Lyft, Credit Acceptance and others): the contract, fees paid, and the administrator's reports on amounts claimed, paid, returned and unclaimed. Raised by: announcements that state restitution without stating what reached people.
6. **Unclaimed and residual restitution.** The office's policy and records for where money goes when restitution cannot be delivered or is not claimed.
7. **Payroll charged to the Attorney General's trust accounts.** The authority and accounting for payroll charged to trust-type accounts: $25.1 million, 25% of what those accounts paid out since fiscal 2010 in the spending data (payroll included). The data does not say which settlements funded those accounts.

8. **Retained-revenue lines.** For the False Claims RR and Civil Penalties Retained Revenue lines (`data/ag-retained-revenue-and-trust-lines-fy2015-2027.tsv`): the settlements and judgments credited to each line by fiscal year, and what the money paid for. Raised by: $45.5 million spent from these two lines since fiscal 2015, with the funding settlements not named in the spending data.

## To the Executive Office of Health and Human Services and the Department of Public Health

9. **Opioid Recovery and Remediation Fund.** Award and procurement records, contracts and payment records for the largest payees in `findings/04-multistate-and-opioid.md` and `data/state-fund-payees-cthru.tsv`, and the advisory council's minutes and recommendations. Raised by: $145.8 million paid to 106 payees since fiscal 2023.

## To the Comptroller of the Commonwealth

10. **Account-level ledgers** for the settlement trust accounts in request 3, if the Attorney General's office does not produce them: deposits by source for each account.

## A short letter to adapt

> Under the Massachusetts Public Records Law, G.L. c. 66, section 10, I request copies of the following records of your office: [paste the request]. I ask for electronic copies in a searchable format. If any part is withheld, please identify the exemption relied on and release the rest. If fees will exceed $[amount], please tell me before processing. [Name, contact.]
