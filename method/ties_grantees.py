import collections
import csv
import glob
import os
import sys

H = os.environ.get("AG_SWEEP_WORK", "work")  # scratch folder for downloads and intermediate files
sys.path.insert(0, H)
sys.path.insert(0, os.environ.get("MATCH_TABLES_DIR", "."))
import ties  # noqa: E402

man = {r["release_id"]: r for r in csv.DictReader(open(os.path.join(H, "grants_read", "manifest.tsv"), encoding="utf-8"), delimiter="\t")}
rows = []
for f in sorted(glob.glob(os.path.join(H, "agent_out", "B*.csv"))):
    rows += list(csv.DictReader(open(f, encoding="utf-8", newline="")))
gr = [r for r in rows if r["row_type"] == "grantee" and r["grantee"].strip()]
progs = collections.defaultdict(set)
for r in gr:
    progs[r["grantee"].strip()].add(r["program"][:40])
rec = [(g, {"total": "", "programs": "; ".join(sorted(p))}) for g, p in progs.items()]
out = ties.run(rec, "AG grant-program grantees named in the releases", os.path.join(H, "ties_grantees.tsv"))
print("\nlargest by donations + lobbying:")
for o in sorted(out, key=lambda o: -(o["ocpf"] + o["fec"] + o["lob_firm"] + o["lob_inhouse"]))[:22]:
    print(f"  {o['name'][:46]:46s} donations ${o['ocpf'] + o['fec']:>9,.0f}  lobbying ${o['lob_firm'] + o['lob_inhouse']:>10,.0f}  officials' ties {o['hold']:>3}  | {o['programs'][:60]}")

# program totals across the awards (not the launches), as stated
prog = [r for r in rows if r["row_type"] == "program" and man[r["release_id"]]["kind"] == "award"]
def num(x):
    try:
        return float(str(x).replace(",", "")) if str(x).strip() else 0.0
    except ValueError:
        return 0.0
tot = sum(num(r["amount"]) for r in prog if num(r["amount"]) < 100_000_000)
print(f"\nAG grant-program awards announced 2015-2026 (award releases only, excluding the $525M opioid abatement announcement): {len(prog)} releases, ${tot:,.0f}")
