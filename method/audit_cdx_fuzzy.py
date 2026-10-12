"""Which Wayback-captured AG slugs have no counterpart in the live listing once slug truncation and -N suffixes are normalised?"""
import csv
import os
import re

H = os.environ.get("AG_SWEEP_WORK", ".")
lst = [r for r in csv.DictReader(open(os.path.join(H, "ag-news-list.tsv"), encoding="utf-8"), delimiter="\t")]
miss = [ln.strip() for ln in open(os.path.join(H, "cdx_not_in_listing.txt"), encoding="utf-8") if ln.strip()]
K = 70


def key(p):
    s = p.replace("/news/", "")
    s = re.sub(r"-\d+$", "", s)
    return s[:K]


lkeys = {key(r["path"]) for r in lst}
lfull = [r["path"].replace("/news/", "") for r in lst]
unmatched = []
for p in miss:
    k = key(p)
    if k in lkeys:
        continue
    s = p.replace("/news/", "")
    # also allow the listing slug to be a prefix-extension or the capture to be a prefix of a listing slug
    if any(f.startswith(s[:60]) or s.startswith(f[:60]) for f in lfull):
        continue
    unmatched.append(p)
print("captured paths not in listing (raw):", len(miss))
print("after normalising truncation and -N suffixes, still unmatched:", len(unmatched))
with open(os.path.join(H, "cdx_unmatched.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(unmatched))
for p in unmatched[:60]:
    print("  ", p)
