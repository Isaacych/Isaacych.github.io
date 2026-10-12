#!/usr/bin/env python3
"""Generate _data/publications.yml from assets/ref/works.bib.

Pure Python standard library only (re, sys, os). No yaml/bibtexparser and no
Jekyll build — this is just the local data-generation step.

Usage
-----
Run from the repo root:

    python3 scripts/convert_bib.py

It reads ``assets/ref/works.bib`` and writes ``_data/publications.yml``.
The generated file is the single rendered source for the Publications page
(``_includes/publications.html`` renders ``site.data.publications``).
Re-run it after any change to the .bib; do NOT edit the generated YAML by hand.

Because the GitHub Pages builder runs Jekyll with ``--safe`` and a fixed plugin
whitelist, it cannot parse a .bib on the server — hence this pre-build step.
"""

import os
import re
import sys

BIB = "assets/ref/works.bib"
OUT = "_data/publications.yml"

# ---------------------------------------------------------------------------
# Unicode helpers: subscripts / superscripts used to clean chemical formulas
# ---------------------------------------------------------------------------

_SUB = "₀₁₂₃₄₅₆₇₈₉"
_SUP = "⁰¹²³⁴⁵⁶⁷⁸₉"
# operator chars that appear as msup exponents get a fixed superscript symbol
_SUP_OP = {"+": "⁺", "-": "⁻", "−": "⁻", "–": "⁻", "*": "*"}


def to_sub(s):
    return "".join(_SUB[ord(c) - 48] if c in "0123456789" else c for c in s)


def to_super(s):
    out = []
    for c in s:
        if c in _SUP_OP:
            out.append(_SUP_OP[c])
        elif c in "0123456789":
            out.append(_SUP[ord(c) - 48])
        else:
            out.append(c)
    return "".join(out)


# ---------------------------------------------------------------------------
# Title / name cleaning
# ---------------------------------------------------------------------------

# A handful of titles do not clean up sensibly with the general pipeline
# (isotope notation, reaction arrows with spacing problems, a spaced subscript
# that the generic letter->digit rule misses).  They are fixed verbatim here,
# keyed by citation key, and bypass the general cleaner.
TITLE_OVERRIDES = {
    "Yuen_2018": "Quantum-tunneling isotope-exchange reaction H₂ + D⁻ → HD + H⁻",
    "Yuen_2019c": (
        "The Role of Ozone Vibrational Resonances in the Isotope Exchange "
        "Reaction ¹⁶O¹⁶O + ¹⁸O → ¹⁸O¹⁶O + ¹⁶O: The Time-Dependent Picture"
    ),
    "Liu_2019": "Theoretical study of electron-induced vibrational excitation of NO₂",
    "Roy_2016": "Photoassociative production of ultracold heteronuclear YbLi* molecules",
}

# Common LaTeX accented letters -> unicode (e.g. Ep{\'{e}}e -> Epée).
# \' is the acute accent; \" the diaeresis; \~ the tilde.
_ACCENT = {
    "a": "á", "e": "é", "i": "í", "o": "ó", "u": "ú", "y": "ý", "n": "ń", "c": "ć",
    "A": "Á", "E": "É", "I": "Í", "O": "Ó", "U": "Ú", "Y": "Ý", "N": "Ń", "C": "Ć",
}
_ACCENT_DIA = {"a": "ä", "e": "ë", "o": "ö", "u": "ü", "A": "Ä", "E": "Ë",
               "O": "Ö", "U": "Ü"}
_ACCENT_TILDE = {"a": "ã", "o": "õ", "u": "ũ", "A": "Ã", "O": "Õ", "U": "Ũ"}

# Normalize a few exotic whitespace code points BibDesk sometimes inserts.
_UNI_WS = re.compile(r"[ ]")

# MathML subscripts: <msub> base </msub>  (base = one <mi>, subscript = one <mn>)
_MSUB = re.compile(
    r"<mml:msub[^>]*>\s*<mml:mi[^>]*>([^<]*)</mml:mi>\s*"
    r"<mml:mn[^>]*>([^<]*)</mml:mn>\s*</mml:msub>",
    re.IGNORECASE,
)
# MathML superscripts: <msup> base </msup>  (base = <mrow>/<mi>, op = <mo>)
_MSUP = re.compile(
    r"<mml:msup[^>]*>\s*(?:<mml:mrow[^>]*>)?\s*<mml:mi[^>]*>([^<]*)</mml:mi>\s*"
    r"(?:</mml:mrow>)?\s*<mml:mo[^>]*>([^<]*)</mml:mo>\s*</mml:msup>",
    re.IGNORECASE,
)
_TAG = re.compile(r"<[^>]+>")


