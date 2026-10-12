"""Classify every sweep settlement document (text-layer and OCR'd) for the Massachusetts AG's discretion over how the money is used."""
import csv
import glob
import os
import re

H = os.path.dirname(os.path.abspath(__file__))
rows = list(csv.DictReader(open(os.path.join(H, "sweep-docs.tsv"), encoding="utf-8"), delimiter="\t"))
status = {int(r["idx"]): r for r in csv.DictReader(open(os.path.join(H, "sweep-docs-status.tsv"), encoding="utf-8"), delimiter="\t")}
old_docs = {re.sub(r"/download$", "", r["doc_url"].rstrip("/")) for r in csv.DictReader(open(os.path.join(H, "ag-docs.tsv"), encoding="utf-8"), delimiter="\t")}

SOLE = r"s[o0]le\s+d[il1]scret[il1][o0]n"
OTHER = re.compile(r"American Samoa|Iowa|Settling States?|State Entities|Enforcement Committee|Multistate Working Group|Oversight Committee|each State|respective State|Participating (?:States|Attorneys)|Attorney General of (?!the Commonwealth)", re.I)
USE = re.compile(r"distribut|expend|use (?:or distribute )?the payment|use the (?:monetary )?payment|allocat", re.I)
NOT = re.compile(r"rescind|installment|identity of the Trustee|Settlement Administrator|choose the Trustee|extend|waive", re.I)
STRICT = re.compile(r"any\s+amount,?\s+allocation|in\s+any\s+amount\s+or\s+apportionment|expended,?\s+within\s+the\s+" + SOLE, re.I)


def sentences(t):
    t = re.sub(r"\s+", " ", t)
    return re.split(r"(?<=[.;:])\s+(?=[A-Z(\"“])", t)


def classify(t):
    sn = sentences(t)
    best = ("", "")
    for x in sn:
        if re.search(SOLE + r"|discretion of the (?:Attorney General|AGO)", x, re.I) and USE.search(x) and not NOT.search(x) and not OTHER.search(x):
            lvl = "strict" if STRICT.search(x) else "partial"
            if lvl == "strict" or not best[0]:
                best = (lvl, x)
            if lvl == "strict":
                break
    return best


def text_of(i):
    s = status[i]
    if s["kind"] == "pdf-text":
        return "text-layer", open(os.path.join(H, "sweep_docs", f"{i:03d}.txt"), encoding="utf-8", errors="replace").read()
    pages = sorted(glob.glob(os.path.join(H, "ocr_all", f"{i:03d}_p*.txt")))
    return "ocr", "\n".join(open(p, encoding="utf-8", errors="replace").read() for p in pages)


AMT = re.compile(r"\$\s?(\d[\d,]*(?:\.\d+)?)(?:\s?(million|billion))?", re.I)


def title_amount(title):
    m = AMT.search(title)
    if not m:
        return ""
    v = float(m.group(1).replace(",", ""))
    return int(v * {"million": 1e6, "billion": 1e9}.get((m.group(2) or "").lower(), 1))


out = []
for i, r in enumerate(rows):
    kind = status[i]["kind"]
    if kind not in ("pdf-text", "pdf-scanned"):
        continue
    how, t = text_of(i)
    if how == "ocr" and len(t.strip()) < 800:
        out.append([i, r["date"], r["title"][:110], title_amount(r["title"]), how, "unreadable", "", r["doc_url"], r["path"], "already analysed" if re.sub(r"/download$", "", r["doc_url"].rstrip("/")) in old_docs else ""])
        continue
    lvl, clause = classify(t)
    out.append([i, r["date"], r["title"][:110], title_amount(r["title"]), how, lvl or "none", clause[:360], r["doc_url"], r["path"], "already analysed" if re.sub(r"/download$", "", r["doc_url"].rstrip("/")) in old_docs else ""])
new = [o for o in out if not o[9]]
print("documents:", len(out), " new (not analysed before):", len(new))
for how in ("text-layer", "ocr"):
    sub = [o for o in new if o[4] == how]
    print(f"  {how}: {len(sub)} docs; strict {sum(1 for o in sub if o[5] == 'strict')}, partial {sum(1 for o in sub if o[5] == 'partial')}, none {sum(1 for o in sub if o[5] == 'none')}, unreadable {sum(1 for o in sub if o[5] == 'unreadable')}")
print("\nstrict Massachusetts-AG discretion clauses (new documents):")
for o in sorted([o for o in new if o[5] == "strict"], key=lambda o: o[1][-4:] + o[1]):
    print(f"  {o[1]:>10} [{o[4]}] ${o[3] or 0:>11,} {o[2][:78]}")
with open(os.path.join(H, "sweep-docs-classified2.tsv"), "w", encoding="utf-8", newline="") as fh:
    w = csv.writer(fh, delimiter="\t", lineterminator="\n")
    w.writerow(["idx", "date", "title", "title_amount", "text_source", "ag_discretion", "clause_as_read", "document_url", "release_path", "note"])
    w.writerows(out)
