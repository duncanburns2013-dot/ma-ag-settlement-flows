"""Check the audit readers' work: every quote verbatim in its release, every recorded amount inside its quote, parts not above the total."""
import collections
import csv
import glob
import os
import re
import sys

H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, H)
from sweep2_lib import amounts  # noqa: E402

KINDS = {"single_state_settlement", "multistate_settlement", "grant_or_funding", "report_or_summary", "no_payment_or_other"}
PARTS = [("harmed", "quote_harmed"), ("noncash_relief", "quote_noncash"), ("state_penalties_costs", "quote_state"),
         ("state_agency_recovery", "quote_state_agency"), ("designated", "quote_designated")]
VALS = [("headline_dollars", "quote_headline"), ("national_total", "quote_national"), ("ma_amount", "quote_ma")]


def norm(s):
    s = (s or "").replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"').replace("–", "-").replace("—", "-").replace("\xa0", " ")
    return re.sub(r"\s+", " ", s).strip().lower()


def num(x):
    x = (x or "").strip().replace(",", "").replace("$", "")
    try:
        return float(x) if x else None
    except ValueError:
        return None


def hit(v, q):
    return any(abs(a - v) <= max(1, v * 0.005) for a in amounts(q))


def run(pattern="U*.csv", quiet=False):
    manifest = {r["release_id"]: r for r in csv.DictReader(open(os.path.join(H, "audit_read", "manifest.tsv"), encoding="utf-8"), delimiter="\t")}
    rows = []
    for f in sorted(glob.glob(os.path.join(H, "agent_out", pattern))):
        rows += list(csv.DictReader(open(f, encoding="utf-8", newline="")))
    ids = [r["release_id"] for r in rows]
    dups = [k for k, v in collections.Counter(ids).items() if v > 1]
    missing = sorted(set(manifest) - set(ids))
    print(f"rows {len(rows)} of {len(manifest)}; duplicate ids {dups}; missing {len(missing)} {missing[:12]}")
    src = {}
    clean, problems = [], []
    for r in rows:
        rid = r["release_id"]
        if rid not in manifest:
            problems.append((rid, "unknown release id"))
            continue
        if rid not in src:
            src[rid] = norm(open(os.path.join(H, "audit_read", f"{rid}.txt"), encoding="utf-8").read())
        s = src[rid]
        bad = []
        if r["kind"] not in KINDS:
            bad.append(f"kind {r['kind']!r} not allowed")
        for col, qcol in VALS + PARTS:
            v = num(r.get(col))
            q = r.get(qcol, "")
            if q and norm(q) not in s:
                bad.append(f"{qcol} not verbatim")
            if v is not None:
                if not q:
                    bad.append(f"{col} without a quote")
                elif not hit(v, q):
                    bad.append(f"{col} not in its quote")
        qd = r.get("quote_destination", "")
        if qd and norm(qd) not in s:
            bad.append("quote_destination not verbatim")
        total = num(r.get("headline_dollars")) or num(r.get("ma_amount")) or 0
        parts = sum(num(r.get(c)) or 0 for c, _ in PARTS)
        if total and parts > total * 1.02:
            bad.append(f"parts {parts:,.0f} exceed total {total:,.0f}")
        if bad:
            problems.append((rid, "; ".join(bad)))
        else:
            clean.append(r)
    print(f"passing every check: {len(clean)}; with a problem: {len(problems)}")
    if not quiet:
        for rid, b in problems[:80]:
            print("  ", rid, manifest.get(rid, {}).get("title", "")[:48], "|", b[:140])
    print("kinds:", dict(collections.Counter(r["kind"] for r in rows)))
    return manifest, rows, clean, problems


if __name__ == "__main__":
    m, rows, clean, problems = run()
    with open(os.path.join(H, "audit_problems.tsv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerows(problems)