def _normalize_ws(s):
    return _UNI_WS.sub(" ", s)


def _accent_to_unicode(s):
    s = re.sub(r"\\'([A-Za-z])", lambda m: _ACCENT.get(m.group(1), m.group(1)), s)
    s = re.sub(r'\\"([A-Za-z])', lambda m: _ACCENT_DIA.get(m.group(1), m.group(1)), s)
    s = re.sub(r"\\~([A-Za-z])", lambda m: _ACCENT_TILDE.get(m.group(1), m.group(1)), s)
    return s


def latex_to_unicode(s):
    """Map common TeX math macros / delimiters to unicode."""
    replacements = [
        (r"\\mathplus", "+"),
        (r"\\longrightarrow", "→"),
        (r"\\rightarrow", "→"),
        (r"\\to", "→"),
        (r"\\times", "×"),
        (r"\\cdot", "·"),
        (r"\\ast", "∗"),
        (r"\\star", "★"),
    ]
    for pat, rep in replacements:
        s = re.sub(pat, rep, s)
    s = s.replace("$", "")          # drop math-mode delimiters
    s = s.replace("\\", "")        # drop any stray escape chars
    return s


def clean_title(key, raw):
    if key in TITLE_OVERRIDES:
        return TITLE_OVERRIDES[key]
    t = _normalize_ws(raw)
    # 1. MathML sub- and superscript structures -> unicode before the generic strip
    t = _MSUB.sub(lambda m: m.group(1) + to_sub(m.group(2)), t)
    t = _MSUP.sub(lambda m: m.group(1) + to_super(m.group(2)), t)
    # 2. strip any remaining XML/HTML tags (mml wrappers, <b>, <sub>, ...)
    t = _TAG.sub("", t)
    # 3. LaTeX macros -> unicode
    t = latex_to_unicode(t)
    # 4. strip literal-protection braces
    t = t.replace("{", "").replace("}", "")
    # 5. digit immediately after a letter -> subscript  (re-run to a fixed point)
    prev = None
    while prev != t:
        prev = t
        t = re.sub(r"([A-Za-z])([0-9]+)", lambda m: m.group(1) + to_sub(m.group(2)), t)
    # 6. a glued '+' charge on a formula -> superscript (but not operators in " + ")
    t = re.sub(r"(?<=\w)\+(?![0-9A-Za-z+])", "⁺", t)
    # 7. tidy whitespace (including the BibDesk "108 , 023123" -> "108, 023123")
    t = re.sub(r"\s+", " ", t)
    t = t.replace(" ,", ",")
    return t.strip()


def clean_authors(raw):
    names = [n for n in re.split(r"\s+and\s+", _normalize_ws(raw), flags=re.IGNORECASE)]
    cleaned = []
    for n in names:
        n = n.replace("{", "").replace("}", "")
        n = _accent_to_unicode(n)
        n = re.sub(r"\s+", " ", n)
        n = n.strip()
        if n:
            cleaned.append(n)
    return ", ".join(cleaned)


def clean_journal(raw):
    j = raw.replace("{", "").replace("}", "")
    j = re.sub(r"\s+", " ", _normalize_ws(j)).strip()
    return j


# ---------------------------------------------------------------------------
# Brace-aware BibTeX parser
# ---------------------------------------------------------------------------

