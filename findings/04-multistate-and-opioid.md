# Multistate settlements, the opioid money, and who gets paid from the state accounts, 2026-10-12

Preliminary. Same method and limits as `03-single-state-sweep.md`. The register is `data/multistate-ma-share.tsv`: one row per release, with the quotes, the Massachusetts amount and a status column saying which rows are counted.

## Method
The 259 releases in the Attorney General's 2015 to 2026 archive that match a text test for multistate or national matters were read for the Massachusetts amount and where the release says it goes. Each recorded amount carries a verbatim quote from the release. I re-checked every quote against the release text and every amount against its quote by script: all 259 rows passed. The text test is broad, so 107 of the 259 turned out to be multistate settlements; the rest are single-state matters (131 of them; they were not counted here and were read as single-state settlements in the audit, see `05-completeness-audit.md`) or multistate actions with no payment (letters, lawsuits, comments). Where a release states no Massachusetts amount, none is recorded: nothing was divided or estimated.

## What Massachusetts is to receive
**First-pass figures; the audit added six matters.** The counts below are from `data/multistate-ma-share.tsv` (90 distinct matters, $1.968 billion). The audit added six more matters with a Massachusetts amount from `data/audit-releases-read.tsv` (General Motors, PHH Mortgage, Comstar, Community Health Systems, Sprague Resources, Dr. Hooshang Poor), $3.1 million in all, so the dashboard shows 96 matters and $1.971 billion; the shares round to the same figures. The Massachusetts amount is a stated maximum in three matters (Meta, Purdue and the Sackler family, and Mylan and six other drugmakers; together $638 million, 32% of the total) and, for the Meta settlement, about $366 million of $516 million is described as guaranteed over ten years.

Of the 107 multistate settlement releases, 95 state a Massachusetts amount. After removing matters announced more than once and two superseded versions of the Purdue and Sackler settlement, 90 distinct matters remain, with $1.968 billion in stated Massachusetts amounts. These are amounts the releases say Massachusetts will receive, many of them "up to" or paid over 10 to 18 years, not cash received.

| Where the release says the Massachusetts amount goes | Matters | Stated amount | Share |
|---|---|---|---|
| Opioid abatement (the state fund and municipalities) | 8 | $1,089,000,000 | 55.3% |
| More than one purpose (mostly the Meta settlement) | 7 | $568,003,410 | 28.9% |
| State agencies recovering their own losses (mostly MassHealth) | 17 | $102,115,601 | 5.2% |
| Use not stated | 29 | $86,741,947 | 4.4% |
| Paid to the Commonwealth, no use stated | 13 | $63,616,374 | 3.2% |
| Restitution or relief to Massachusetts consumers | 13 | $54,615,627 | 2.8% |
| Another named fund or program | 3 | $3,589,818 | 0.2% |

Leaving out the opioid settlements and Meta, the other 81 consumer-protection and Medicaid matters total $362.7 million: 28% to MassHealth and other state agencies, 24% with no stated use, 17.5% paid to the Commonwealth, 15% to consumers as restitution or relief, 14% to more than one purpose, 1% to a named program. In these matters the Massachusetts amount is mostly not paid to consumers, and for a quarter of it the release does not say what happens to it.

## Opioid settlements
Eight distinct matters, $1.089 billion stated for Massachusetts: the distributors and Johnson & Johnson ($525 million over 18 years, of which the release says more than $210 million goes directly to municipalities and more than $310 million to the statewide Opioid Recovery and Remediation Fund), CVS and Walgreens ($230 million), Teva and Allergan ($130 million), Purdue and the Sackler family (up to $105 million over 15 years), Walmart ($61 million), Mylan, Hikma, Amneal and others (up to $17 million), McKinsey ($13 million) and Publicis Health ($8 million). The Attorney General's May 2026 release says Massachusetts has secured more than $1.1 billion in opioid settlement funds; the eight matters agree with that. The money goes to programs and governments, not to individuals harmed: the state fund's payments are in `data/state-fund-payees-cthru.tsv` (106 payees, $145.8 million since fiscal 2023).

## The Meta settlement
The August 2026 settlement with Meta ($17.1 billion nationally) provides Massachusetts "up to $516 million, including approximately $366 million guaranteed to be paid over the next ten years", for youth mental health, crisis services, after-school and summer programs, digital literacy and phone-free schools, with a portion to the General Fund. It is subject to court approval. Most of the "more than one purpose" row above is this settlement.

## Individuals paid from the Attorney General's trust-type accounts and the opioid fund
The recipient lists in this repository include 47 payees whose names look like individuals (inferred from the name only), paid $286,710 in all from the Attorney General's trust accounts and the opioid fund since fiscal 2010: `data/payments-to-individuals.tsv`. The largest is $151,200 from the Opioid Recovery and Remediation Fund. CTHRU records an expense category for each payment (70% of the dollars are coded consultant services, 11% space rental, 10% operational services) and the account it came from; about 30% of the dollars come from trust lines that are not named for a settlement (a conference and training trust, the Gaming Commission, forfeited funds). It does not record the case, contract or service performed, and a name here is not evidence of anything about the payment. The file shows the category and account for each payee. The same payees appear, flagged `individual (inferred from the name)`, in `data/state-fund-payees-cthru.tsv` and `data/state-fund-recipients-political-money-ties.tsv`.

## Limits
- "Stated" is not "received" or "delivered".
- The Massachusetts amount is recorded only where the release states it; at least 12 of the 107 multistate settlements state none, so the total is a floor.
- The readings were made by a model and checked for verbatim quotes and amounts, not against the underlying settlement documents.
- Settlements before 2015 are not covered.
