"""Read set for grant announcements missing from the earlier grants register."""
import csv
import glob
import os
import re
import sys

H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, H)
from sweep2_lib import main_text  # noqa: E402
import verify_audit as v  # noqa: E402

man, rows, clean, problems = v.run(quiet=True)
known = set()
for f in glob.glob(os.path.join(H, "grants_read", "G*.txt")):
    m = re.search(r"^URL:\s*(\S+)", open(f, encoding="utf-8").read(), re.M)
    if m:
        known.add(m.group(1).replace("https://www.mass.gov", ""))
items = []  # (path, date, title, text)
for r in clean:
    if r["kind"] == "grant_or_funding":
        m = man[r["release_id"]]
        p = m["url"].replace("https://www.mass.gov", "")
        if p not in known:
            t = open(os.path.join(H, "audit_read", r["release_id"] + ".txt"), encoding="utf-8").read().split("\n---\n", 1)[1]
            items.append((p, m["date"], m["title"], t))
EXC = re.compile(r"Sues|Challenges|Joins|Indictment|Co-Leads|Statement|Protects Access|Wins Ruling|Secures Victory|Lawsuit|Receives|Awarded \$1\.7|Asks Court|Webinar|Parents. Choice|Releases", re.I)
src = {}
for i, r in enumerate(csv.DictReader(open(os.path.join(H, "sweep-selected.tsv"), encoding="utf-8"), delimiter="\t")):
    src[r["path"]] = os.path.join(H, "rel", f"{i:04d}.html")
for r in csv.DictReader(open(os.path.join(H, "unselected.tsv"), encoding="utf-8"), delimiter="\t"):
    src[r["path"]] = os.path.join(H, "rel_unsel", f"{int(r['idx']):04d}.html")
have = {i[0] for i in items}
for r in csv.DictReader(open(os.path.join(H, "grants_scan_new.tsv"), encoding="utf-8"), delimiter="\t"):
    if EXC.search(r["title"]) or r["path"] in have:
        continue
    t = main_text(open(src[r["path"]], encoding="utf-8", errors="replace").read())
    items.append((r["path"], r["date"], r["title"], t))
items.sort(key=lambda x: (x[1][-4:], x[1]))
os.makedirs(os.path.join(H, "grants_read2"), exist_ok=True)
mf = []
for n, (p, d, t, body) in enumerate(items, 1):
    rid = f"K{n:03d}"
    open(os.path.join(H, "grants_read2", rid + ".txt"), "w", encoding="utf-8", newline="\n").write(f"RELEASE_ID: {rid}\nDATE: {d}\nTITLE: {t}\nURL: https://www.mass.gov{p}\n---\n{body}\n")
    mf.append((rid, d, t, "https://www.mass.gov" + p, len(body)))
with open(os.path.join(H, "grants_read2", "manifest.tsv"), "w", encoding="utf-8", newline="") as fh:
    w = csv.writer(fh, delimiter="\t", lineterminator="\n")
    w.writerow(["release_id", "date", "title", "url", "chars"])
    w.writerows(mf)
print(len(mf), "grant announcements to read: K001..K%03d" % len(mf))
for m in mf:
    print(" ", m[0], m[1], m[2][:80])
