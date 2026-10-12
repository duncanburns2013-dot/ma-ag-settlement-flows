import collections
import csv
import glob
import os
import re
import sys

H = os.environ.get("AG_SWEEP_WORK", "work")  # scratch folder for downloads and intermediate files
sys.path.insert(0, H)
from sweep2_lib import amounts  # noqa: E402


def norm(s):
    s = (s or "").replace("\u2019", "'").replace("\u2018", "'").replace("\u201c", '"').replace("\u201d", '"').replace("\u2013", "-").replace("\u2014", "-").replace("\xa0", " ")
    return re.sub(r"\s+", " ", s).strip().lower()


def num(x):
    x = (x or "").strip().replace(",", "").replace("$", "")
    try:
        return float(x) if x else None
    except ValueError:
        return None


man = {r["release_id"]: r for r in csv.DictReader(open(os.path.join(H, "grants_read", "manifest.tsv"), encoding="utf-8"), delimiter="\t")}
rows = []
for f in sorted(glob.glob(os.path.join(H, "agent_out", "B*.csv"))):
    rows += list(csv.DictReader(open(f, encoding="utf-8", newline="")))
src = {}
def source(rid):
    if rid not in src:
        src[rid] = norm(open(os.path.join(H, "grants_read", f"{rid}.txt"), encoding="utf-8").read())
    return src[rid]

bad, good = [], []
for r in rows:
    rid = r["release_id"]
    probs = []
    if rid not in man:
        bad.append((rid, "unknown release"))
        continue
    s = source(rid)
    amt = num(r["amount"])
    qa, qf = r.get("quote_amount", ""), r.get("quote_funding", "")
    if qa and norm(qa) not in s:
        probs.append("quote_amount not verbatim")
    if qf and norm(qf) not in s:
        probs.append("quote_funding not verbatim")
    if amt is not None:
        if not qa:
            probs.append("amount without a quote")
        elif not any(abs(a - amt) <= max(1, amt * 0.005) for a in amounts(qa)):
            probs.append("amount not in its quote")
    if r["funding_source"] and not qf:
        probs.append("funding source without a quote")
    if r["row_type"] == "grantee" and qa and r["grantee"] and norm(r["grantee"]) not in norm(qa):
        probs.append("grantee name not in its quote")
    (bad if probs else good).append((r, probs) if probs else r)
print(f"rows: {len(rows)}; passing: {len(good)}; with a problem: {len(bad)}")
for item in bad[:25]:
    r, p = item if isinstance(item, tuple) and isinstance(item[0], dict) else (None, item)
    print("  ", (r or {}).get("release_id"), (r or {}).get("row_type"), (r or {}).get("grantee", "")[:40], "|", p if not isinstance(p, tuple) else p[1])
prog = [r for r in good if r["row_type"] == "program"]
gr = [r for r in good if r["row_type"] == "grantee"]
print("program rows:", len(prog), " grantee rows:", len(gr), " distinct grantee names:", len({norm(r['grantee']) for r in gr}))
with_amt = [r for r in gr if num(r["amount"])]
print("grantee rows with an amount:", len(with_amt), " total $", f"{sum(num(r['amount']) for r in with_amt):,.0f}")
print("\nprogram totals and funding sources as stated in the releases:")
for r in sorted(prog, key=lambda r: man[r["release_id"]]["date"][-4:] + man[r["release_id"]]["date"]):
    m = man[r["release_id"]]
    print(f"  {m['date']:>10} {r['release_id']} ${num(r['amount']) or 0:>11,.0f}  {r['program'][:48]:48s} | funded by: {r['funding_source'][:90]}")
