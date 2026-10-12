import collections
import csv
import os
import re

H = os.environ.get("AG_SWEEP_WORK", "work")  # scratch folder for downloads and intermediate files
rows = list(csv.DictReader(open(os.path.join(H, "ag-docs.tsv"), encoding="utf-8"), delimiter="\t"))


def sentences(t):
    t = re.sub(r"\s+", " ", t)
    return re.split(r"(?<=[.;])\s+(?=[A-Z(\"“])", t)


ALLOC = re.compile(r"distribut|allocat|expend|apportion|use (?:or distribute )?this payment|use the (?:monetary )?payment", re.I)
NOT_ALLOC = re.compile(r"rescind|installment|identity of the Trustee|Settlement Administrator will be chosen|choose the Trustee|extend|waive", re.I)
RESTIT = re.compile(r"Settlement Administrator|Trustee|Settlement Fund|escrow|restitution (?:payment|fund)|pay restitution|restitution in the (?:total )?amount|restitution of|refunds? (?:to|of)|consumer redress|consumer relief", re.I)

per = {}
for i, r in enumerate(rows):
    f = os.path.join(H, "ag-docs", f"{i:03d}.pdf.txt")
    if not os.path.exists(f):
        continue
    t = open(f, encoding="utf-8", errors="replace").read()
    if len(t.strip()) < 800:
        continue
    ss = sentences(t)
    disc = [s for s in ss if re.search(r"sole discretion", s, re.I) and ALLOC.search(s) and not NOT_ALLOC.search(s)]
    rest = [s for s in ss if RESTIT.search(s) and "$" in s]
    lcaf = bool(re.search(r"Local Consumer Aid Fund", t, re.I))
    gen = bool(re.search(r"General Fund", t, re.I))
    d = per.setdefault(r["penalty_id"], {"defendant": r["defendant"], "date": r["date"], "amount": float(r["amount"]), "disc": [], "rest": [], "lcaf": False, "gen": False, "docs": 0})
    d["disc"] += disc
    d["rest"] += rest
    d["lcaf"] |= lcaf
    d["gen"] |= gen
    d["docs"] += 1

cls = collections.defaultdict(list)
for pid, d in per.items():
    key = ("AG decides the split" if d["disc"] else "") + (" + " if d["disc"] and d["rest"] else "") + ("document defines a consumer payment" if d["rest"] else "")
    cls[key or "neither found"].append((pid, d))
print(f"settlements with a readable linked document: {len(per)}   (headline ${sum(d['amount'] for d in per.values()):,.0f})")
for k, lst in sorted(cls.items(), key=lambda kv: -sum(d['amount'] for _, d in kv[1])):
    print(f"  {k:55s} {len(lst):3d} settlements  ${sum(d['amount'] for _, d in lst):>14,.0f}")
print()
print("settlements whose document leaves the split to the Attorney General:")
for pid, d in sorted(cls.get("AG decides the split", []) + cls.get("AG decides the split + document defines a consumer payment", []), key=lambda x: -x[1]["amount"]):
    s = d["disc"][0]
    print(f"  [{d['date']}] {d['defendant'][:34]:34s} ${d['amount']:>12,.0f}  LCAF:{'y' if d['lcaf'] else 'n'}  {s[:230]}")
