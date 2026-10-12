# Completeness audit: what the first sweep missed, 2026-10-12

Preliminary. The first sweep chose 713 of the 2,863 archive releases by title and read the single-state settlements of $1 million or more. This note records the checks run afterward to find what that choice missed, what they found, and how the totals moved. The audit changed the headline: the first sweep said about 71% of announced dollars came with no dollar split, and the combined record says 32%. Earlier notes: `01-scoping.md` to `04-multistate-and-opioid.md`.

## What was checked
1. **The 131 releases the multistate test flagged.** The first sweep used one text test to route releases into a single-state pass and another into a multistate pass. 131 releases that the multistate test flagged turned out to be Massachusetts-only matters, and neither pass counted them. They hold 103 counted settlements, $1.19 billion in announced totals, including a $600 million payment from the tobacco manufacturers to the General Fund (August 2024), Beth Israel Lahey Health's merger commitments ($71.6 million), NiSource and Columbia Gas ($56 million), Judgment Acquisitions Unlimited ($52 million of debt relief), Santander Consumer ($22 million) and Equifax ($18.2 million). An independent review of the finished page found this gap. These rows are tagged in `data/multistate-ma-share.tsv` and counted in `data/audit-releases-read.tsv`.
2. **The archive listing itself.** The crawl reached the end of the archive and holds all 114 live releases already known to the project. It lacks others. The Internet Archive holds 67 dated releases that the listing does not, 61 of them from September 2017 to March 2018, the months around the Attorney General's website move. Four more looked missing and turned out to be listed under a later title (the office retitled releases after publication; UBS and MaidPro are two). Another 13 captured pages have no date or failed to download, and nothing probed slugs that do not start with "ag-". The true number of unlisted releases is unknown and larger than 67. Register: `data/releases-missing-from-live-listing.tsv`.
3. **The 2,150 releases the title filter skipped.** All were fetched and their text tested for a dollar amount of $100,000 or more in a sentence with settlement or payment language. 279 passed. Readers classified them: 90 single-state settlements (88 after removing two repeats), 3 multistate settlements, 18 grant announcements, 24 reports or summaries, 144 releases with no defendant payment (lawsuits, briefs, statements). The title filter's verb list lacked "resolution", which is how the $26 billion opioid distributors announcement (7/21/2021) was skipped; the matter is counted from a later release.
4. **The tier the first sweep did not read.** 232 releases inside the original selection, with a $100,000 amount and settlement language, had not been read. They hold 206 single-state settlements, mostly $100,000 to $1 million.
5. **The releases recovered from the Internet Archive.** 26 had money language: 9 counted single-state settlements (the largest, Centrus Premier Home Care, $14.3 million to MassHealth, December 2017) and 3 multistate settlements (General Motors, Massachusetts share $2.1 million; PHH Mortgage, about $340,000; UBS, a repeat).
6. **A second reading of the recovered matters.** A second reader, given only the release text, rechecked the 48 recovered single-state matters with totals of $1 million and over for kind, total, parts and repeats. None was a non-settlement or a repeat, and 11 had a problem in the parts. Six were corrected in the register: the $6 million Santander payment to Massachusetts was added; two payments of $1.0 million and $0.6 million that the releases tie to consumer refunds (DMB, Global) moved to no dollar split; Penske's $3 million, a civil penalty, moved out of "no stated purpose"; and restitution that had been entered twice in two MassHealth cases ($0.65 million) was kept once. Five were left as read and each row's note says why: the register takes one quoted amount per column, so a sum or a half-share cannot be entered, and one release describes $7 million of savings as additional to its total. A script scan of every counted row for the same double entry found no others. The smaller recovered matters were not rechecked by a second reader.

All 668 audit rows carry verbatim quotes, and a script confirmed every quote appears in its release and every amount appears in its quote. Register: `data/audit-releases-read.tsv`. Method scripts: `method/`.

## How the totals moved
Single-state settlements with a stated total, 2015 to 2026. "First sweep" is the 99 settlements the first pass counted; "audit" is everything the audit added, including the 131 flagged releases.

| | first sweep | audit | combined |
|---|---|---|---|
| settlements | 99 | 379 | 478 |
| announced totals | $755.4M | $1,289.6M | $2,045.0M |
| to the harmed | 15.8% | 8.6% | 11.3% |
| penalties, fines, fees or costs | 1.5% | 11.5% | 7.8% |
| paid to the Commonwealth, purpose not stated | 5.0% | 48.7% | 32.6% |
| to state agencies for their own losses | 5.5% | 3.9% | 4.5% |
| designated funds, programs, organizations | 1.4% | 10.2% | 6.9% |
| non-cash relief | 0.1% | 7.7% | 4.9% |
| no dollar split in the release | 70.7% | 9.4% | 32.0% |

