"""Draw a seeded random sample of already-read settlement releases for a blind second reading (new ids, so the second reader sees no earlier answers)."""
import csv
import glob
import os
import random
import shutil
import sys

H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, H)
import verify_audit as v  # noqa: E402

man, urows, clean, problems = v.run(quiet=True)
bad = {ln.split("\t")[0] for ln in open(os.path.join(H, "agent_problems.tsv"), encoding="utf-8") if ln.strip()}
R = []
for fn in sorted(glob.glob(os.path.join(H, "agent_out", "A*.csv"))):
    for r in csv.DictReader(open(fn, encoding="utf-8", newline="")):
        if r["kind"] == "settlement_or_judgment" and r["release_id"] not in bad and r["release_id"] not in {"R078", "R137", "R087"}:
            R.append(r["release_id"])
Uids = [r["release_id"] for r in clean if r["kind"] == "single_state_settlement" and r["release_id"] not in {"U060", "U347", "U079"}]
rnd = random.Random(20261012)
sample = [("R", x) for x in rnd.sample(R, 20)] + [("U", x) for x in rnd.sample(Uids, 25)]
rnd.shuffle(sample)
os.makedirs(os.path.join(H, "blind_read"), exist_ok=True)
key = []
for n, (src, rid) in enumerate(sample, 1):
    srcf = os.path.join(H, "read" if src == "R" else "audit_read", rid + ".txt")
    t = open(srcf, encoding="utf-8").read()
    new = f"V{n:03d}"
    t = t.replace(f"RELEASE_ID: {rid}", f"RELEASE_ID: {new}", 1)
    open(os.path.join(H, "blind_read", new + ".txt"), "w", encoding="utf-8", newline="\n").write(t)
    key.append((new, src, rid))
with open(os.path.join(H, "blind_read", "key.tsv"), "w", encoding="utf-8", newline="") as fh:
    w = csv.writer(fh, delimiter="\t", lineterminator="\n")
    w.writerow(["blind_id", "source_set", "original_id"])
    w.writerows(key)
with open(os.path.join(H, "blind_read", "manifest.tsv"), "w", encoding="utf-8", newline="") as fh:
    w = csv.writer(fh, delimiter="\t", lineterminator="\n")
    w.writerow(["release_id", "date", "title", "url", "chars", "source", "max_amount"])
    for new, src, rid in key:
        t = open(os.path.join(H, "blind_read", new + ".txt"), encoding="utf-8").read()
        d = {k.strip(): val.strip() for k, val in (ln.split(":", 1) for ln in t.split("\n---\n")[0].split("\n") if ":" in ln)}
        w.writerow([new, d.get("DATE", ""), d.get("TITLE", ""), d.get("URL", ""), len(t), "blind", ""])
print("blind sample:", len(key), "releases (R:", sum(1 for k in key if k[1] == "R"), " U:", sum(1 for k in key if k[1] == "U"), ")")
