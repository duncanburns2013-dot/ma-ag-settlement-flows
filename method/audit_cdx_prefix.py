"""Enumerate captured AG news pages (slugs starting ag-) from both Wayback CDX endpoints; diff against the live listing."""
import csv
import os
import re
import subprocess

H = os.environ.get("AG_SWEEP_WORK", ".")
lst = {r["path"] for r in csv.DictReader(open(os.path.join(H, "ag-news-list.tsv"), encoding="utf-8"), delimiter="\t")}
ENDPOINTS = {
    "web.archive.org": "https://web.archive.org/cdx/search/cdx?url=mass.gov/news/ag-&matchType=prefix&output=txt&fl=original&collapse=urlkey&filter=statuscode:200&limit=20000",
    "archive-it": "https://wayback.archive-it.org/1101/timemap/cdx?url=https://www.mass.gov/news/ag-&matchType=prefix&output=txt&fl=original&collapse=urlkey&limit=20000",
}
allp = {}
for name, u in ENDPOINTS.items():
    r = subprocess.run(["curl.exe", "-s", "-k", "--max-time", "180", u], capture_output=True, text=True)
    paths = set()
    for ln in r.stdout.splitlines():
        m = re.search(r"mass\.gov(/news/[^\s?#]+)", ln)
        if m:
            paths.add(m.group(1).rstrip("/"))
    print(f"{name}: http-ok bytes={len(r.stdout)} distinct /news/ paths={len(paths)}")
    allp[name] = paths
union = set().union(*allp.values())
missing = sorted(p for p in union if p not in lst)
print("union:", len(union), " in live listing:", len(union) - len(missing), " NOT in live listing:", len(missing))
with open(os.path.join(H, "cdx_not_in_listing.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(missing))
for p in missing[:25]:
    print("  ", p[:120])
