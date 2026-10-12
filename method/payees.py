import csv
import os
import sys

H = os.environ.get("AG_SWEEP_WORK", "work")  # scratch folder for downloads and intermediate files
os.chdir(os.environ.get("LEDGER_PROJECT", "."))
sys.path.insert(0, ".")
from pipeline.cthru import build_url, fetch_json

W = "budget_fiscal_year>=2010 AND vendor not like '%PAYROLL%'"
SCOPES = {
    "AG trust accounts": W + " AND department_code='AGO' AND appropriation_type like '(3TN)%'",
    "Opioid Recovery and Remediation Fund": W + " AND upper(fund) like '%OPIOID RECOVERY AND REMEDIATION%'",
    "Mortgage Loan Settlement Trust": W + " AND appropriation_name like '%MORTGAGE LOAN SETTLEMENT TRUST%'",
}
allv = {}
for name, where in SCOPES.items():
    rows = fetch_json(build_url("vendor,sum(amount) as total,count(*) as n,min(budget_fiscal_year) as a,max(budget_fiscal_year) as b", where=where, group="vendor", order="total DESC", limit=5000))
    for r in rows:
        v = allv.setdefault(r["vendor"], {"total": 0.0, "scopes": {}, "first": 9999, "last": 0})
        v["total"] += float(r["total"])
        v["scopes"][name] = v["scopes"].get(name, 0) + float(r["total"])
        v["first"] = min(v["first"], int(r["a"]))
        v["last"] = max(v["last"], int(r["b"]))
with open(os.path.join(H, "payees.tsv"), "w", encoding="utf-8", newline="") as fh:
    w = csv.writer(fh, delimiter="\t", lineterminator="\n")
    w.writerow(["vendor", "total", "first_fy", "last_fy", "scopes"])
    for k, v in sorted(allv.items(), key=lambda kv: -kv[1]["total"]):
        w.writerow([k, f"{v['total']:.2f}", v["first"], v["last"], "; ".join(f"{s}: {a:,.0f}" for s, a in v["scopes"].items())])
print(len(allv), "payees,", f"${sum(v['total'] for v in allv.values()):,.0f}")
