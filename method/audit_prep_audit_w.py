"""Read set W: the Wayback-recovered releases (absent from the live archive listing). All fetched ones with money language, no title screen; the rest are logged."""
import csv
import os
import re
import sys

H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, H)
from sweep2_lib import amounts, main_text, sentences  # noqa: E402

rows = list(csv.DictReader(open(os.path.join(H, "cdx_releases.tsv"), encoding="utf-8"), delimiter="\t"))
SETTLE = re.compile(r"settle|agree[sd]? to pay|restitution|refund|penalt|judgment|consent|assurance of discontinuance|ordered to pay|will pay|\bto pay\b|\bpays?\b|recover|secure[sd]?|resolv|reimburs|forfeit|disgorg|damages|\bfine[sd]?\b|debt relief|payout", re.I)
manifest = list(csv.DictReader(open(os.path.join(H, "audit_read", "manifest.tsv"), encoding="utf-8"), delimiter="\t"))
have = {m["release_id"] for m in manifest}
cands, nomoney, failed = [], [], []
for r in rows:
    if r["source"] == "FAILED":
        failed.append(r)
        continue
    f = os.path.join(H, "cdx_rel", f"{int(r['idx']):03d}.html")
    t = main_text(open(f, encoding="utf-8", errors="replace").read())
    t = t.split("Help Us Improve Mass.gov")[0]
    best = 0
    for s in sentences(t):
        am = amounts(s)
        if am and max(am) >= 100000 and SETTLE.search(s):
            best = max(best, max(am))
    date = r["date"] or ""
    # date may be missing when the capture lacks the 'For immediate release' line; take it from the first date in the text
    if not date:
        m = re.search(r"\b(\d{1,2}/\d{1,2}/20\d\d)\b", t)
        date = m.group(1) if m else ""
    (cands if best else nomoney).append((r, date, t, best))
print("recovered releases:", len(rows) - len(failed), " with a >=$100K settlement-type sentence:", len(cands), " without:", len(nomoney), " failed to fetch:", len(failed))
print("failed:")
for r in failed:
    print("  ", r["path"][:110])
cands.sort(key=lambda c: (c[1][-4:], c[1]))
os.makedirs(os.path.join(H, "audit_read"), exist_ok=True)
new = []
for n, (r, date, t, best) in enumerate(cands, 1):
    rid = f"W{n:03d}"
    title = r["title"]
    open(os.path.join(H, "audit_read", rid + ".txt"), "w", encoding="utf-8", newline="\n").write(f"RELEASE_ID: {rid}\nDATE: {date}\nTITLE: {title}\nURL: https://www.mass.gov{r['path']}\n---\n{t}\n")
    new.append((rid, date, title, "https://www.mass.gov" + r["path"], len(t), "cdx", best))
    print(f"  {rid} {date:>10} ${best:>12,.0f} | {title[:85]}")
with open(os.path.join(H, "audit_read", "manifest.tsv"), "a", encoding="utf-8", newline="") as fh:
    w = csv.writer(fh, delimiter="\t", lineterminator="\n")
    for row in new:
        if row[0] not in have:
            w.writerow(row)
print("appended", len(new), "to the audit manifest")
print("not read (no money language):")
for r, date, t, best in nomoney:
    print("  ", date, "|", r["title"][:90])
