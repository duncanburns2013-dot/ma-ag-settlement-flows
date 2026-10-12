"""Fetch the settlement documents linked from the AG releases and read their distribution clauses where there is a text layer."""
import csv
import os
import re
import subprocess
import time

H = os.environ.get("AG_SWEEP_WORK", "work")  # scratch folder for downloads and intermediate files
os.makedirs(os.path.join(H, "ag-docs"), exist_ok=True)
rows = list(csv.DictReader(open(os.path.join(H, "ag-docs.tsv"), encoding="utf-8"), delimiter="\t"))
print("documents linked:", len(rows))
out = []
for i, r in enumerate(rows):
    f = os.path.join(H, "ag-docs", f"{i:03d}.pdf")
    if not os.path.exists(f) or os.path.getsize(f) < 2000:
        subprocess.run(["powershell", "-File", os.path.join(H, "massgov_get.ps1"), "-Url", (r["doc_url"] if r["doc_url"].endswith("/download") else r["doc_url"].rstrip("/") + "/download"), "-Out", f, "-Referer", r["release_url"]], capture_output=True, text=True)
        time.sleep(0.8)
    size = os.path.getsize(f) if os.path.exists(f) else 0
    head = open(f, "rb").read(5) if size else b""
    kind = "pdf" if head.startswith(b"%PDF") else ("html" if size else "missing")
    txt = ""
    if kind == "pdf":
        subprocess.run(["pdftotext", "-layout", f, f + ".txt"], capture_output=True)
        txt = open(f + ".txt", encoding="utf-8", errors="replace").read() if os.path.exists(f + ".txt") else ""
    out.append((i, r, kind, size, txt))
pdfs = [o for o in out if o[2] == "pdf"]
texty = [o for o in pdfs if len(o[4].strip()) > 800]
print(f"fetched: {len(pdfs)} PDFs, {len(texty)} with a text layer, {len(pdfs) - len(texty)} scanned or empty, {sum(1 for o in out if o[2] != 'pdf')} not PDFs")

FLAGS = {
    "sole discretion over use": r"sole discretion",
    "Local Consumer Aid Fund": r"Local Consumer Aid Fund",
    "General Fund": r"General Fund",
    "restitution to consumers": r"restitution",
    "refund": r"refund",
    "payment to the Commonwealth": r"pay (?:to )?the Commonwealth|payable to the (?:\"?)Commonwealth|paid to the Commonwealth",
    "cy pres / nonprofit": r"cy pres|non-?profit|charit",
}
print("\nclause counts among the text-layer documents:")
for k, rx in FLAGS.items():
    n = sum(1 for o in texty if re.search(rx, o[4], re.I))
    print(f"  {k:32s} {n:3d} of {len(texty)}")
with open(os.path.join(H, "ag-docs-flags.tsv"), "w", encoding="utf-8", newline="") as fh:
    w = csv.writer(fh, delimiter="\t")
    w.writerow(["penalty_id", "defendant", "date", "amount", "doc_url", "kind", "text_chars"] + list(FLAGS))
    for i, r, kind, size, txt in out:
        w.writerow([r["penalty_id"], r["defendant"][:40], r["date"], r["amount"], r["doc_url"], kind, len(txt.strip())] + [int(bool(re.search(rx, txt, re.I))) if txt.strip() else "" for rx in FLAGS.values()])
print("\nexamples of the sole-discretion language:")
shown = 0
for i, r, kind, size, txt in texty:
    t = re.sub(r"\s+", " ", txt)
    m = re.search(r"[^.]{0,260}sole discretion[^.]{0,260}\.", t, re.I)
    if m:
        print(f"  [{r['date']}] {r['defendant'][:30]}: ...{m.group(0).strip()[:420]}")
        shown += 1
    if shown >= 6:
        break
