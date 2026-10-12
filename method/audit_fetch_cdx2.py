"""Robust fetch of the Wayback-only AG releases: try every slug variant and every 200-status capture, reject forbidden/404/429 bodies, back off on 429."""
import csv
import html
import os
import re
import subprocess
import time

H = os.environ.get("AG_SWEEP_WORK", ".")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
BAD = (b"page is forbidden", b"find that page", b"Too Many Requests", b"ma__press-teaser")
paths = [ln.strip() for ln in open(os.path.join(H, "cdx_unmatched.txt"), encoding="utf-8") if ln.strip()]


def norm(p):
    return re.sub(r"-\d+$", "", p)


# families: variants that share a 60-char prefix are one release
fams = []
for p in sorted(set(paths), key=lambda x: -len(x)):
    for fam in fams:
        if fam[0][:60] == p[:60]:
            fam.append(p)
            break
    else:
        fams.append([p])
fams.sort(key=lambda f: f[0])
print("families:", len(fams), flush=True)
os.makedirs(os.path.join(H, "cdx_rel"), exist_ok=True)


def curl(url, f=None, timeout=60):
    args = ["curl.exe", "-sS", "-L", "--compressed", "--ssl-no-revoke", "-m", str(timeout), "-H", f"User-Agent: {UA}",
            "-H", "Accept: text/html,*/*;q=0.8", "-H", "Accept-Language: en-US,en;q=0.9"]
    if f:
        args += ["-o", f]
    r = subprocess.run(args + [url], capture_output=True)
    return r.stdout


def good(f):
    if not (os.path.exists(f) and os.path.getsize(f) > 5000):
        return False
    b = open(f, "rb").read()
    return b"<h1" in b and not any(x in b for x in BAD)


def captures(slug):
    for attempt in range(4):
        out = curl(f"https://web.archive.org/cdx/search/cdx?url=mass.gov{slug}&output=txt&fl=timestamp,statuscode&filter=statuscode:200&collapse=digest&limit=12").decode("utf-8", "replace")
        if "Too Many" in out:
            time.sleep(10 * (attempt + 1))
            continue
        return [ln.split()[0] for ln in out.splitlines() if ln.strip() and ln.split()[0].isdigit()]
    return []


rows = []
for i, fam in enumerate(fams):
    f = os.path.join(H, "cdx_rel", f"{i:03d}.html")
    src, used = "FAILED", ""
    # live first (a few are really live)
    for slug in fam:
        curl("https://www.mass.gov" + slug, f)
        if good(f):
            src, used = "live", slug
            break
        time.sleep(0.4)
    if src == "FAILED":
        done = False
        for slug in fam:
            for ts in captures(slug)[:6]:
                for attempt in range(3):
                    curl(f"https://web.archive.org/web/{ts}id_/https://www.mass.gov{slug}", f)
                    b = open(f, "rb").read() if os.path.exists(f) else b""
                    if b"Too Many Requests" in b[:400]:
                        time.sleep(12 * (attempt + 1))
                        continue
                    break
                if good(f):
                    src, used, done = "wayback", f"{slug}@{ts}", True
                    break
                time.sleep(1.2)
            if done:
                break
    raw = open(f, encoding="utf-8", errors="replace").read() if os.path.exists(f) and src != "FAILED" else ""
    txt = re.sub(r"<[^>]+>", " ", raw)
    m = re.search(r"For immediate release[:\s]*(\d{1,2}/\d{1,2}/\d{4})", txt, re.I)
    t = re.search(r"<h1[^>]*>(.*?)</h1>", raw, re.S)
    title = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", t.group(1)))).strip() if t else ""
    rows.append((i, fam[0], src, used, m.group(1) if m else "", title))
    print(i, src, (m.group(1) if m else "-"), fam[0][6:70], flush=True)
    time.sleep(1.0)
with open(os.path.join(H, "cdx_releases.tsv"), "w", encoding="utf-8", newline="") as fh:
    w = csv.writer(fh, delimiter="\t", lineterminator="\n")
    w.writerow(["idx", "path", "source", "used", "date", "title"])
    w.writerows(rows)
print("done. live:", sum(1 for r in rows if r[2] == "live"), " wayback:", sum(1 for r in rows if r[2] == "wayback"), " failed:", sum(1 for r in rows if r[2] == "FAILED"), flush=True)
