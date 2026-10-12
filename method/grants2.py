import csv
import os
import re
import subprocess
import sys
import time

H = os.environ.get("AG_SWEEP_WORK", "work")  # scratch folder for downloads and intermediate files
sys.path.insert(0, H)
from sweep2_lib import main_text  # noqa: E402

rows = list(csv.DictReader(open(os.path.join(H, "grant-releases.tsv"), encoding="utf-8"), delimiter="\t"))
sel = [r for r in rows if re.search(r"Awards|Distributes|Receive|Grant(?:ee)? Recipients|Celebrate", r["title"], re.I)
       and not re.search(r"Opens|Launch|Statement|Trump|Department Of Education|Governor|Application", r["title"], re.I)]
# the grant-program launches also name the funding settlements; keep them too as context
launch = [r for r in rows if r not in sel and re.search(r"Launch|Announces .*Grant|New Grant|Opens", r["title"], re.I) and not re.search(r"Statement|Trump|Governor|Education Grants|Arrested|Foxborough", r["title"], re.I)]
print("award/distribution releases:", len(sel), " program launch releases:", len(launch))
os.makedirs(os.path.join(H, "grants_read"), exist_ok=True)
man = []
for k, r in enumerate(sel + launch, 1):
    f = os.path.join(H, "grants_raw", f"{k:03d}.html")
    os.makedirs(os.path.dirname(f), exist_ok=True)
    if not os.path.exists(f) or os.path.getsize(f) < 5000:
        subprocess.run(["powershell", "-File", os.path.join(H, "massgov_get.ps1"), "-Url", "https://www.mass.gov" + r["path"], "-Out", f], capture_output=True, text=True)
        time.sleep(0.5)
    raw = open(f, encoding="utf-8", errors="replace").read() if os.path.exists(f) else ""
    t = main_text(raw)
    gid = f"G{k:03d}"
    kind = "award" if r in sel else "launch"
    with open(os.path.join(H, "grants_read", gid + ".txt"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(f"RELEASE_ID: {gid}\nDATE: {r['date']}\nTITLE: {r['title']}\nURL: https://www.mass.gov{r['path']}\nKIND: {kind}\n---\n{t}\n")
    man.append((gid, r["date"], r["title"], "https://www.mass.gov" + r["path"], kind, len(t)))
with open(os.path.join(H, "grants_read", "manifest.tsv"), "w", encoding="utf-8", newline="") as fh:
    w = csv.writer(fh, delimiter="\t", lineterminator="\n")
    w.writerow(["release_id", "date", "title", "url", "kind", "chars"])
    w.writerows(man)
print(len(man), "written; chars median", sorted(m[5] for m in man)[len(man) // 2], "max", max(m[5] for m in man))