def parse_records(text):
    """Parse a BibTeX file into a list of (key, type, {field: value}) in file order."""
    records = []
    i, n = 0, len(text)
    while True:
        at = text.find("@", i)
        if at == -1:
            break
        m = re.match(r"@\s*([A-Za-z]+)\s*\{", text[at:])
        if not m:
            i = at + 1
            continue
        typ = m.group(1)
        # walk to the matching closing brace, respecting nesting and quoted strings
        depth = 1
        k = at + m.end() - 1 + 1  # position just after the opening '{'
        end = None
        while k < n and depth > 0:
            c = text[k]
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    end = k
                    break
            elif c == '"':
                k += 1
                while k < n and text[k] != '"':
                    if text[k] == "\\" and k + 1 < n:
                        k += 2
                    else:
                        k += 1
            k += 1
        if end is None:
            # malformed record; stop
            break
        body = text[at + m.end(): end]
        if typ.lower() == "comment":
            i = end + 1
            continue
        fields = _parse_body(body)
        if fields:
            records.append((fields.get("key", ""), typ, fields))
        i = end + 1
    return records


def _split_top_level(body):
    """Split a record body on top-level commas (ignoring braces and quoted strings)."""
    parts, depth, in_quote, cur = [], 0, False, []
    i = 0
    while i < len(body):
        c = body[i]
        if in_quote:
            cur.append(c)
            if c == "\\" and i + 1 < len(body):
                cur.append(body[i + 1])
                i += 2
                continue
            if c == '"':
                in_quote = False
            i += 1
            continue
        if c == '"':
            in_quote = True
            cur.append(c)
        elif c == "{":
            depth += 1
            cur.append(c)
        elif c == "}":
            depth = max(0, depth - 1)
            cur.append(c)
        elif c == "," and depth == 0:
            parts.append("".join(cur))
            cur = []
        else:
            cur.append(c)
        i += 1
    if cur or parts:
        parts.append("".join(cur))
    return parts


def _parse_value(s):
    s = _normalize_ws(s).strip()
    if not s:
        return ""
    if s[0] == "{":
        depth, k, out = 1, 1, []
        while k < len(s) and depth > 0:
            c = s[k]
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    break
            out.append(c)
            k += 1
        return _normalize_ws("".join(out)).strip()
    if s[0] == '"':
        k, out = 1, []
        while k < len(s):
            c = s[k]
            if c == "\\" and k + 1 < len(s):
                out.append(s[k:k + 2])
                k += 2
                continue
            if c == '"':
                break
            out.append(c)
            k += 1
        return "".join(out).strip()
    # bareword: stop at a closing brace or end
    return s.split(",", 1)[0].split("}", 1)[0].strip()


def _parse_body(body):
    """Return a plain dict of lowercased field-name -> string value, plus a 'key'."""
    segments = _split_top_level(body)
    fields = {}
    for idx, seg in enumerate(segments):
        seg = seg.strip()
        if not seg:
            continue
        if "=" in seg:
            name, _, val = seg.partition("=")
            fields[name.strip().lower()] = _parse_value(val)
        elif idx == 0:
            fields["key"] = seg
        # other barewords are ignored
    return fields


# ---------------------------------------------------------------------------
# Build the publication list
# ---------------------------------------------------------------------------

FORBIDDEN = re.compile(r"[<>$\\{}]")  # leftover MathML / LaTeX / brace junk
# (matches a stray '<', '>', '$', backslash, '{' or '}' in a cleaned title/field)


def year_from(raw):
    m = re.search(r"(\d{4})", raw or "")
    return int(m.group(1)) if m else None


def build_records(records):
    entries = []
    for key, typ, f in records:
        if not key or not f.get("title"):
            continue
        year = year_from(f.get("year", ""))
        if year is None:
            print("WARNING: no year for %r" % (key,), file=sys.stderr)
            continue
        clean = {
            "key": key,
            "year": year,
            "authors": clean_authors(f.get("author", "")),
            "title": clean_title(key, f.get("title", "")),
            "journal": clean_journal(f.get("journal", "")),
        }
        if f.get("volume"):
            clean["volume"] = f["volume"]
        if f.get("number"):
            clean["number"] = f["number"]
        if f.get("pages"):
            clean["pages"] = f["pages"].replace("--", "–")
        raw_url = f.get("url", "")
        doi = f.get("doi", "")
        if doi:
            clean["doi"] = doi
            clean["url"] = "https://doi.org/" + doi
        elif raw_url and "%" not in raw_url and not raw_url.startswith("http://dx"):
            clean["url"] = raw_url
        entries.append((year, f.get("doi", ""), clean))
    # newest first, stable (file order preserved within a year)
    entries.sort(key=lambda e: -e[0])
    return entries


