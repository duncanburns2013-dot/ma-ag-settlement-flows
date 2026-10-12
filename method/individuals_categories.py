"""Rebuild data/payments-to-individuals.tsv with the expense category and account CTHRU records for each payee whose name looks like an individual."""
import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cthru import build_url, fetch_json  # noqa: E402

REPO = os.environ.get("AG_REPO", os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
P = os.path.join(REPO, "data", "payments-to-individuals.tsv")
sample = fetch_json(build_url("*", where="department_code='AGO'", limit=1))
print("fields:", sorted(sample[0].keys()))
oc = next((k for k in sample[0] if k.lower().replace("_", "") in ("objectclass", "objectclassname")), None)
print("object class field:", oc)
rows = list(csv.DictReader(open(P, encoding="utf-8", newline=""), delimiter="\t"))
NOT_SETTLEMENT = ("CONFERENCE", "TRAINING", "TRAVEL", "GAMING COMMISSION", "FORFEITED", "MENTAL RETARDATION")
out = []
for r in rows:
    v = r["payee"].replace("'", "''")
    where = f"vendor='{v}' AND budget_fiscal_year>=2010 AND ((department_code='AGO' AND appropriation_type like '(3TN)%') OR upper(fund) like '%OPIOID RECOVERY AND REMEDIATION%')"
    sel = "appropriation_name," + (oc + "," if oc else "") + "sum(amount) as total"
    grp = "appropriation_name" + ("," + oc if oc else "")
    q = fetch_json(build_url(sel, where=where, group=grp, order="total DESC", limit=200))
    accts = "; ".join(f"{x['appropriation_name']}: {float(x['total']):,.0f}" for x in q)
    cats = "; ".join(sorted({x.get(oc, "") for x in q if oc and x.get(oc)}))
    named = "no" if q and all(any(k in x["appropriation_name"].upper() for k in NOT_SETTLEMENT) for x in q) else "yes" if q else ""
    out.append([r["payee"], r["total_paid"], r["first_fiscal_year"], r["last_fiscal_year"], accts or r["accounts_and_amounts"], cats, named,
                "name looks like an individual (inferred from the name only); CTHRU records the expense category and account shown but not the case, contract or service performed"])
with open(P, "w", encoding="utf-8", newline="") as fh:
    w = csv.writer(fh, delimiter="\t", lineterminator="\n")
    w.writerow(["payee", "total_paid", "first_fiscal_year", "last_fiscal_year", "accounts_and_amounts", "expense_category", "account_named_for_a_settlement", "note"])
    w.writerows(out)
tot = sum(float(r["total_paid"]) for r in rows)
nn = sum(float(r["total_paid"]) for r, o in zip(rows, out) if o[6] == "no")
print("payees:", len(out), "total", round(tot), "| from accounts not named for a settlement:", round(nn), f"({100 * nn / tot:.0f}%)")
