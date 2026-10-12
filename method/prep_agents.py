"""Write clean text files for the single-state releases with a headline of $1M or more, and split them into batches for readers."""
import csv
import os
import re
import sys

H = os.environ.get("AG_SWEEP_WORK", "work")  # scratch folder for downloads and intermediate files
sys.path.insert(0, H)
from sweep2_lib import main_text  # noqa: E402

sel = list(csv.DictReader(open(os.path.join(H, "sweep-selected.tsv"), encoding="utf-8"), delimiter="\t"))
idx = {r["path"]: i for i, r in enumerate(sel)}
cl = [r for r in csv.DictReader(open(os.path.join(H, "sweep-classes.tsv"), encoding="utf-8"), delimiter="\t") if r["multistate"] == "0" and int(r["headline_dollars"]) >= 1_000_000]
cl.sort(key=lambda r: (r["date"][-4:], r["date"]))
os.makedirs(os.path.join(H, "read"), exist_ok=True)
manifest = []
for n, r in enumerate(cl, 1):
    raw = open(os.path.join(H, "rel", f"{idx[r['path']]:04d}.html"), encoding="utf-8", errors="replace").read()
    t = main_text(raw)
    t = re.sub(r"Office of (?:the )?Attorney General\s+(?:Office of (?:the )?Attorney General\s+)?(?:Media Contact|MEDIA CONTACT)[^.]{0,260}?(?:BOSTON|Boston)\s*[—–-]", "BOSTON —", t)
    fn = f"R{n:03d}.txt"
    with open(os.path.join(H, "read", fn), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(f"RELEASE_ID: R{n:03d}\nDATE: {r['date']}\nTITLE: {r['title']}\nURL: https://www.mass.gov{r['path']}\n---\n{t}\n")
    manifest.append((f"R{n:03d}", r["date"], r["title"], "https://www.mass.gov" + r["path"], len(t)))
with open(os.path.join(H, "read", "manifest.tsv"), "w", encoding="utf-8", newline="") as fh:
    w = csv.writer(fh, delimiter="\t", lineterminator="\n")
    w.writerow(["release_id", "date", "title", "url", "chars"])
    w.writerows(manifest)
print(len(manifest), "release text files written; median chars", sorted(m[4] for m in manifest)[len(manifest) // 2], "max", max(m[4] for m in manifest))
B = 6
per = (len(manifest) + B - 1) // B
for b in range(B):
    ids = [m[0] for m in manifest[b * per:(b + 1) * per]]
    print(f"batch {b + 1}: {ids[0]}..{ids[-1]} ({len(ids)})")
