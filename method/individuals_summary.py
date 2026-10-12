"""Totals for the individual-payee register: dollars by CTHRU expense category and by whether the account is named for a settlement."""
import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cthru import build_url, fetch_json  # noqa: E402

REPO = os.environ.get("AG_REPO", os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
rows = list(csv.DictReader(open(os.path.join(REPO, "data", "payments-to-individuals.tsv"), encoding="utf-8", newline=""), delimiter="\t"))
names = ",".join("'" + r["payee"].replace("'", "''") + "'" for r in rows)
where = f"vendor in ({names}) AND budget_fiscal_year>=2010 AND ((department_code='AGO' AND appropriation_type like '(3TN)%') OR upper(fund) like '%OPIOID RECOVERY AND REMEDIATION%')"
q = fetch_json(build_url("object_class,appropriation_name,sum(amount) as total", where=where, group="object_class,appropriation_name", order="total DESC", limit=500))
tot = sum(float(x["total"]) for x in q)
bycat, bynamed = {}, {"settlement-named or opioid fund": 0.0, "not named for a settlement": 0.0}
NOT = ("CONFERENCE", "TRAINING", "TRAVEL", "GAMING COMMISSION", "FORFEITED", "MENTAL RETARDATION")
for x in q:
    v = float(x["total"])
    bycat[x["object_class"]] = bycat.get(x["object_class"], 0) + v
    bynamed["not named for a settlement" if any(k in x["appropriation_name"].upper() for k in NOT) else "settlement-named or opioid fund"] += v
print(f"total ${tot:,.0f}")
for k, v in sorted(bycat.items(), key=lambda kv: -kv[1]):
    print(f"  {k:45s} ${v:>10,.0f} {100 * v / tot:5.1f}%")
for k, v in bynamed.items():
    print(f"  {k:45s} ${v:>10,.0f} {100 * v / tot:5.1f}%")