# ---------------------------------------------------------------------------
# YAML emission (double-quoted scalars for strings, bare for integers)
# ---------------------------------------------------------------------------

def yaml_str(s):
    s = s.replace("\\", "\\\\").replace('"', '\\"')
    return '"%s"' % s


def yaml_snumber(s):
    """Emit bare when the scalar is a pure integer, else a double-quoted string."""
    s = s.strip()
    if re.fullmatch(r"\d+", s or ""):
        return s
    return yaml_str(s)


def emit_yaml(groups):
    lines = [
        "# AUTO-GENERATED from assets/ref/works.bib by scripts/convert_bib.py",
        "# DO NOT EDIT BY HAND. Re-run the script after changing the .bib.",
    ]
    for year, group in groups:
        lines.append("")
        lines.append("- year: %d" % year)
        lines.append("  entries:")
        for e in group:
            lines.append("    - key: %s" % e["key"])
            for field in ("authors", "title", "journal", "volume", "number", "pages", "doi", "url"):
                if field in e:
                    val = e[field]
                    if field == "pages":
                        # page/article numbers are identifiers: keep their
                        # leading zeros (e.g. APS 043125) and 'L' letter
                        # prefixes -- always quote so YAML/Ruby never reads
                        # them as (octal) numbers.
                        out = yaml_str(val)
                    elif field in ("volume", "number"):
                        out = yaml_snumber(val)
                    else:
                        out = yaml_str(val)
                    lines.append("      %s: %s" % (field, out))
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Preview / verification printing
# ---------------------------------------------------------------------------

def print_preview(entries, raw_by_key, overrides_used):
    print("=== CLEANED TITLES (raw -> cleaned) ===")
    current_year = None
    for _, _, e in entries:
        if e["year"] != current_year:
            current_year = e["year"]
            print("\n---- %d ----" % current_year)
        raw = raw_by_key.get(e["key"], "").strip()
        if raw != e["title"].strip():
            tag = "  [OVERRIDE]" if e["key"] in overrides_used else ""
            print("\n  key: %s%s" % (e["key"], tag))
            print("  raw:     %s" % raw)
            print("  cleaned: %s" % e["title"].strip())
        else:
            print("  (%s) %s" % (e["key"], e["title"]))
    print("\n=== PROBLEM CHECK ===")
    problems = 0
    for _, _, e in entries:
        for field in ("title", "authors", "journal"):
            hits = FORBIDDEN.findall(e.get(field, ""))
            if hits:
                print("  FOUND %r in %s.%s:\n    %s"
                      % ("".join(hits), e["key"], field, e[field]))
                problems += 1
        for req in ("authors", "journal", "doi", "url"):
            if e.get(req, "") == "":
                print("  EMPTY %s in %s" % (req, e["key"]))
                problems += 1
    if problems == 0:
        print("  OK: no forbidden characters, no missing fields, all titles look clean.")
    print("\n=== SUMMARY ===")
    print("  entries: %d" % len(entries))
    print("  overrides applied: %s" % (", ".join(sorted(overrides_used)) or "(none)"))
    years = sorted({e[2]["year"] for e in entries}, reverse=True)
    print("  years (%d): %s" % (len(years), ", ".join(str(y) for y in years)))


def group_by_year(entries):
    """entries are already year-sorted descending and stable within a year."""
    out = []
    for _, _, e in entries:
        y = e["year"]
        if out and out[-1][0] == y:
            out[-1][1].append(e)
        else:
            out.append((y, [e]))
    return out


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.abspath(os.path.join(here, os.pardir))
    bib_path = os.path.join(root, BIB)
    out_path = os.path.join(root, OUT)

    with open(bib_path, "r", encoding="utf-8") as fh:
        text = fh.read()

    records = parse_records(text)
    raw_by_key = {r[0]: r[2].get("title", "") for r in records}
    entries = build_records(records)
    groups = group_by_year(entries)

    overrides_used = {e[2]["key"] for e in entries if e[2]["key"] in TITLE_OVERRIDES}
    print_preview(entries, raw_by_key, overrides_used)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(emit_yaml(groups))
    print("")
    print("Wrote %s (%d entries across %d years)"
          % (OUT, len(entries), len(groups)))


if __name__ == "__main__":
    main()
