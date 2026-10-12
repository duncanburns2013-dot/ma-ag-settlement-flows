# Completeness audit: what the first sweep missed, 2026-10-12

Preliminary. The first sweep chose 713 of the 2,863 archive releases by title and read the single-state settlements of $1 million or more. This note records the checks run afterward to find what that choice missed, what they found, and how the totals moved. Earlier notes: `01-scoping.md` to `04-multistate-and-opioid.md`.

## What was checked
1. **The archive listing itself.** The crawl reached the end of the archive and holds all 114 live releases already known to the project. It lacks others. The Internet Archive holds 68 dated releases that the listing does not, 61 of them from September 2017 to March 2018, the months around the Attorney General's website move. Three more looked missing and turned out to be listed under a later title (the office retitled releases after publication; UBS is one). Another 13 captured pages have no date or failed to download, and nothing probed slugs that do not start with "ag-". The true number of unlisted releases is unknown and larger than 68. Register: `data/releases-missing-from-live-listing.tsv`.
2. **The 2,150 releases the title filter skipped.** All were fetched and their text tested for a dollar amount of $100,000 or more in a sentence with settlement or payment language. 279 passed. Readers classified them: 90 single-state settlements (88 after removing two repeats of matters already counted), 3 multistate settlements, 18 grant announcements, 24 reports or summaries, 144 releases with no defendant payment (lawsuits, briefs, statements). The title filter's verb list lacked "resolution", which is how the $26 billion opioid distributors announcement (7/21/2021) was skipped; the matter is counted from a later release.
3. **The tier the first sweep did not read.** 232 releases inside the original selection, with a $100,000 amount and settlement language, had not been read. They hold 206 single-state settlements, mostly $100,000 to $1 million.
4. **The 26 releases recovered from the Internet Archive** with money language: 10 single-state settlements (the largest, Centrus Premier Home Care, $14.3 million to MassHealth, December 2017) and 3 multistate settlements (General Motors, Massachusetts share $2.1 million, half to the General Fund and half to the Local Consumer Aid Fund; PHH Mortgage, about $340,000 to 660 borrowers; UBS, a repeat).

All 537 audit rows carry verbatim quotes, and a script confirmed every quote appears in its release and every amount appears in its quote. Register: `data/audit-releases-read.tsv`.

## How the totals moved
Single-state settlements with a stated total, 2015 to 2026. The first sweep read the $1 million tier; the audit read mostly $100,000 to $1 million.

| | first sweep | audit | combined |
|---|---|---|---|
| settlements | 99 | 280 | 379 |
| stated totals | $755.4M | $103.8M | $859.2M |
| to the harmed | 15.8% | 10.4% | 15.2% |
| penalties, fines, fees or costs | 1.5% | 9.7% | 2.5% |
| paid to the Commonwealth, purpose not stated | 5.0% | 3.3% | 4.8% |
| to state agencies for their own losses | 5.5% | 22.3% | 7.5% |
| designated funds, programs, organizations | 1.4% | 4.5% | 1.8% |
| non-cash relief | 0.1% | 3.0% | 0.4% |
| no breakdown in the release | 70.7% | 46.9% | 67.8% |

The headline finding holds: two thirds of settlement dollars arrive in an announcement with a total and no split. Where the parts add up to the total (147 settlements, $226.0 million), 47.6% goes to the harmed, 20.4% to the Commonwealth (penalties, costs, purpose unstated), 25.2% to state agencies, 5.4% to designated recipients and 1.4% is non-cash.

