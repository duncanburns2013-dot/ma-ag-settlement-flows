"""Fetch the settlement documents linked from the sweep releases and extract their text layer."""
import csv
import os
import subprocess
import threading
import time
from concurrent.futures import ThreadPoolExecutor

import fitz  # PyMuPDF

H = os.path.dirname(os.path.abspath(__file__))
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
rows = list(csv.DictReader(open(os.path.join(H, "sweep-docs.tsv"), encoding="utf-8"), delimiter="\t"))
out = os.path.join(H, "sweep_docs")
os.makedirs(out, exist_ok=True)
res = {}
lock = threading.Lock()


def get(i):
    r = rows[i]
    url = r["doc_url"].rstrip("/")
    if not url.endswith("/download"):
        url += "/download"
    f = os.path.join(out, f"{i:03d}.bin")
    for attempt in range(3):
        subprocess.run(["curl.exe", "-sS", "-L", "--compressed", "--ssl-no-revoke", "-m", "120", "-o", f, "-H", f"User-Agent: {UA}", "-H", "Accept: */*",
                        "-H", "Accept-Language: en-US,en;q=0.9", "-H", "Referer: https://www.mass.gov/", "-H", "Sec-Fetch-Dest: empty", "-H", "Sec-Fetch-Mode: cors",
                        "-H", "Sec-Fetch-Site: same-origin", url], capture_output=True)
        if os.path.exists(f) and os.path.getsize(f) > 1000:
            break
        time.sleep(2)
    kind, chars, pages = "missing", 0, 0
    if os.path.exists(f) and os.path.getsize(f) > 1000:
        head = open(f, "rb").read(8)
        if head.startswith(b"%PDF"):
            try:
                d = fitz.open(f)
                pages = d.page_count
                t = "\n".join(p.get_text() for p in d)
                open(os.path.join(out, f"{i:03d}.txt"), "w", encoding="utf-8").write(t)
                chars = len(t.strip())
                kind = "pdf-text" if chars >= 800 else "pdf-scanned"
            except Exception as e:  # noqa: BLE001
                kind = "pdf-error"
        else:
            kind = "not-pdf"
    time.sleep(0.3)
    with lock:
        res[i] = (kind, chars, pages)
        if len(res) % 20 == 0:
            print(f"{len(res)}/{len(rows)}", flush=True)


with ThreadPoolExecutor(max_workers=3) as ex:
    list(ex.map(get, range(len(rows))))
with open(os.path.join(H, "sweep-docs-status.tsv"), "w", encoding="utf-8", newline="") as fh:
    w = csv.writer(fh, delimiter="\t", lineterminator="\n")
    w.writerow(["idx", "kind", "chars", "pages"])
    for i in range(len(rows)):
        w.writerow([i, *res[i]])
import collections
print("done:", dict(collections.Counter(v[0] for v in res.values())), flush=True)
