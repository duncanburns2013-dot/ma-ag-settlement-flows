import html
import re

AMT = re.compile(r"\$\s?(\d[\d,]*(?:\.\d+)?)(?:\s?(million|billion|thousand|m|b|k)\b)?", re.I)
UNIT = {"million": 1e6, "m": 1e6, "billion": 1e9, "b": 1e9, "thousand": 1e3, "k": 1e3}


def amounts(s):
    out = []
    for m in AMT.finditer(s):
        v = float(m.group(1).replace(",", "").rstrip("."))
        v *= UNIT.get((m.group(2) or "").lower(), 1)
        out.append(v)
    return out


def main_text(raw):
    m = re.search(r"<main.*?</main>", raw, re.S)
    t = m.group(0) if m else raw
    t = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", t, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    t = re.sub(r"\s+", " ", html.unescape(t)).strip()
    i = re.search(r"For immediate release[:\s]*\d+/\d+/\d{4}", t, re.I)
    if i:
        t = t[i.end():]
    j = t.find("### Media Contact")
    if j > 0:
        t = t[:j]
    return t


def sentences(t):
    return re.split(r"(?<=[.!?])\s+(?=[A-Z\"“])", t)
