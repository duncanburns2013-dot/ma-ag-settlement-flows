"""Releases whose fetched page carries no release text (only site boilerplate). A body scan cannot see these; only the title is known."""
import csv
import os
import re
import sys

H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, H)
from sweep2_lib import amounts, main_text  # noqa: E402

srcs = []
for i, r in enumerate(csv.DictReader(open(os.path.join(H, "sweep-selected.tsv"), encoding="utf-8"), delimiter="\t")):
    srcs.append(("sel", r["path"], r["date"], r["title"], os.path.join(H, "rel", f"{i:04d}.html")))
for r in csv.DictReader(open(os.path.join(H, "unselected.tsv"), encoding="utf-8"), delimiter="\t"):
    srcs.append(("unsel", r["path"], r["date"], r["title"], os.path.join(H, "rel_unsel", f"{int(r['idx']):04d}.html")))


def real_body(t):
    # strip the boilerplate blocks and see what is left
    t = re.sub(r"Help Us Improve Mass\.gov.*", "", t, flags=re.S)
    t = re.sub(r"Media Contact.*?(?=BOSTON|$)", "", t, flags=re.S) if "BOSTON" in t else t
    return t


empty = []
for src, path, date, title, f in srcs:
    raw = open(f, encoding="utf-8", errors="replace").read()
    t = main_text(raw)
    # a real release has a dateline or at least several sentences of prose before the feedback widget
    pre = t.split("Help Us Improve Mass.gov")[0]
    pre = re.sub(r"Media Contact.{0,200}?(?:Email [A-Za-z .'-]+ at [\w.@-]+)", "", pre)
    pre = re.sub(r"Office of (?:the )?Attorney General[^.]{0,120}", "", pre)
    prose = len(re.findall(r"[a-z]{4,}\s+[a-z]{3,}\s+[a-z]{3,}", pre))
    if len(pre.strip()) < 700 or prose < 8:
        empty.append((src, path, date, title, len(pre.strip()), max(amounts(title), default=0)))
print("releases with no release text on the fetched page:", len(empty), "of", len(srcs))
by_year = {}
for e in empty:
    by_year[e[2].split("/")[-1]] = by_year.get(e[2].split("/")[-1], 0) + 1
print("by year:", dict(sorted(by_year.items())))
with_money = [e for e in empty if e[5] >= 100000]
print("of those, with a dollar figure of $100K or more in the title:", len(with_money))
for e in sorted(with_money, key=lambda e: e[2][-4:] + e[2]):
    print(f"  {e[2]:>10} [{e[0]}] chars {e[4]:>4} ${e[5]:>12,.0f} | {e[3][:90]}")
with open(os.path.join(H, "empty_bodies.tsv"), "w", encoding="utf-8", newline="") as fh:
    w = csv.writer(fh, delimiter="\t", lineterminator="\n")
    w.writerow(["source", "path", "date", "title", "chars", "title_amount"])
    w.writerows(empty)
