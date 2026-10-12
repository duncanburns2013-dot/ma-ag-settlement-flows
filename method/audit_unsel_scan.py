"""Scan the bodies of releases the title filter skipped: a dollar amount in a sentence that also carries settlement or payment language."""
import csv
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sweep2_lib import amounts, main_text, sentences  # noqa: E402

H = os.path.dirname(os.path.abspath(__file__))
SETTLE = re.compile(r"settle|agree[sd]? to pay|agreed to|restitution|refund|penalt|judgment|consent (decree|judgment)|assurance of discontinuance|"
                    r"ordered to pay|will pay|to pay|pays?\b|recover|secure[sd]?|resolv|reimburs|forfeit|disgorg|damages|fine[sd]?\b|debt relief|relief", re.I)
GRANT = re.compile(r"grant|award|fund(s|ing)? (to|for)|announces? \$|invest", re.I)
rows = list(csv.DictReader(open(os.path.join(H, "unselected.tsv"), encoding="utf-8"), delimiter="\t"))
out = []
n_have = 0
for r in rows:
    f = os.path.join(H, "rel_unsel", f"{int(r['idx']):04d}.html")
    if not (os.path.exists(f) and os.path.getsize(f) > 5000):
        continue
    n_have += 1
    t = main_text(open(f, encoding="utf-8", errors="replace").read())
    hits = []
    for s in sentences(t):
        am = amounts(s)
        if am and max(am) >= 100000 and SETTLE.search(s):
            hits.append((max(am), s.strip()))
    if hits:
        top = max(hits)
        out.append((r["idx"], r["date"], r["title"], int(top[0]), len(hits), top[1][:400]))
print("bodies read:", n_have, " of", len(rows), " with a >=$100K settlement-type sentence:", len(out))
with open(os.path.join(H, "unsel_candidates.tsv"), "w", encoding="utf-8", newline="") as fh:
    w = csv.writer(fh, delimiter="\t", lineterminator="\n")
    w.writerow(["idx", "date", "title", "max_amount", "n_sentences", "top_sentence"])
    w.writerows(out)
for o in sorted(out, key=lambda x: -x[3])[:40]:
    print(o[1], f"${o[3]:,}", "|", o[2][:90])
