"""Political-money ties for ALL grantees (earlier B set plus the audit's K set)."""
import collections
import csv
import glob
import os
import sys

H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, H)
sys.path.insert(0, os.environ.get("LEDGER_PROJECT", "."))
import ties  # noqa: E402

rows = []
for pat in ("B*.csv", "K*.csv"):
    for f in sorted(glob.glob(os.path.join(H, "agent_out", pat))):
        rows += list(csv.DictReader(open(f, encoding="utf-8", newline="")))
gr = [r for r in rows if r["row_type"] == "grantee" and r["grantee"].strip()]
progs = collections.defaultdict(set)
for r in gr:
    progs[r["grantee"].strip()].add(r["program"][:40])
rec = [(g, {"total": "", "programs": "; ".join(sorted(p))}) for g, p in progs.items()]
print("grantee names (raw):", len(rec))
out = ties.run(rec, "AG grant-program grantees named in the releases (both reading passes)", os.path.join(H, "ties_grantees_all.tsv"))
print("\nlargest by donations + lobbying:")
for o in sorted(out, key=lambda o: -(o["ocpf"] + o["fec"] + o["lob_firm"] + o["lob_inhouse"]))[:20]:
    print(f"  {o['name'][:46]:46s} donations ${o['ocpf'] + o['fec']:>9,.0f}  lobbying ${o['lob_firm'] + o['lob_inhouse']:>10,.0f}  officials' ties {o['hold']:>3}")
