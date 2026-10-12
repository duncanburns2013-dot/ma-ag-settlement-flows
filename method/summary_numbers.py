"""Print the destination shares behind the README and notes, from docs/data.json (built from the registers by build_dashboard_data.py)."""
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
REPO = os.environ.get("AG_REPO", os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
d = json.load(open(os.path.join(REPO, "docs", "data.json"), encoding="utf-8"))
S = d["settlements"]


def parts(r):
    return r["hm"] + r["pen"] + r["un"] + r["ag"] + r["ds"] + r["nc"]


def rep(label, rows):
    W = [r for r in rows if r["h"] > 0]
    H = sum(r["h"] for r in W)
    o = {k: sum(r[k] for r in W) for k in ("hm", "pen", "un", "ag", "ds", "nc")}
    P = sum(o.values())
    any_ = sum(1 for r in W if parts(r) > 0)
    rec = [r for r in W if abs(parts(r) - r["h"]) <= 0.03 * r["h"]]
    RH = sum(r["h"] for r in rec)
    rp = {k: sum(r[k] for r in rec) for k in o}
    RP = sum(rp.values()) or 1
    print(f"\n== {label}: rows {len(rows)}, with a stated total {len(W)}, announced ${H:,.0f}")
    for k, v in o.items():
        print(f"   {k:4s} ${v:>14,.0f} {100 * v / H:5.1f}%")
    print(f"   no dollar split ${H - P:>14,.0f} {100 * (H - P) / H:5.1f}%   any amount {any_}/{len(W)} ({100 * any_ / len(W):.0f}%)   within 3%: {len(rec)} (${RH:,.0f}) parts: " + ", ".join(f"{k} {100 * v / RP:.1f}%" for k, v in rp.items()))


W = [r for r in S if r["h"] > 0]
rep("all counted settlements", S)
rep("criminal cases excluded", [r for r in S if not r["crim"]])
rep("citations excluded", [r for r in S if not r["cit"]])
big = max(W, key=lambda r: r["h"])
rep("excluding the largest settlement (" + big["n"][:30] + ")", [r for r in S if r["id"] != big["id"]])
rep("announced totals of $1 million and over", [r for r in S if r["h"] >= 1e6])
rep("announced totals under $1 million", [r for r in S if 0 < r["h"] < 1e6])
print("\nrows without a stated total:", sum(1 for r in S if r["h"] <= 0), "| state parts:", sum(1 for r in S if r["h"] <= 0 and parts(r) > 0), "| their parts total $%s" % f"{sum(parts(r) for r in S if r['h'] <= 0):,.0f}")
print("flags among rows with a total: criminal", sum(r["crim"] for r in W), "| citation", sum(r["cit"] for r in W), "| total from title", sum(r["ti"] for r in W), "| 'up to'", sum(r["ceil"] for r in W), "| suspended amount", sum(r["susp"] for r in W), "| merger agreement", sum(r["mer"] for r in W))
