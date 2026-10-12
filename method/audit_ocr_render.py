"""Render the scanned sweep documents to page images for local OCR."""
import csv
import os

import fitz

H = os.path.dirname(os.path.abspath(__file__))
st = list(csv.DictReader(open(os.path.join(H, "sweep-docs-status.tsv"), encoding="utf-8"), delimiter="\t"))
out = os.path.join(H, "sweep_docs_png")
os.makedirs(out, exist_ok=True)
n = 0
for s in st:
    if s["kind"] != "pdf-scanned":
        continue
    i = int(s["idx"])
    d = fitz.open(os.path.join(H, "sweep_docs", f"{i:03d}.bin"))
    for p in range(d.page_count):
        fn = os.path.join(out, f"{i:03d}_p{p + 1:03d}.png")
        if not os.path.exists(fn):
            d[p].get_pixmap(dpi=200, colorspace=fitz.csGRAY).save(fn)
        n += 1
print("pages rendered:", n)
