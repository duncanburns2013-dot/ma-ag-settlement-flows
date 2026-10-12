# Where do Attorney General settlement dollars go? First pass, 2026-10-12

Preliminary. Read from documents on 2026-10-12; nothing here has been cross-checked a second time. Scope notes are in `01-scoping.md`.

## What the settlement documents say about the money
The Attorney General's consent judgments and assurances of discontinuance carry a standard payment clause. In the driving-school case (Commonwealth v. North Andover Auto School, LLC and Michael J. Larocque, Essex Superior Court 2177CV00336, filed 2024-05-07, read from the court-stamped judgment, paragraphs 9 and 10), the $300,000 is $186,868.30 paid by the defendants plus $113,131.70 in cash and bank assets the State Police seized from them in September 2020, and the clause reads: "At her sole discretion, the Attorney General may use or distribute the Monetary Payment, in any amount, allocation, or apportionment and for any purpose permitted by law," including (a) payments to or for consumers, (b) the General Fund, (c) the Local Consumer Aid Fund (G.L. c. 12, section 11G), and/or (d) programs "in furtherance of the protection of the people of the Commonwealth." No amount is committed to the students. The 2021 complaint had asked for over $1 million in full refunds to about 1,500 students.

Across the 168 Attorney General settlements in the earlier hand-built list: 114 releases are live on mass.gov, 48 of them link at least one settlement document (74 documents), 59 of those are readable as text and 14 are scanned images (read later by OCR; see note 05; the driving-school judgment is one of them and was read by eye). The clause above, in which the Attorney General alone decides how a payment is allocated, appears in **15 of the 43 settlements with a readable document**, which carry $281.5 million of the $467.2 million headline in the 43. Four more documents use "sole discretion" over part of a payment or over procedures (Injured Workers Pharmacy, Optum Rx, Express Scripts, Santander Consumer; $25.6 million headline), so the count of 19 matches in `data/settlement-documents-discretion-clauses.tsv` is split into a strict and a looser kind in its `kind` column. The table has one row per settlement with the clause as read and the document link. Where the strict clause appears it is standard text and the listed purposes begin with payments to or for consumers; the documents do not say how much was spent on each purpose, and nothing in them requires any amount to reach consumers. The dollar figures are headline amounts of the settlements, not the discretionary part: in Uber and Lyft ($175 million) the release says a substantial majority goes to drivers.

Settlements whose documents instead define a consumer payment (a trustee, a settlement administrator or a stated restitution fund): 6 settlements, $93.2 million; 4 more have both. Uber and Lyft ($175 million) are in the "both" group.

## What the state's spending data shows
- The Local Consumer Aid Fund, named in the clause, shows **$95** in the Comptroller's CTHRU data (fiscal 2018, a reimbursement) and no payments to outside recipients under its own name. Where it distributes money is not visible there.
- The Attorney General's trust-type accounts paid $100.7 million since fiscal 2010: $25.1 million (25%) was payroll charged to those trust accounts; the rest went to 853 payees (the recipient tables in the scoping note).
- CTHRU holds nothing named for the driving-school case, and no claims administrator or consumer-refund payee in the trust accounts beyond two $19,000 and $3,000 analytics vendors. Direct refund checks to individuals do not appear in the data.
- Opioid Recovery and Remediation Fund: $145.8 million to 106 payees since fiscal 2023.

## What the releases say (rough, not yet classified by hand)
A sentence-level read of the 158 releases already on disk finds a dollar figure next to restitution or relief words in about two thirds of them, a penalty or "to the Commonwealth" amount in under half, and a designated fund, grant or nonprofit in about 30%. These are keyword counts on headline text, double-count across buckets, and are not delivered amounts. The largest settlements (State Street 2010, Uber and Lyft, State Street 2019, HealthMarkets, the mortgage-securitization cases) state large amounts for the harmed. Many mid-size consumer-protection settlements (Injured Workers Pharmacy $11 million, Rent-A-Center $8.75 million, First Transit $7.3 million) state a payment "to the Commonwealth" and nothing about its use.

## Not yet known
- What share of the discretionary payments was in fact spent on consumers. That needs the Attorney General's own records on refunds paid.
- The 54 releases only on the Internet Archive (some were read in the audit; see note 05).
- Settlements outside the earlier list's 168: the Attorney General's full press-release archive has more (read in notes 03 to 05).
- Recipients' political ties (donations, lobbying, officials' disclosures) have not been run yet.
