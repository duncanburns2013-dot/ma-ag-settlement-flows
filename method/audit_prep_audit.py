"""Build the audit read set: every release body from ANY source (selected, unselected, Wayback-found) that carries a >=$100K amount in a
settlement-type sentence and was not already read in the R (single-state >=$1M) or M (multistate) passes."""
import csv
import os
import re
import sys

H = os.environ.get("AG_SWEEP_WORK", ".")
sys.path.insert(0, H)
from sweep2_lib import amounts, main_text, sentences  # noqa: E402

SETTLE = re.compile(r"settle|agree[sd]? to pay|restitution|refund|penalt|judgment|consent (decree|judgment)|assurance of discontinuance|ordered to pay|"
                    r"will pay|\bto pay\b|\bpays?\b|recover|secure[sd]?|resolv|resolution|reimburs|forfeit|disgorg|damages|\bfine[sd]?\b|debt relief|payout", re.I)


def tsv(name):
    return list(csv.DictReader(open(os.path.join(H, name), encoding="utf-8"), delimiter="\t"))


def url_key(p):
    return p.replace("https://www.mass.gov", "").strip()


read_urls = set()
for m in ("read/manifest.tsv", "multi_read/manifest.tsv"):
    for r in tsv(m):
        read_urls.add(url_key(r["url"]))
print("already read (R+M):", len(read_urls))

sources = []
for i, r in enumerate(tsv("sweep-selected.tsv")):
    sources.append(("sel", r["path"], r["date"], r["title"], os.path.join(H, "rel", f"{i:04d}.html")))
for r in tsv("unselected.tsv"):
    sources.append(("unsel", r["path"], r["date"], r["title"], os.path.join(H, "rel_unsel", f"{int(r['idx']):04d}.html")))
cdxp = os.path.join(H, "cdx_releases.tsv")
if os.path.exists(cdxp):
    for r in tsv("cdx_releases.tsv"):
        sources.append(("cdx", r["path"], r["date"], r["title"], os.path.join(H, "cdx_rel", f"{int(r['idx']):03d}.html")))

cands, nobody = [], 0
for src, path, date, title, f in sources:
    if url_key(path) in read_urls:
        continue
    if not (os.path.exists(f) and os.path.getsize(f) > 5000):
        nobody += 1
        continue
    t = main_text(open(f, encoding="utf-8", errors="replace").read())
    t = re.sub(r"Office of (?:the )?Attorney General\s+(?:Office of (?:the )?Attorney General\s+)?(?:Media Contact|MEDIA CONTACT)[^.]{0,260}?(?:BOSTON|Boston)\s*[—–-]", "BOSTON —", t)
    best = 0
    for s in sentences(t):
        am = amounts(s)
        if am and max(am) >= 100000 and SETTLE.search(s):
            best = max(best, max(am))
    if best:
        cands.append((src, path, date, title, best, t))
print("bodies missing (not fetched/too small):", nobody, " candidates:", len(cands), " by source:", {s: sum(1 for c in cands if c[0] == s) for s in ("sel", "unsel", "cdx")})
cands.sort(key=lambda c: (c[2][-4:], c[2]))
os.makedirs(os.path.join(H, "audit_read"), exist_ok=True)
man = []
for n, (src, path, date, title, best, t) in enumerate(cands, 1):
    rid = f"U{n:03d}"
    with open(os.path.join(H, "audit_read", rid + ".txt"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(f"RELEASE_ID: {rid}\nDATE: {date}\nTITLE: {title}\nURL: https://www.mass.gov{path}\n---\n{t}\n")
    man.append((rid, date, title, "https://www.mass.gov" + path, len(t), src, best))
with open(os.path.join(H, "audit_read", "manifest.tsv"), "w", encoding="utf-8", newline="") as fh:
    w = csv.writer(fh, delimiter="\t", lineterminator="\n")
    w.writerow(["release_id", "date", "title", "url", "chars", "source", "max_amount"])
    w.writerows(man)
print("median chars", sorted(m[4] for m in man)[len(man) // 2], "max", max(m[4] for m in man))
B = max(1, round(len(man) / 50))
per = (len(man) + B - 1) // B
for b in range(B):
    ids = [m[0] for m in man[b * per:(b + 1) * per]]
    print(f"batch {b + 1}: {ids[0]}..{ids[-1]} ({len(ids)})")
