#!/usr/bin/env python3
"""Guard against drift between the design tokens and the report template.

`templates/design/tokens.css` is the source of truth for the design system.
`templates/design/report.html` DUPLICATES a subset of those token values inline in
its <style> so the generated HTML stays self-contained (no external assets). This
script compares the two and fails if a shared token's value diverges — so an edit
to tokens.css that isn't mirrored into report.html is caught, not shipped silently.

It compares the first (light) :root block of each file. Shared tokens must match;
report-only / tokens-only tokens are reported as notes, not failures.

Usage:
    python3 tools/check-design-sync.py          # exit 1 on divergence

No third-party dependencies.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TOKENS = os.path.join(ROOT, "templates", "design", "tokens.css")
REPORT = os.path.join(ROOT, "templates", "design", "report.html")


def _norm(value):
    """Normalize so equivalent values compare equal: collapse whitespace, lowercase,
    expand 3-digit hex (#fff → #ffffff)."""
    v = re.sub(r"\s+", "", value).lower()
    m = re.fullmatch(r"#([0-9a-f])([0-9a-f])([0-9a-f])", v)
    if m:
        v = "#" + "".join(c * 2 for c in m.groups())
    return v


def light_root_vars(text):
    """Parse `--name: value` from the FIRST :root{...} block, resolving var() refs."""
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)   # strip CSS comments
    m = re.search(r":root\s*{(.*?)}", text, flags=re.DOTALL)
    if not m:
        sys.exit("error: no :root block found")
    out = {}
    for name, value in re.findall(r"--([\w-]+)\s*:\s*([^;]+);", m.group(1)):
        out[name] = _norm(value)
    # resolve var(--x) one ref at a time until stable (intra-block references)
    for _ in range(8):
        changed = False
        for k, v in out.items():
            ref = re.fullmatch(r"var\(--([\w-]+)\)", v)
            if ref and ref.group(1) in out:
                out[k] = out[ref.group(1)]
                changed = True
        if not changed:
            break
    return out


def main():
    with open(TOKENS, encoding="utf-8") as f:
        tok = light_root_vars(f.read())
    with open(REPORT, encoding="utf-8") as f:
        rep = light_root_vars(f.read())

    shared = sorted(set(tok) & set(rep))
    mismatches = [(k, tok[k], rep[k]) for k in shared if tok[k] != rep[k]]

    if mismatches:
        print("OUT OF SYNC — tokens.css ↔ report.html diverge:")
        for k, tv, rv in mismatches:
            print("  --%s: tokens=%s  report=%s" % (k, tv, rv))
        print("Update report.html's inline <style> to match tokens.css, then re-run.")
        sys.exit(1)

    print("in sync — %d shared design tokens match" % len(shared))
    report_only = sorted(set(rep) - set(tok))
    if report_only:
        print("note: report.html defines tokens not in tokens.css: %s" % ", ".join(report_only))


if __name__ == "__main__":
    main()
