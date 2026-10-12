"""Crawl the Attorney General's news archive on mass.gov, page by page, into one list."""
import csv
import html
import os
import re
import subprocess
import sys
import time

H = os.environ.get("AG_SWEEP_WORK", "work")  # scratch folder for downloads and intermediate files
os.makedirs(os.path.join(H, "pages"), exist_ok=True)
out = os.path.join(H, "ag-news-list.tsv")
seen, rows, empty = set(), [], 0
page = 0
while page < 900 and empty < 3:
    f = os.path.join(H, "pages", f"p{page:04d}.html")
    if not os.path.exists(f) or os.path.getsize(f) < 5000:
        url = "https://www.mass.gov/orgs/office-of-the-attorney-general/news" + (f"?page={page}" if page else "")
        subprocess.run(["powershell", "-File", os.path.join(H, "massgov_get.ps1"), "-Url", url, "-Out", f], capture_output=True, text=True)
        time.sleep(0.6)
    s = open(f, encoding="utf-8", errors="replace").read() if os.path.exists(f) else ""
    items = re.findall(r'<section class="ma__press-teaser[^"]*">(.*?)</section>', s, re.S)
    n_new = 0
    for it in items:
        m = re.search(r'href="(/news/[^"]+)"', it)
        if not m or m.group(1) in seen:
            continue
        seen.add(m.group(1))
        title = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", re.search(r'ma__press-teaser__title">(.*?)</h2>', it, re.S).group(1)))).strip() if re.search(r'ma__press-teaser__title">(.*?)</h2>', it, re.S) else ""
        d = re.search(r'ma__press-teaser__date">\s*([\d/]+)', it)
        desc = re.search(r'ma__press-teaser__description">(.*?)</div>\s*</div>', it, re.S)
        desc = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", desc.group(1)))).strip() if desc else ""
        rows.append((m.group(1), d.group(1) if d else "", title, desc[:400]))
        n_new += 1
    empty = empty + 1 if n_new == 0 else 0
    if page % 20 == 0:
        print(f"page {page}: {n_new} new, {len(rows)} total, last date {rows[-1][1] if rows else ''}", flush=True)
    page += 1
with open(out, "w", encoding="utf-8", newline="") as fh:
    w = csv.writer(fh, delimiter="\t", lineterminator="\n")
    w.writerow(["path", "date", "title", "description"])
    w.writerows(rows)
print("pages crawled:", page, " releases listed:", len(rows), " oldest:", rows[-1][1] if rows else "", " newest:", rows[0][1] if rows else "")
