"""Build docs/data.json and docs/index.html for the dashboard from the registers in data/. Reads only this repository's files."""
import collections
import csv
import datetime
import json
import os
import re

REPO = os.environ.get("AG_REPO", os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
D = os.path.join(REPO, "data")
OUT = os.path.join(REPO, "docs", "data.json")
BUILT = os.environ.get("AG_BUILT") or datetime.date.today().isoformat()
RETRIEVED = "2026-10-12"  # date the sources were fetched; change only after re-fetching


def rd(name):
    return list(csv.DictReader(open(os.path.join(D, name), encoding="utf-8", newline=""), delimiter="\t"))


def num(x):
    try:
        return float(str(x).replace(",", "").replace("$", "")) if str(x).strip() else 0.0
    except ValueError:
        return 0.0


def iso(d):
    m = re.match(r"(\d{1,2})/(\d{1,2})/(\d{4})$", (d or "").strip())
    if m:
        return f"{m.group(3)}-{int(m.group(1)):02d}-{int(m.group(2)):02d}"
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})$", (d or "").strip())
    return d.strip() if m else ""


def pen_or_unsp(r):
    """Split state_penalties_costs by the basis recorded in the register."""
    v = num(r.get("state_penalties_costs"))
    if not v:
        return 0.0, 0.0
    return (v, 0.0) if (r.get("state_payment_basis") or "").startswith("penalty") else (0.0, v)


CRIM = {r["release_id"] for r in rd("criminal-cases-flagged.tsv")}
TITLE_ONLY = {"R003", "R028", "R051", "U489", "U500"}  # registers note the total appears only in the release title
TITLE_RX = re.compile(r"only in (?:the )?title|total only in title|from the title|appears only in title", re.I)
CEIL_RX = re.compile(r"\bup to\b|\bas much as\b", re.I)
SUSP_RX = re.compile(r"suspend", re.I)
MERGER_RX = re.compile(r"merger|acquisition|approval agreement", re.I)


def flags(r):
    text = " ".join([r.get("quote_headline") or "", r.get("notes") or ""])
    return {"ti": 1 if (r["release_id"] in TITLE_ONLY or TITLE_RX.search(r.get("notes") or "")) else 0,
            "crim": 1 if r["release_id"] in CRIM else 0,
            "ceil": 1 if CEIL_RX.search(text) else 0,
            "susp": 1 if SUSP_RX.search(text) else 0,
            "mer": 1 if MERGER_RX.search(text + " " + (r.get("defendant") or "")) else 0}


settlements = []
for r in rd("single-state-settlements-destinations.tsv"):
    if r["status"] != "counted":
        continue
    pen, unsp = pen_or_unsp(r)
    s = {"id": r["release_id"], "d": iso(r["date"]), "n": r["defendant"], "h": num(r["headline_dollars"]), "hm": num(r["harmed"]), "nc": num(r["noncash_relief"]),
         "pen": pen, "un": unsp, "ag": num(r["state_agency_recovery"]), "ds": num(r["designated"]), "set": "f", "how": "sel", "cit": 0, "u": r["url"]}
    s.update(flags(r))
    settlements.append(s)
for r in rd("audit-releases-read.tsv"):
    if r["kind"] != "single_state_settlement" or not r["status"].startswith("counted"):
        continue
    pen, unsp = pen_or_unsp(r)
    hf = r["how_found"]
    how = "sel" if hf.startswith("original") else ("skip" if hf.startswith("skipped") else ("ms" if hf.startswith("flagged") else "arch"))
    s = {"id": r["release_id"], "d": iso(r["date"]), "n": r["defendant"], "h": num(r["headline_dollars"]), "hm": num(r["harmed"]), "nc": num(r["noncash_relief"]),
         "pen": pen, "un": unsp, "ag": num(r["state_agency_recovery"]), "ds": num(r["designated"]), "set": "a", "how": how, "cit": 1 if "citation" in r["status"] else 0, "u": r["url"]}
    s.update(flags(r))
    settlements.append(s)
settlements.sort(key=lambda s: s["d"])

