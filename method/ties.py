"""Political-money ties for a list of recipients: exact normalized name = confirmed match. Needs local donation, lobbying and disclosure tables and matcher modules that are not published in this repository."""
import collections
import csv
import json
import os
import sys

R = os.environ.get("MATCH_TABLES_DIR", ".")  # folder holding the matching tables and modules (not published here)
os.chdir(R)
sys.path.insert(0, ".")
from pipeline import build_holdings, build_lobbying  # noqa: E402
from pipeline.donor_match import make_matcher  # noqa: E402
from pipeline.lobbying import load_client_details, load_firm_details  # noqa: E402
from pipeline.schema import normalize_name  # noqa: E402


def run(recipients, label, outfile):
    """recipients: list of (name, extra dict). Writes a TSV and prints the headline numbers."""
    by_norm = collections.OrderedDict()
    for name, extra in recipients:
        k = normalize_name(name)
        if k:
            by_norm.setdefault(k, {"names": set(), "extra": extra})["names"].add(name)
    companies = {f"r{i}": {"aliases": [k], "vendor_aliases": []} for i, k in enumerate(by_norm)}
    keys = list(by_norm)
    match = make_matcher(companies)
    res = {f"r{i}": {"ocpf": 0.0, "fec": 0.0, "n_gifts": 0, "lob_firm": 0.0, "lob_inhouse": 0.0, "lob_years": set(), "hold": 0, "hold_officials": set()} for i in range(len(keys))}

    # donations: confirmed, cash, no memo, not pass-through
    with open("data/donations.csv", encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            cid, tier = match(r["employer"])
            if tier != "confirmed" or r["kind"] != "cash" or r["memo_cd"] or r["pass_through"] != "0":
                continue
            d = res[cid]
            d["ocpf" if r["source"] == "OCPF" else "fec"] += float(r["amount"])
            d["n_gifts"] += 1

    # lobbying clients
    rows = load_firm_details(build_lobbying.firm_paths(), "2026-10-12") + load_client_details(build_lobbying.client_paths(), "2026-10-12")
    for r in rows:
        cid, tier = match(r["payer_name"])
        if tier == "confirmed":
            d = res[cid]
            d["lob_firm" if r["kind"] == "firm_fee" else "lob_inhouse"] += float(r["amount"] or 0)
            d["lob_years"].add(r["year"])

    # officials' disclosed ties
    filings = build_holdings.load_filings()
    hrows = build_holdings.load_holdings(os.path.join(build_holdings.SFI, "sfi_entities.csv"), os.path.join(build_holdings.SFI, "sfi_master.csv"), "2026-10-12", "", filings)
    for r in build_holdings.classify(hrows, companies):
        if r["match_tier"] == "confirmed":
            d = res[r["company_id"]]
            d["hold"] += 1
            d["hold_officials"].add(r["official_name"])

    out = []
    for i, k in enumerate(keys):
        d = res[f"r{i}"]
        out.append({"name": sorted(by_norm[k]["names"])[0], **by_norm[k]["extra"], **d})
    with open(outfile, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["recipient", "state_dollars", "donations_ocpf", "donations_fec", "gifts", "lobbying_firm_fees", "lobbying_in_house", "lobbying_years", "officials_ties", "officials_n"])
        for o in sorted(out, key=lambda o: -(o["ocpf"] + o["fec"] + o["lob_firm"] + o["lob_inhouse"])):
            w.writerow([o["name"], o.get("total", ""), f"{o['ocpf']:.0f}", f"{o['fec']:.0f}", o["n_gifts"], f"{o['lob_firm']:.0f}", f"{o['lob_inhouse']:.0f}", len(o["lob_years"]), o["hold"], len(o["hold_officials"])])
    n = len(out)
    don = [o for o in out if o["ocpf"] + o["fec"] > 0]
    lob = [o for o in out if o["lob_firm"] + o["lob_inhouse"] > 0]
    hol = [o for o in out if o["hold"] > 0]
    anyt = [o for o in out if o["ocpf"] + o["fec"] + o["lob_firm"] + o["lob_inhouse"] > 0 or o["hold"] > 0]
    print(f"{label}: {n} distinct recipient names")
    print(f"  with employee donations: {len(don)}   with lobbying: {len(lob)}   with an official's disclosed tie: {len(hol)}   with any of the three: {len(anyt)}")
    print(f"  donations total ${sum(o['ocpf'] + o['fec'] for o in don):,.0f}   lobbying total ${sum(o['lob_firm'] + o['lob_inhouse'] for o in lob):,.0f}")
    return out


if __name__ == "__main__":
    H = os.environ.get("AG_SWEEP_WORK", "work")
    rec = [(r["vendor"], {"total": r["total"], "scopes": r["scopes"]}) for r in csv.DictReader(open(os.path.join(H, "payees.tsv"), encoding="utf-8"), delimiter="\t")]
    out = run(rec, "recipients of AG trust accounts, the opioid fund and the mortgage trust", os.path.join(H, "ties_cthru.tsv"))
    print("\nlargest by lobbying + donations:")
    for o in sorted(out, key=lambda o: -(o["ocpf"] + o["fec"] + o["lob_firm"] + o["lob_inhouse"]))[:25]:
        print(f"  {o['name'][:44]:44s} state ${float(o['total']):>12,.0f}  donations ${o['ocpf'] + o['fec']:>10,.0f}  lobbying ${o['lob_firm'] + o['lob_inhouse']:>11,.0f}  officials' ties {o['hold']}")
