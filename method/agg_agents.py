import collections
import csv
import glob
import os
import re

H = os.environ.get("AG_SWEEP_WORK", "work")  # scratch folder for downloads and intermediate files
manifest = {r["release_id"]: r for r in csv.DictReader(open(os.path.join(H, "read", "manifest.tsv"), encoding="utf-8"), delimiter="\t")}
bad = {line.split("\t")[0] for line in open(os.path.join(H, "agent_problems.tsv"), encoding="utf-8") if line.strip()}
rows = []
for f in sorted(glob.glob(os.path.join(H, "agent_out", "A*.csv"))):
    rows += list(csv.DictReader(open(f, encoding="utf-8", newline="")))


def n(x):
    try:
        return float(str(x).replace(",", "")) if str(x).strip() else 0.0
    except ValueError:
        return 0.0


DUP = {"R078", "R137", "R087"}
S = [r for r in rows if r["kind"] == "settlement_or_judgment" and r["release_id"] not in bad and r["release_id"] not in DUP]
print(f"settlement/judgment rows passing every check: {len(S)} (of {sum(1 for r in rows if r['kind'] == 'settlement_or_judgment')} read; {sum(1 for r in rows if r['kind'] == 'settlement_or_judgment' and r['release_id'] in bad)} flagged and left out)")
H_ = sum(n(r["headline_dollars"]) for r in S)
cats = ["harmed", "state_penalties_costs", "state_agency_recovery", "designated"]
tot = {c: sum(n(r[c]) for r in S) for c in cats}
nonc = sum(n(r["noncash_relief"]) for r in S)
print(f"headline dollars: ${H_:,.0f}")
for c in cats:
    print(f"  stated as {c:24s} ${tot[c]:>14,.0f}  ({tot[c] * 100 / H_:5.1f}% of headline)")
print(f"  stated as noncash_relief (debt forgiveness etc.; not quote-verified) ${nonc:,.0f}")
stated = sum(tot.values())
print(f"  all four cash categories together: ${stated:,.0f} ({stated * 100 / H_:.1f}% of headline); not broken down in the release: ${H_ - stated - nonc:,.0f} ({(H_ - stated - nonc) * 100 / H_:.1f}%)")

anyc = [r for r in S if any(n(r[c]) for c in cats + ["noncash_relief"])]
nob = [r for r in S if not any(n(r[c]) for c in cats + ["noncash_relief"])]
print(f"\nreleases with any category stated: {len(anyc)} ({len(anyc) * 100 // len(S)}%); total only, no breakdown: {len(nob)}, headline ${sum(n(r['headline_dollars']) for r in nob):,.0f}")
comp = [r for r in S if n(r["headline_dollars"]) and abs(sum(n(r[c]) for c in cats + ['noncash_relief']) - n(r["headline_dollars"])) <= 0.03 * n(r["headline_dollars"])]
print(f"releases where stated parts account for the headline within 3%: {len(comp)}, headline ${sum(n(r['headline_dollars']) for r in comp):,.0f}")
ct = {c: sum(n(r[c]) for r in comp) for c in cats + ["noncash_relief"]}
ch = sum(ct.values())
for c, v in ct.items():
    print(f"    {c:24s} ${v:>13,.0f}  {v * 100 / ch:5.1f}%")

print("\nlargest settlements and what the release says:")
for r in sorted(S, key=lambda r: -n(r["headline_dollars"]))[:18]:
    m = manifest[r["release_id"]]
    print(f"  {m['date']:>10} {r['defendant'][:26]:26s} ${n(r['headline_dollars']):>13,.0f} harmed {n(r['harmed']):>12,.0f} state {n(r['state_penalties_costs']):>11,.0f} agency {n(r['state_agency_recovery']):>11,.0f} desig {n(r['designated']):>11,.0f}")

rec = collections.Counter()
recamt = collections.defaultdict(float)
for r in S:
    for name in [x.strip() for x in r["recipients_named"].split(";") if x.strip()]:
        rec[name] += 1
        recamt[name] += n(r["designated"])
print("\nnamed funds, programs and organizations that receive settlement money (count of settlements):")
for name, c in rec.most_common(25):
    print(f"  {c:2d}  {name[:70]}")

with open(os.path.join(H, "agent_clean.tsv"), "w", encoding="utf-8", newline="") as fh:
    w = csv.writer(fh, delimiter="\t", lineterminator="\n")
    cols = ["release_id", "date", "url", "kind", "defendant", "headline_dollars", "harmed", "noncash_relief", "state_penalties_costs", "state_agency_recovery", "designated", "unstated", "recipients_named", "quote_headline", "quote_harmed", "quote_state", "quote_state_agency", "quote_designated", "notes"]
    w.writerow(cols)
    for r in rows:
        m = manifest[r["release_id"]]
        w.writerow([r.get(c, "") if c not in ("date", "url") else (m["date"] if c == "date" else m["url"]) for c in cols] + [])