CEIL_M = {"M253", "M225", "M226"}  # registers: "up to" or "as much as" figures
YEARS_M = {"M174", "M253", "M167", "M225", "M189"}  # registers: paid over 7 to 18 years
MUNI_M = {"M174", "M167", "M166", "M225"}  # registers: amount includes municipalities or local governments
GUARANTEED_M = {"M253": 366000000}  # register quote: about $366 million guaranteed over ten years
multistate = []
for r in rd("multistate-ma-share.tsv"):
    if r["status"] == "counted":
        rid = r["release_id"]
        multistate.append({"id": rid, "d": iso(r["date"]), "n": r["defendant"], "nat": num(r["national_total"]), "ma": num(r["ma_amount"]), "cls": r["ma_destination_class"], "det": r["ma_destination_detail"][:160], "u": r["url"],
                           "ceil": 1 if rid in CEIL_M else 0, "yrs": 1 if rid in YEARS_M else 0, "mun": 1 if rid in MUNI_M else 0, "g": GUARANTEED_M.get(rid, 0)})
for r in rd("audit-releases-read.tsv"):
    if r["kind"] == "multistate_settlement" and r["status"].startswith("counted") and num(r["ma_amount"]):
        multistate.append({"id": r["release_id"], "d": iso(r["date"]), "n": r["defendant"], "nat": num(r["national_total"]), "ma": num(r["ma_amount"]), "cls": r["ma_destination_class"], "det": r["ma_destination_detail"][:160], "u": r["url"],
                           "ceil": 0, "yrs": 0, "mun": 0, "g": 0})
multistate.sort(key=lambda s: s["d"])

PART_DOCS = ("Adroit", "Collegium")  # discretion covers only part of the payment
docs = []
for r in rd("settlement-documents-discretion-clauses.tsv"):
    lvl = "strict" if r["kind"].startswith("strict") else "partial"
    docs.append({"pass": "first pass", "d": iso(r["date"]), "n": r["defendant"], "amt": num(r["headline_amount"]), "lvl": lvl, "cl": r["clause_as_read (first 300 characters)"][:360], "u": r["document_url"], "ru": r["release_url"],
                 "part": 1 if any(k in r["defendant"] for k in PART_DOCS) else 0})
for r in rd("settlement-documents-discretion-clauses-pass2.tsv"):
    if r["ag_discretion"] in ("strict", "partial"):
        docs.append({"pass": r["pass"], "d": iso(r["date"]), "n": r["title"], "amt": num(r["amount_in_title"]), "lvl": r["ag_discretion"], "cl": r["clause_as_read"][:360], "u": r["document_url"], "ru": r["release_url"],
                     "part": 1 if any(k in r["title"] for k in PART_DOCS) else 0})
docs.sort(key=lambda s: s["d"])
docs_read = collections.Counter()
for r in rd("settlement-documents-discretion-clauses.tsv"):
    docs_read[iso(r["date"])[:4]] += 1
for r in rd("settlement-documents-discretion-clauses-pass2.tsv"):
    if r["ag_discretion"] != "unreadable":
        docs_read[iso(r["date"])[:4]] += 1

grantees = []
for r in rd("grantees-political-money-ties.tsv"):
    grantees.append({"n": r["recipient"], "don": num(r["donations_ocpf"]) + num(r["donations_fec"]), "lob": num(r["lobbying_firm_fees"]) + num(r["lobbying_in_house"]), "off": int(num(r["officials_ties"])), "ly": int(num(r["lobbying_years"]))})

budget = {"types": [{"t": r["appropriation_type"], "total": num(r["total_dollars"])} for r in rd("ag-spending-by-appropriation-type-fy2015-2027.tsv")],
          "lines": [{"type": r["type"], "name": r["appropriation_name"], "a": r["first_fy"], "b": r["last_fy"], "total": num(r["total_dollars"])} for r in rd("ag-retained-revenue-and-trust-lines-fy2015-2027.tsv")],
          "fy": [{"fy": int(r["fiscal_year"]), "rr": num(r["retained_revenue_dollars"]), "all": num(r["all_ag_spending_dollars"]), "share": num(r["share"])} for r in rd("ag-retained-revenue-share-by-fiscal-year.tsv")]}

listed = collections.Counter()
for r in rd("ag-news-archive-2015-2026.tsv"):
    m, d, y = r["date"].split("/")
    listed[f"{y}-{int(m):02d}"] += 1