In the combined record, 270 of 478 settlements (56%) state a dollar amount for at least one destination, and 199 (42%, $1.31 billion) have stated amounts within 3% of their total (184 exactly). By size: totals of $1 million and over (143 settlements, $1.94 billion) are 31% no split and 11% to the harmed; totals under $1 million (335 settlements, $104 million) are 52% no split and 14% to the harmed.

Read these shares with the concentration in view. The $600 million tobacco payment is 29% of the announced total and 90% of the money paid to the Commonwealth with no stated purpose; without it, the combined record is 15.9% to the harmed and 45.3% with no dollar split. Uber and Lyft ($175 million) and Eonsmoke ($51 million) sit in the no-split share. The no-split share also counts releases that say money goes to consumers, drivers or homeowners without an amount.

Corrections to earlier figures in this repository:
- **The first-sweep split** is a subset result. It missed the 131 releases above and read only the $1 million tier it found.
- **Category label.** The first pass filed every "paid to the Commonwealth" amount as penalties and costs. Only $11.5 million of the $49.6 million filed that way is called a penalty, fine, fee or cost; $38.1 million is paid with no stated purpose. Both registers carry a `state_payment_basis` column. The audit readers recorded such payments the same way, so the buckets match across passes.
- **Grubhub.** One first-sweep settlement had parts but no total, and the first-pass shares counted its parts without its total.
- **Title-only totals.** Eight counted totals, $240.6 million, come from the release title because the body states none, among them a $165 million court order against HealthMarkets, State Street in 2019 ($54 million, with restitution "expected to exceed" $48 million) and a $13.5 million judgment whose release page carries no body text. The dashboard lists them in note 7 and tags each row.
- **Repeats.** Ten single-state repeats and two multistate repeats were removed (for example Penske and Ditech, each posted twice, and a MaidPro release counted under two titles).
- **Combine script.** A regular expression in the audit's combine script had lost its word boundaries, which understated the penalty share by 0.1 point in an interim table. The registers and dashboard use the correct test.

Rows to know about: 35 counted rows with totals are criminal cases ($25.0 million), 40 are administrative citations ($15.4 million), 41 totals are described as "up to" figures and 40 mention a suspended amount. Four merger approval agreements with dollar commitments ($129 million) are counted. The dashboard has toggles for citations and criminal cases and discloses each count.

Multistate: the audit adds six matters with a Massachusetts amount, $3.1 million in all, so the multistate total is $1.97 billion across 96 matters, at stated maximums (note 04).

## Where the money goes, as the releases state it
Single-state settlements with a stated total, 2015 to 2026. The three columns are slices of the same register, so read them side by side. In the third column each share is of the money the releases assign, because those settlements have no unassigned remainder.

| where the release says it goes | all 478 settlements | without the $600 million tobacco payment | the 198 others whose stated amounts add up to the total |
|---|---|---|---|
| to the harmed | 11.3% | 15.9% | 28.6% |
| non-cash relief | 4.9% | 6.9% | 12.0% |
| penalties, fines, fees or costs | 7.8% | 11.1% | 21.8% |
| paid to the Commonwealth, no purpose stated | 32.6% | 4.6% | 7.5% |
| state agencies for their own losses | 4.5% | 6.3% | 11.7% |
| named funds, programs or organizations | 6.9% | 9.8% | 18.4% |
| no dollar split in the release | 32.0% | 45.3% | none |
| announced dollars | $2.05 billion | $1.45 billion | $712 million |

How to read it:
- **A stated destination is not delivery.** A release says what a settlement is worth and who is to receive it. It does not report what was collected or paid out.
- **"To the harmed" and non-cash relief both reach consumers.** "To the harmed" is refunds, restitution, bill credits and back wages. Non-cash relief is valued relief such as loan principal reduction or debt forgiveness. Together they are 16.1% of all announced dollars, 22.9% without the tobacco payment, and 40.6% where the stated amounts add up.
- **The tobacco payment drives the largest bucket.** The $600 million paid to the General Fund in August 2024 is 29.3% of announced dollars and 90.0% of the money paid to the Commonwealth with no stated purpose.
- **No dollar split is not evidence either way.** It includes releases that say money goes to consumers or drivers without an amount, and releases that give no breakdown at all. The largest are Uber and Lyft ($175 million, most to drivers as restitution according to the release), State Street ($74.5 million of a $75 million disgorgement, recipient not stated) and Eonsmoke ($51 million, no breakdown).
- **How no dollar split is computed.** It is the announced total minus the stated parts, netted across settlements. Five settlements state parts that exceed their total (by $391,500 in all, $300,000 of it Franklin Credit, whose release says "over $10 million"). Clipping those rows at their totals would make the no-split share 32.1% instead of 32.0%, and 45.4% instead of 45.3% without the tobacco payment.
- **Checked twice, independently.** Two readers recomputed every figure in this section from the raw registers without seeing the build code, one in Python and one in PowerShell, and both matched.
- **What the register cannot show** is whether money paid to the Commonwealth or to designated recipients reaches the people harmed. That needs the office's own accounting, which the records requests ask for.

