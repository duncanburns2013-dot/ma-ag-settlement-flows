"""Query the Comptroller's CTHRU spending dataset (Socrata pegc-naaa) with server-side aggregation."""
import json
import subprocess
from urllib.parse import urlencode

BASE = "https://cthru.data.socrata.com/resource/pegc-naaa.json"
UA = "ma-ag-settlement-flows/1.0 civic-transparency"


def build_url(select, where=None, group=None, order=None, limit=50000, offset=0):
    params = {"$select": select, "$limit": str(limit), "$offset": str(offset)}
    if where:
        params["$where"] = where
    if group:
        params["$group"] = group
    if order:
        params["$order"] = order
    return BASE + "?" + urlencode(params, safe="")


def fetch_json(url, run=subprocess.run):
    p = run(["curl.exe", "-sS", "-f", "--ssl-no-revoke", "-m", "180", "-A", UA, url], capture_output=True, text=True, encoding="utf-8")
    if p.returncode != 0:
        raise RuntimeError(f"curl exit {p.returncode}: {p.stderr[:200]}")
    try:
        data = json.loads(p.stdout)
    except ValueError as e:
        raise RuntimeError(f"non-JSON response: {p.stdout[:120]!r}") from e
    if not isinstance(data, list):
        raise RuntimeError(f"unexpected response: {str(data)[:120]}")
    return data