recovered = collections.Counter()
rec_rows = rd("releases-missing-from-live-listing.tsv")
for r in rec_rows:
    if r["date"] and not r["same_as_a_listed_release"]:
        m, d, y = r["date"].split("/")
        recovered[f"{y}-{int(m):02d}"] += 1
rec_undated = sum(1 for r in rec_rows if not r["date"])
months = []
y, m = 2015, 1
while (y, m) <= (2026, 10):
    k = f"{y}-{m:02d}"
    months.append({"m": k, "listed": listed.get(k, 0), "rec": recovered.get(k, 0)})
    m += 1
    if m == 13:
        y, m = y + 1, 1

blind = rd("blind-reread-comparison.tsv")
fields = ["headline_dollars", "harmed", "noncash_relief", "state_penalties_costs", "state_agency_recovery", "designated"]
blind_sum = {f: dict(collections.Counter(r[f + "_agree"] for r in blind)) for f in fields}

first_rows = rd("single-state-settlements-destinations.tsv")
audit_rows = rd("audit-releases-read.tsv")
ms_rows = rd("multistate-ma-share.tsv")
failed = [r for r in first_rows if r["status"].startswith("left out: failed")]
excl = {"first_failed": len(failed), "first_failed_h": sum(num(r["headline_dollars"]) for r in failed),
        "first_dup": sum(1 for r in first_rows if r["status"].startswith("left out: duplicate")),
        "audit_dup_ss": sum(1 for r in audit_rows if r["status"].startswith("left out:") and r["kind"] == "single_state_settlement"),
        "audit_dup_ms": sum(1 for r in audit_rows if r["status"].startswith("left out:") and r["kind"] == "multistate_settlement"),
        "first_read": len(first_rows), "first_counted": sum(1 for r in first_rows if r["status"] == "counted"),
        "first_notset": sum(1 for r in first_rows if r["status"].startswith("not a settlement")),
        "multi_read": len(ms_rows), "multi_settle": sum(1 for r in ms_rows if r["kind"] == "multistate_settlement"),
        "multi_no_ma": sum(1 for r in ms_rows if r["status"].startswith("not counted: no Massachusetts amount")) + sum(1 for r in audit_rows if r["kind"] == "multistate_settlement" and r["status"].startswith("counted") and not num(r["ma_amount"])),
        "audit_read": len(audit_rows)}
harmed_rows = {r["release_id"]: {"f": r["form"], "r": r["recipients"], "s": r["amount_status"], "m": r["mechanism"], "a": 1 if r["how_decided"].startswith("readers disagreed") else 0} for r in rd("harmed-money-classified.tsv")}
data = {"meta": {"built": BUILT, "retrieved": RETRIEVED, "excl": excl, "repo": "https://github.com/duncanburns2013-dot/ma-ag-settlement-flows", "listed_releases": sum(listed.values()),
                 "recovered_absent": sum(recovered.values()), "recovered_undated": rec_undated, "readable_documents": 170, "docs_read_by_year": dict(sorted(docs_read.items())), "blind_n": len(blind)},
        "settlements": settlements, "harmed": harmed_rows, "multistate": multistate, "docs": docs, "grantees": grantees, "budget": budget, "months": months, "blind": blind_sum}
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as fh:
    json.dump(data, fh, separators=(",", ":"), ensure_ascii=False)
print("wrote", OUT, os.path.getsize(OUT), "bytes;", len(settlements), "settlements,", len(multistate), "multistate,", len(docs), "documents,", len(grantees), "grantees,", len(months), "months")

# inline the data into the single-file dashboard
tpl = os.path.join(REPO, "method", "dashboard_template.html")
if os.path.exists(tpl):
    payload = json.dumps(data, separators=(",", ":"), ensure_ascii=False).replace("</", "<" + chr(92) + "/")
    html = open(tpl, encoding="utf-8").read().replace("__DATA__", payload).replace("__BUILT__", BUILT).replace("__RETRIEVED__", RETRIEVED)
    with open(os.path.join(REPO, "docs", "index.html"), "w", encoding="utf-8") as fh:
        fh.write(html)
    print("wrote docs/index.html", len(html), "bytes")
