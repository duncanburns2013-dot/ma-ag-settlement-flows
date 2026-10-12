import csv
import os
import re

H = os.environ.get("AG_SWEEP_WORK", "work")  # scratch folder for downloads and intermediate files
rows = list(csv.DictReader(open(os.path.join(H, "ag-news-list.tsv"), encoding="utf-8"), delimiter="\t"))
G = re.compile(r"grant(?:s| program| fund)?|awards?\b|distribut\w+ \$|funding to|\bfunds? (?:for|to) (?:community|local|programs)|community program|support(?:s|ing)? (?:local|community|organizations|programs)", re.I)
NOT = re.compile(r"charged|sentenc|indict|arraign|trafficking|firearm|sues|lawsuit|files? (?:a )?(?:brief|comments)|coalition|urges|amicus|Trump|federal", re.I)
hit = [r for r in rows if G.search(r["title"]) and re.search(r"\$\s?\d", r["title"] + " " + r["description"]) and not NOT.search(r["title"])]
print("AG announcements about grants or awards with a dollar figure:", len(hit))
for r in hit:
    print(f"{r['date']:>10}  {r['title'][:130]}")
with open(os.path.join(H, "grant-releases.tsv"), "w", encoding="utf-8", newline="") as fh:
    w = csv.writer(fh, delimiter="\t", lineterminator="\n")
    w.writerow(["path", "date", "title"])
    for r in hit:
        w.writerow([r["path"], r["date"], r["title"]])