Three corrections to the first sweep:
- **Category label.** The first pass filed every "paid to the Commonwealth" amount as penalties and costs. Only $11.5 million of the $49.6 million filed that way is called a penalty, fine, fee or cost in the release; $38.1 million (Rent-A-Center's $8.75 million, for one) is paid to the Commonwealth with no stated purpose. Both registers now carry a `state_payment_basis` column.
- **Grubhub.** One settlement had parts but no stated total, and the first-pass shares counted its parts without its total. The first-sweep harmed share is 15.8%, not the 16.3% in note 03 before this update.
- **R028.** One $13.5 million judgment (a couple who ran an unlicensed clinic, March 2017) rests on its title alone. The release page has no body text, here or in two Internet Archive copies. It stays in the totals, flagged in the register.

Forty of the audit's counted settlements are titled as citations: administrative penalties and restitution the office assessed ($15.4 million), not negotiated settlements. They stay in the table above and are marked in the register. Without them the audit column reads 240 settlements, $88.4 million.

Multistate: the audit adds six matters with a Massachusetts amount, $3.1 million in all, which moves the $1.97 billion total by less than 0.2%.

## The Attorney General's discretion, read again
Local OCR (built into Windows, nothing uploaded) read the 54 scanned settlement documents from the second pass and the 14 from the first, and a script tested 113 newly readable documents plus those scans for the standard clause. 34 documents give the Attorney General sole discretion over the payment "in any amount, allocation or apportionment" among consumers, the General Fund, the Local Consumer Aid Fund and consumer-protection programs: 15 from the first pass, 2 from the first pass's scans and 17 from the second pass. 19 more give discretion over part of the money or use looser wording. The count covers 170 readable documents; one scanned document in each pass was unreadable. The tests miss clauses that OCR garbled, so 34 is a floor. I confirmed two OCR hits against the page images: the driving-school judgment (Essex Superior Court, May 2024) and Marriott's $52 million multistate judgment, where Massachusetts's own payment is $1,601,892 and the same clause applies. Documents of multistate settlements where another state's attorney general holds the discretion are excluded. Register: `data/settlement-documents-discretion-clauses-pass2.tsv` and, for the first pass, `data/settlement-documents-discretion-clauses.tsv`.

## Grants
29 more grant announcements that the first grants scan missed, because it required a dollar figure in the title. 27 are grant programs. They add 644 grantee rows (6 with an amount) and bring the distinct grantee names to 513, of which 280 have employee donations, lobbying or an official's disclosed tie on record by exact name: donations $3.34 million, lobbying $23.1 million (`data/grantees-political-money-ties.tsv`). Several releases name the settlement that funded the program: the Healthy Summer Youth Jobs program from health-care and fair-labor settlements, the Natural Gas Fuel Assistance program from a $3 million National Grid settlement, an abandoned-housing receivership fund from the 2012 national mortgage settlement, Project Here from $500,000 of settlement funds plus a $1.5 million GE Foundation gift.

## The office's own budget
CTHRU, payroll included, fiscal 2015 through October 2026: the Attorney General's office spent $620.5 million. 78.1% came from direct appropriations. $46.4 million (7.5%) came from lines the state classes as retained revenue, money the office keeps and spends: False Claims RR $33.2 million, Civil Penalties Retained Revenue $12.3 million, Clean Water and Air Enforcement $0.8 million. The retained-revenue share peaked at 9.2% in fiscal 2018 and was 6.4% in fiscal 2026. Trust accounts paid $73.7 million (11.9%), of which $16.8 million is the Gaming Commission's, not settlement money. Fiscal 2027 covers July to October only. Files: `data/ag-spending-by-appropriation-type-fy2015-2027.tsv`, `data/ag-retained-revenue-and-trust-lines-fy2015-2027.tsv`, `data/ag-retained-revenue-share-by-fiscal-year.tsv`. This differs from the $75.6 million in note 03, which excludes payroll and starts in fiscal 2010.

## Does the reading hold up
A second reader, given no earlier answers, re-read 45 releases drawn at random (20 from the first sweep, 25 from the audit). They agreed on settlement versus not in 44 of 45 and on the headline amount in 39 of 44; the exceptions were an "up to $200,000" figure against the $112,000 payable, and two cases where one reader left the total blank. Across the category fields, 36 amounts were recorded by at least one reader: 25 matched, 10 were recorded by one reader only, and 1 was assigned to a different category. Four of the ten were "paid to the Commonwealth" with no stated purpose, the ambiguity behind the label correction above. Of the 66 amounts both readers recorded, 64 matched; the two that differ are the "up to" headline and the one reassigned category. Both readings passed the quote check. Data: `data/blind-reread-comparison.tsv`. A sample of 45 bounds the error rate loosely; it does not certify the other 900-odd readings.

## Still open
- Releases before 2015, and releases the listing lacks that the Internet Archive never captured, are not read.
- Six archive pages failed to download, and 13 captured pages carry no date.
- Announcements state what a settlement is worth, not what was collected or delivered. The public-records requests in the repository root ask for the accounting.
- The readings were made by a model, checked against quotes and amounts, and not against the underlying settlement documents, except the clauses confirmed above.
