"""Check the readers' work: each quote must appear in its release, each recorded amount must appear in its quote, parts must not exceed the headline."""
import collections
import csv
import glob
import os
import re
import sys

H = os.environ.get("AG_SWEEP_WORK", "work")  # scratch folder for downloads and intermediate files
sys.path.insert(0, H)
from sweep2_lib import amounts  # noqa: E402

PARTS = [("harmed", "quote_harmed"), ("noncash_relief", "quote_harmed"), ("state_penalties_costs", "quote_state"),
         ("state_agency_recovery", "quote_state_agency"), ("designated", "quote_designated")]


def norm(s):
    s = (s or "").replace("\u2019", "'").replace("\u2018", "'").replace("\u201c", '"').replace("\u201d", '"').replace("\u2013", "-").replace("\u2014", "-").replace("\xa0", " ")
    return re.sub(r"\s+", " ", s).strip().lower()


def num(x):
    x = (x or "").strip().replace(",", "").replace("$", "")
    try:
        return float(x) if x else None
    except ValueError:
        return None


manifest = {r["release_id"]: r for r in csv.DictReader(open(os.path.join(H, "read", "manifest.tsv"), encoding="utf-8"), delimiter="\t")}
rows, problems = [], []
for f in sorted(glob.glob(os.path.join(H, "agent_out", "A*.csv"))):
    for r in csv.DictReader(open(f, encoding="utf-8", newline="")):
        r["_file"] = os.path.basename(f)
        rows.append(r)
ids = [r["release_id"] for r in rows]
dups = [k for k, v in collections.Counter(ids).items() if v > 1]
missing = sorted(set(manifest) - set(ids))
print(f"rows: {len(rows)} of {len(manifest)} releases; duplicates: {dups}; missing: {missing}")

src_cache = {}
def source(rid):
    if rid not in src_cache:
        p = os.path.join(H, "read", f"{rid}.txt")
        src_cache[rid] = norm(open(p, encoding="utf-8").read()) if os.path.exists(p) else ""
    return src_cache[rid]

clean = []
for r in rows:
    rid = r["release_id"]
    bad = []
    if rid not in manifest:
        problems.append((rid, "unknown release id"))
        continue
    src = source(rid)
    head = num(r["headline_dollars"]) or 0
    if head:
        q = r.get("quote_headline", "")
        if not q or norm(q) not in src:
            bad.append("headline quote missing or not verbatim")
        elif not any(abs(a - head) <= max(1, head * 0.005) for a in amounts(q)):
            bad.append("headline amount not in its quote")
    tot = 0.0
    for col, qcol in PARTS:
        v = num(r.get(col))
        if v is None:
            continue
        tot += v
        q = r.get(qcol, "")
        if not q or norm(q) not in src:
            bad.append(f"{col}: quote missing or not verbatim")
        elif not any(abs(a - v) <= max(1, v * 0.005) for a in amounts(q)):
            bad.append(f"{col}: amount not in the quote")
    if head and tot > head * 1.02:
        bad.append(f"parts {tot:,.0f} exceed headline {head:,.0f}")
    if bad:
        problems.append((rid, "; ".join(bad)))
    else:
        clean.append(r)
print(f"rows passing every check: {len(clean)}; rows with a problem: {len(problems)}")
for rid, b in problems[:60]:
    print("  ", rid, manifest.get(rid, {}).get("title", "")[:50], "|", b[:150])
with open(os.path.join(H, "agent_problems.tsv"), "w", encoding="utf-8", newline="") as fh:
    w = csv.writer(fh, delimiter="\t", lineterminator="\n")
    w.writerows(problems)
print("kinds:", dict(collections.Counter(r["kind"] for r in rows)))
