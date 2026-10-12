"""Compare the blind second reading with the first reading, field by field."""
import collections
import csv
import glob
import os
import sys

H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, H)
from verify_audit import norm, num  # noqa: E402
import verify_audit as v  # noqa: E402

key = {r["blind_id"]: r for r in csv.DictReader(open(os.path.join(H, "blind_read", "key.tsv"), encoding="utf-8"), delimiter="\t")}
first = {}
for pat in ("A*.csv", "U*.csv"):
    for f in glob.glob(os.path.join(H, "agent_out", pat)):
        for r in csv.DictReader(open(f, encoding="utf-8", newline="")):
            first[r["release_id"]] = r
second = {}
for f in glob.glob(os.path.join(H, "agent_out", "V*.csv")):
    for r in csv.DictReader(open(f, encoding="utf-8", newline="")):
        second[r["release_id"]] = r
print("blind rows:", len(second), "of", len(key))
# verify the blind quotes with the same checks (point verifier at blind_read)
src = {}
bad = 0
for rid, r in second.items():
    s = norm(open(os.path.join(H, "blind_read", rid + ".txt"), encoding="utf-8").read())
    problems = []
    for col, qcol in v.VALS + v.PARTS:
        val, q = num(r.get(col)), r.get(qcol, "")
        if q and norm(q) not in s:
            problems.append(qcol)
        if val is not None and (not q or not v.hit(val, q)):
            problems.append(col)
    bad += bool(problems)
print("blind rows failing the quote check:", bad)
FIELDS = ["headline_dollars", "harmed", "noncash_relief", "state_penalties_costs", "state_agency_recovery", "designated"]
tally = {f: collections.Counter() for f in FIELDS}
kinds = collections.Counter()
absdiff = collections.Counter()
valsum = collections.Counter()
diffs = []
for bid, k in key.items():
    if bid not in second or k["original_id"] not in first:
        continue
    a, b = first[k["original_id"]], second[bid]
    ka = "settlement" if a["kind"] in ("settlement_or_judgment", "single_state_settlement") else a["kind"]
    kb = "settlement" if b["kind"] in ("single_state_settlement", "multistate_settlement") else b["kind"]
    kinds[(ka == kb)] += 1
    if ka != kb:
        diffs.append((bid, k["original_id"], "kind", a["kind"], b["kind"]))
        continue
    for f in FIELDS:
        x, y = num(a.get(f)), num(b.get(f))
        if x is None and y is None:
            tally[f]["both blank"] += 1
        elif x is None or y is None:
            tally[f]["one reader blank"] += 1
            diffs.append((bid, k["original_id"], f, x, y))
        elif abs(x - y) <= max(1, 0.005 * max(x, y)):
            tally[f]["agree"] += 1
        else:
            tally[f]["differ"] += 1
            diffs.append((bid, k["original_id"], f, x, y))
        absdiff[f] += abs((x or 0) - (y or 0))
        valsum[f] += max(x or 0, y or 0)
print("kind agreement (settlement vs not):", dict(kinds))
for f in FIELDS:
    t = tally[f]
    n = sum(t.values())
    nb = n - t["both blank"]
    print(f"  {f:24s} agree {t['agree']:3d} | one blank {t['one reader blank']:3d} | differ {t['differ']:3d} | both blank {t['both blank']:3d}   dollar disagreement {absdiff[f] * 100 / max(1, valsum[f]):5.1f}% of dollars")
print("\ndisagreements:")
for d in diffs[:60]:
    print("  ", d)
