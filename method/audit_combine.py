"""Combine the audit readings (U) with the first-sweep single-state readings (R) and report destinations of settlement dollars."""
import collections
import csv
import glob
import os
import re
import sys

H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, H)
import verify_audit as v  # noqa: E402

man, urows, clean, problems = v.run(quiet=True)
n = v.num
CATS = ["harmed", "state_penalties_costs", "state_agency_recovery", "designated"]
DUP_U = {"U060": "follow-up of R006 (Just Energy $4M matter)", "U347": "earlier announcement of M174 (opioid distributors, $525M)", "U079": "earlier release of R045 (QBE Insurance matter)", "W019": "same release as M083 (UBS $68M, retitled on the live site)"}
CIT = re.compile(r"\bcit(?:e|es|ed|ation|ations)\b", re.I)


def f(x):
    return n(x) or 0.0


# U set
U = []
for r in clean:
    if r["kind"] != "single_state_settlement" or r["release_id"] in DUP_U:
        continue
    r = dict(r)
    r["_head"] = f(r["headline_dollars"])
    r["_citation"] = bool(CIT.search(man[r["release_id"]]["title"]))
    U.append(r)
print(f"audit single-state settlements counted: {len(U)} (left out as repeats of matters already counted: {sorted(DUP_U)})")
print(f"  of which titled as citations: {sum(1 for r in U if r['_citation'])}; without a stated headline: {sum(1 for r in U if not r['_head'])}")

# R set
rman = {r["release_id"]: r for r in csv.DictReader(open(os.path.join(H, "read", "manifest.tsv"), encoding="utf-8"), delimiter="\t")}
bad = {ln.split("\t")[0] for ln in open(os.path.join(H, "agent_problems.tsv"), encoding="utf-8") if ln.strip()}
R = []
for fn in sorted(glob.glob(os.path.join(H, "agent_out", "A*.csv"))):
    for r in csv.DictReader(open(fn, encoding="utf-8", newline="")):
        if r["kind"] == "settlement_or_judgment" and r["release_id"] not in bad and r["release_id"] not in {"R078", "R137", "R087"}:
            r["_head"] = f(r["headline_dollars"])
            R.append(r)
print(f"first-sweep single-state settlements counted (>= $1M tier): {len(R)}")


PEN = re.compile(r"penalt|fines?|fees?|costs?|civil|investigat|assess", re.I)


def state_split(S):
    pen = unspec = 0.0
    for r in S:
        v_ = f(r["state_penalties_costs"])
        if not v_:
            continue
        if PEN.search(r.get("quote_state", "")):
            pen += v_
        else:
            unspec += v_
    return pen, unspec


def report(label, S, with_head_only=True):
    S = [r for r in S if r["_head"]] if with_head_only else S
    H_ = sum(r["_head"] for r in S)
    tot = {c: sum(f(r[c]) for r in S) for c in CATS}
    nonc = sum(f(r["noncash_relief"]) for r in S)
    stated = sum(tot.values())
    anyc = [r for r in S if any(f(r[c]) for c in CATS + ["noncash_relief"])]
    comp = [r for r in S if abs(sum(f(r[c]) for c in CATS + ["noncash_relief"]) - r["_head"]) <= 0.03 * r["_head"]]
    print(f"\n== {label}: {len(S)} settlements with a stated headline, ${H_:,.0f}")
    for c in CATS:
        print(f"   {c:24s} ${tot[c]:>14,.0f}  {tot[c] * 100 / H_:5.1f}%")
    pen, unspec = state_split(S)
    print(f"      of which the release calls it a penalty, fine, fee or cost: ${pen:,.0f} ({pen * 100 / H_:.1f}%); paid to the Commonwealth with no stated purpose: ${unspec:,.0f} ({unspec * 100 / H_:.1f}%)")
    print(f"   noncash_relief           ${nonc:>14,.0f}  {nonc * 100 / H_:5.1f}%")
    print(f"   no breakdown in the release ${H_ - stated - nonc:>11,.0f}  {(H_ - stated - nonc) * 100 / H_:5.1f}%   (releases with any category stated: {len(anyc)} of {len(S)})")
    ch = sum(f(r[c]) for r in comp for c in CATS + ["noncash_relief"])
    if comp:
        print(f"   {len(comp)} settlements whose parts reconcile to the headline within 3% (${sum(r['_head'] for r in comp):,.0f}):", end=" ")
        print(", ".join(f"{c.split('_')[0]} {sum(f(r[c]) for r in comp) * 100 / ch:.1f}%" for c in CATS + ["noncash_relief"]))
    return S


report("AUDIT SET (U), all", U)
report("AUDIT SET (U), excluding citations", [r for r in U if not r["_citation"]])
report("AUDIT SET (U), from the 90 releases the title filter skipped", [r for r in U if man[r["release_id"]]["source"] == "unsel"])
report("FIRST SWEEP (R), >= $1M", R)
report("COMBINED (R + U)", R + U)

# multistate additions
MS = [r for r in clean if r["kind"] == "multistate_settlement" and r["release_id"] not in DUP_U]
print(f"multistate settlements found by the audit: {len(MS)}; with a Massachusetts amount: {sum(1 for r in MS if f(r['ma_amount']))}; Massachusetts total ${sum(f(r['ma_amount']) for r in MS):,.0f}")
for r in sorted(MS, key=lambda r: -f(r["ma_amount"])):
    m = man[r["release_id"]]
    print(f"   {r['release_id']} {m['date']:>10} {r['defendant'][:28]:28s} nat ${f(r['national_total']):>13,.0f} MA ${f(r['ma_amount']):>11,.0f} {r['ma_destination_class']:12s} {r['ma_destination_detail'][:60]}")

# who is named as recipient in the audit set
rec = collections.Counter()
for r in U:
    for name in [x.strip() for x in r["recipients_named"].split(";") if x.strip()]:
        rec[name] += 1
print("\nnamed funds/organizations receiving money in the audit set (count of settlements):")
for name, c in rec.most_common(20):
    print(f"  {c:2d}  {name[:80]}")

# register
with open(os.path.join(H, "audit_register.tsv"), "w", encoding="utf-8", newline="") as fh:
    w = csv.writer(fh, delimiter="\t", lineterminator="\n")
    w.writerow(["release_id", "date", "url", "source_of_release", "kind", "defendant", "headline_dollars", "harmed", "noncash_relief", "state_penalties_costs", "state_agency_recovery", "designated", "recipients_named", "quote_headline", "quote_harmed", "quote_state", "quote_state_agency", "quote_designated", "status", "notes"])
    for r in urows:
        m = man[r["release_id"]]
        st = "counted" if r["kind"] == "single_state_settlement" and r["release_id"] not in DUP_U else ("left out: " + DUP_U[r["release_id"]] if r["release_id"] in DUP_U else "not a single-state settlement (" + r["kind"] + ")")
        w.writerow([r["release_id"], m["date"], m["url"], m["source"], r["kind"], r["defendant"], r["headline_dollars"], r["harmed"], r["noncash_relief"], r["state_penalties_costs"], r["state_agency_recovery"], r["designated"], r["recipients_named"], r["quote_headline"], r["quote_harmed"], r["quote_state"], r["quote_state_agency"], r["quote_designated"], st, r["notes"]])
print("\nwrote audit_register.tsv:", len(urows), "rows")