## The Attorney General's discretion, read again
Local OCR (built into Windows, nothing uploaded) read the 54 scanned settlement documents from the second pass and the 14 from the first, and a script tested 113 newly readable documents plus those scans for the standard clause. 34 settlement rows give the Attorney General sole discretion over the payment "in any amount, allocation or apportionment" among consumers, the General Fund, the Local Consumer Aid Fund and consumer-protection programs: 15 from the first pass, 2 from the first pass's scans and 17 from the second pass. 19 more give discretion over part of the money or use looser wording. Uber and Lyft are two settlements under one agreement, so the 34 rows rest on 33 distinct documents, and in a few rows (Collegium; Adroit, $2 million of $5 million) the discretion covers only part of the payment. The count covers 170 readable items (43 settlements from the first sweep, 127 documents from the second); one scanned document in each pass was unreadable. The earliest clause found is dated November 2019 and only 8 documents before 2020 are itemised in the registers, so earlier years are largely unread, not clause-free. The tests miss clauses that OCR garbled, so 34 is a floor. I confirmed two OCR hits against the page images: the driving-school judgment (Essex Superior Court, May 2024) and Marriott's $52 million multistate judgment, where Massachusetts's own payment is $1,601,892 and the same clause applies. Documents of multistate settlements where another state's attorney general holds the discretion are excluded. A Citibank row had shown a North Carolina sentence; it now shows the Massachusetts clause, which covers uncashed Massachusetts funds only. Register: `data/settlement-documents-discretion-clauses-pass2.tsv` and, for the first pass, `data/settlement-documents-discretion-clauses.tsv`.

## Grants
29 more grant announcements that the first grants scan missed, because it required a dollar figure in the title. 27 are grant programs. They add 644 grantee rows (6 with an amount) and bring the distinct grantee names to 513 (names matched after ignoring case, punctuation and endings such as Inc.), of which 280 have employee donations, lobbying or an official's disclosed tie on record: donations $3.34 million, lobbying $23.1 million (`data/grantees-political-money-ties.tsv`). Several releases name the settlement that funded the program: the Healthy Summer Youth Jobs program from health-care and fair-labor settlements, the Natural Gas Fuel Assistance program from a $3 million National Grid settlement, an abandoned-housing receivership fund from the 2012 national mortgage settlement, Project Here from $500,000 of settlement funds plus a $1.5 million GE Foundation gift.

## The office's own budget
CTHRU, payroll included, fiscal 2015 through October 2026: the Attorney General's office spent $620.5 million across every funding type. 78.1% came from direct appropriations. $46.4 million (7.5%) came from lines the state classes as retained revenue, money the office keeps and spends: False Claims RR $33.2 million, Civil Penalties Retained Revenue $12.3 million, Clean Water and Air Enforcement $0.8 million. The retained-revenue share peaked at 9.2% in fiscal 2018 and was 6.4% in fiscal 2026, a provisional figure. Trust accounts paid $73.7 million (11.9%), which include payments to outside recipients and $16.8 million for the Gaming Commission, not settlement money. Fiscal 2027 covers July to October only. Files: `data/ag-spending-by-appropriation-type-fy2015-2027.tsv`, `data/ag-retained-revenue-and-trust-lines-fy2015-2027.tsv`, `data/ag-retained-revenue-share-by-fiscal-year.tsv`. This differs from the $75.6 million in note 03, which excludes payroll and starts in fiscal 2010.

## Does the reading hold up
A second reader, given no earlier answers, re-read 45 releases drawn at random (20 from the first sweep, 25 from the audit). They agreed on settlement versus not in 44 of 45 and on the headline amount in 39 of 44; the exceptions were an "up to $200,000" figure against the $112,000 payable, and two cases where one reader left the total blank. Across the category fields, 36 amounts were recorded by at least one reader: 25 matched, 10 were recorded by one reader only, and 1 was assigned to a different category. Four of the ten were "paid to the Commonwealth" with no stated purpose, the ambiguity behind the label correction above. Of the 66 amounts both readers recorded, 64 matched. The comparison does not show which way the shares would move. Both readings passed the quote check. Data: `data/blind-reread-comparison.tsv`. A sample of 45 bounds the error rate loosely, and it was drawn before the 131 flagged releases were read.

## Still open
- Releases before 2015, and releases the listing lacks that the Internet Archive never captured, are not read. Settlements under $100,000 were not systematically searched for.
- Six archive pages failed to download, and 13 captured pages carry no date.
- Announcements state what a settlement is worth, not what was collected or delivered. The public-records requests in the repository root ask for the accounting.
- The readings were made by a model, checked against quotes and amounts, and not against the underlying settlement documents, except the clauses confirmed above.
