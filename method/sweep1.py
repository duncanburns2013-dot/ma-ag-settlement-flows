"""Pick the settlement-type releases from the AG archive list and fetch each one (release page + the settlement documents it links)."""
import collections
import csv
import html
import os
import re
import subprocess
import time

H = os.environ.get("AG_SWEEP_WORK", "work")  # scratch folder for downloads and intermediate files
os.makedirs(os.path.join(H, "rel"), exist_ok=True)
rows = list(csv.DictReader(open(os.path.join(H, "ag-news-list.tsv"), encoding="utf-8"), delimiter="\t"))
MONEY = re.compile(r"\$\s?\d", re.I)
VERB = re.compile(r"settle|agree[sd]? to pay|to pay|pays?\b|paid|secure[sd]?|recover|resolv|judgment|order[sd]? to|refund|restitution|relief|penalt|fine[sd]?|reimburs|returns?\b|obtain", re.I)
NOT = re.compile(r"grant program|awards? \$|announces? .*grants?|receives? \$|coalition|comments|letter|amicus|brief|urges|sues|lawsuit against|files? (?:a )?(?:lawsuit|complaint|suit)|indict|charge[sd]|sentenc|convict|guilty", re.I)
cand = []
for r in rows:
    t = r["title"] + " " + r["description"]
    if MONEY.search(t) and VERB.search(t):
        cand.append(r)
# also settlements without a dollar figure in the headline
cand2 = [r for r in rows if r not in cand and re.search(r"settle|consent judgment|assurance of discontinuance|agrees? to", r["title"], re.I)]
print("archive list:", len(rows), " headline names money and a payment verb:", len(cand), " settlement without a dollar figure in the headline:", len(cand2))
sel = cand + cand2
by_year = collections.Counter(r["date"][-4:] for r in sel)
print("by year:", dict(sorted(by_year.items())))
with open(os.path.join(H, "sweep-selected.tsv"), "w", encoding="utf-8", newline="") as fh:
    w = csv.writer(fh, delimiter="\t", lineterminator="\n")
    w.writerow(["path", "date", "title"])
    for r in sel:
        w.writerow([r["path"], r["date"], r["title"]])

DOCSLUG = re.compile(r"consent|judgment|assurance|aod|settlement|agreement|stipulat|decree|order", re.I)
docs = []
for i, r in enumerate(sel):
    f = os.path.join(H, "rel", f"{i:04d}.html")
    if not os.path.exists(f) or os.path.getsize(f) < 5000:
        subprocess.run(["powershell", "-File", os.path.join(H, "massgov_get.ps1"), "-Url", "https://www.mass.gov" + r["path"], "-Out", f], capture_output=True, text=True)
        time.sleep(0.5)
    s = open(f, encoding="utf-8", errors="replace").read() if os.path.exists(f) else ""
    for l in sorted(set(re.findall(r'href="((?:https://www\.mass\.gov)?/doc/[^"#?]+)', s))):
        if DOCSLUG.search(l) and not re.search(r"complaint|letter|press|motion|brief|memo|petition", l, re.I):
            docs.append((i, r["date"], r["title"], r["path"], l if l.startswith("http") else "https://www.mass.gov" + l))
    if i % 100 == 0:
        print(f"fetched {i}/{len(sel)}; settlement-type documents so far {len(docs)}", flush=True)
with open(os.path.join(H, "sweep-docs.tsv"), "w", encoding="utf-8", newline="") as fh:
    w = csv.writer(fh, delimiter="\t", lineterminator="\n")
    w.writerow(["idx", "date", "title", "path", "doc_url"])
    w.writerows(docs)
print("done: releases fetched", len(sel), " settlement-type documents linked:", len(docs), " from", len({d[0] for d in docs}), "releases")
