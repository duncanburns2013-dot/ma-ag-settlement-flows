import csv
import os
import re

H = os.environ.get("AG_SWEEP_WORK", "work")  # scratch folder for downloads and intermediate files
R = os.environ.get("MATCH_TABLES_DIR", ".")  # folder holding the earlier hand-built list (not published here)
rows = list(csv.DictReader(open(os.path.join(H, "ag-docs.tsv"), encoding="utf-8"), delimiter="\t"))


def sentences(t):
    t = re.sub(r"\s+", " ", t)
    return re.split(r"(?<=[.;])\s+(?=[A-Z(\"“])", t)


ALLOC = re.compile(r"distribut|allocat|expend|apportion|use (?:or distribute )?this payment|use the (?:monetary )?payment", re.I)
NOT_ALLOC = re.compile(r"rescind|installment|identity of the Trustee|Settlement Administrator will be chosen|choose the Trustee|extend|waive", re.I)
out, seen = [], set()
for i, r in enumerate(rows):
    f = os.path.join(H, "ag-docs", f"{i:03d}.pdf.txt")
    if not os.path.exists(f):
        continue
    t = open(f, encoding="utf-8", errors="replace").read()
    if len(t.strip()) < 800:
        continue
    disc = [s for s in sentences(t) if re.search(r"sole discretion", s, re.I) and ALLOC.search(s) and not NOT_ALLOC.search(s)]
    if disc and r["penalty_id"] not in seen:
        seen.add(r["penalty_id"])
        strict = bool(re.search(r"any amount, allocation|allocated at the sole discretion|expend and distribute in her sole discretion", " ".join(disc), re.I))
        out.append([r["penalty_id"], r["defendant"][:60], r["date"], r["amount"], "strict: AG decides allocation of the payment" if strict else "partial or other use of discretion", r["release_url"], r["doc_url"], disc[0][:300]])
out.sort(key=lambda x: -float(x[3]))
p = os.path.join(R, "review", "ag-discretion-clauses.tsv")
with open(p, "w", encoding="utf-8", newline="") as fh:
    w = csv.writer(fh, delimiter="\t", lineterminator="\n")
    w.writerow(["penalty_id", "defendant", "date", "headline_amount", "kind", "release_url", "document_url", "clause_as_read (first 300 characters)"])
    w.writerows(out)
print(len(out), "settlements written to", p, " headline $", f"{sum(float(x[3]) for x in out):,.0f}")
st = [x for x in out if x[4].startswith("strict")]
print("strict:", len(st), " headline $", f"{sum(float(x[3]) for x in st):,.0f}", " | other:", len(out) - len(st), " headline $", f"{sum(float(x[3]) for x in out if not x[4].startswith(chr(115)+chr(116)+chr(114))):,.0f}")
print([x[1][:22] for x in out if not x[4].startswith("strict")])
