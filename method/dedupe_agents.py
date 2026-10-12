import collections
import csv
import glob
import os
import re

H = os.environ.get("AG_SWEEP_WORK", "work")  # scratch folder for downloads and intermediate files
man = {r["release_id"]: r for r in csv.DictReader(open(os.path.join(H, "read", "manifest.tsv"), encoding="utf-8"), delimiter="\t")}
rows = []
for f in sorted(glob.glob(os.path.join(H, "agent_out", "A*.csv"))):
    rows += list(csv.DictReader(open(f, encoding="utf-8", newline="")))
S = [r for r in rows if r["kind"] == "settlement_or_judgment"]


def key(r):
    w = re.sub(r"[^a-z0-9 ]", "", r["defendant"].lower()).split()
    return (w[0] if w else "", )


groups = collections.defaultdict(list)
for r in S:
    groups[key(r)].append(r)
print("possible same-matter pairs (same first word of the defendant):")
for k, lst in groups.items():
    if len(lst) > 1:
        print(" ", k[0])
        for r in lst:
            m = man[r["release_id"]]
            print(f"     {r['release_id']} {m['date']:>10} ${float(r['headline_dollars'] or 0):>12,.0f}  {m['title'][:70]}")
dup_notes = [r for r in rows if re.search(r"duplicate|same matter|same as R", r.get("notes", ""), re.I)]
print("\nrows whose own notes mention a duplicate:", [(r["release_id"], r["notes"][:60]) for r in dup_notes])
