"""Export the AG office's spending by appropriation type and the retained-revenue lines (CTHRU, payroll included) to the repo."""
import csv
import os
import sys

os.chdir(os.environ.get("LEDGER_PROJECT", "."))
sys.path.insert(0, ".")
from pipeline.cthru import build_url, fetch_json  # noqa: E402

D = os.path.join(os.environ.get("AG_REPO", "."), "data")
W = "department_code='AGO' AND budget_fiscal_year>=2015"
rows = fetch_json(build_url("appropriation_type,sum(amount) as total,count(*) as n", where=W, group="appropriation_type", order="total DESC", limit=20))
with open(os.path.join(D, "ag-spending-by-appropriation-type-fy2015-2027.tsv"), "w", encoding="utf-8", newline="") as fh:
    w = csv.writer(fh, delimiter="\t", lineterminator="\n")
    w.writerow(["appropriation_type", "total_dollars", "payments"])
    for r in rows:
        w.writerow([r["appropriation_type"], int(float(r["total"])), r["n"]])
named = []
for typ in ("(1RN)", "(3TN)"):
    for r in fetch_json(build_url("appropriation_name,min(budget_fiscal_year) as a,max(budget_fiscal_year) as b,sum(amount) as total", where=W + f" AND appropriation_type like '{typ}%'", group="appropriation_name", order="total DESC", limit=60)):
        named.append((typ, r["appropriation_name"], r["a"], r["b"], int(float(r["total"]))))
with open(os.path.join(D, "ag-retained-revenue-and-trust-lines-fy2015-2027.tsv"), "w", encoding="utf-8", newline="") as fh:
    w = csv.writer(fh, delimiter="\t", lineterminator="\n")
    w.writerow(["type", "appropriation_name", "first_fy", "last_fy", "total_dollars"])
    w.writerows(named)
a = fetch_json(build_url("budget_fiscal_year,sum(amount) as total", where=W + " AND appropriation_type like '(1RN)%'", group="budget_fiscal_year", order="budget_fiscal_year", limit=20))
b = fetch_json(build_url("budget_fiscal_year,sum(amount) as total", where=W, group="budget_fiscal_year", order="budget_fiscal_year", limit=20))
bm = {r["budget_fiscal_year"]: float(r["total"]) for r in b}
with open(os.path.join(D, "ag-retained-revenue-share-by-fiscal-year.tsv"), "w", encoding="utf-8", newline="") as fh:
    w = csv.writer(fh, delimiter="\t", lineterminator="\n")
    w.writerow(["fiscal_year", "retained_revenue_dollars", "all_ag_spending_dollars", "share"])
    for r in a:
        fy = r["budget_fiscal_year"]
        w.writerow([fy, int(float(r["total"])), int(bm[fy]), round(float(r["total"]) / bm[fy], 4)])
print("wrote CTHRU exports")
