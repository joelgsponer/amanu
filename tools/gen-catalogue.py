#!/usr/bin/env python3
"""Generate the website's extension catalogue from extensions.md.

extensions.md is the single source of truth for the catalogue. This script
parses it and rewrites the block between
    <!-- CATALOGUE:START -->  ...  <!-- CATALOGUE:END -->
in knowledge-base-architecture.html, so the copy-paste cards on the site always
match the prompts in extensions.md.

Usage:
    python3 tools/gen-catalogue.py          # regenerate the HTML in place
    python3 tools/gen-catalogue.py --check  # exit 1 if the HTML is out of sync

No third-party dependencies.
"""
import html
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "extensions.md")
HTML = os.path.join(ROOT, "knowledge-base-architecture.html")

CATEGORIES = ["Inbound", "Outbound", "Interface", "Automation", "Intelligence"]
START = "<!-- CATALOGUE:START -->"
END = "<!-- CATALOGUE:END -->"


def esc(s, keep_ticks=False):
    """HTML-escape for text content; optionally drop Markdown backticks."""
    if not keep_ticks:
        s = s.replace("`", "")
    return html.escape(s, quote=False)


def trust_class(tok):
    if tok.startswith("inbound"):
        return "in"
    if tok.startswith("outbound"):
        return "out"
    return "loc"


def parse(md):
    """Return ordered list of (category, gh, gd, [entries])."""
    lines = md.splitlines()
    groups = []
    cur = None        # current group dict
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        m = re.match(r"^## (\w+)(?: — .*)?$", line)
        if m and m.group(1) in CATEGORIES:
            gh = line[3:].strip()
            gd = ""
            if i + 1 < n and lines[i + 1].strip().startswith("*"):
                gd = lines[i + 1].strip().strip("*").strip()
            cur = {"gh": gh, "gd": gd, "entries": []}
            groups.append(cur)
            i += 1
            continue
        if line.startswith("## "):       # a non-category section ends the catalogue
            cur = None
        if cur is not None and line.startswith("### "):
            parts = [p.strip() for p in line[4:].split("·")]
            entry = {"name": parts[0], "trust": parts[1], "tier": parts[2],
                     "adds": "", "skill": "", "needs": "", "secrets": "", "note": "", "prompt": ""}
            j = i + 1
            while j < n and not lines[j].startswith("### ") and not lines[j].startswith("## "):
                ln = lines[j]
                if ln.startswith("- **Adds:**"):
                    entry["adds"] = ln.split("**Adds:**", 1)[1].strip()
                elif ln.startswith("- **Skill:**"):
                    entry["skill"] = ln.split("**Skill:**", 1)[1].strip()
                elif ln.startswith("- **Needs:**"):
                    rest = ln.split("**Needs:**", 1)[1]
                    needs, _, secrets = rest.partition("**Secrets:**")
                    entry["needs"] = needs.strip().rstrip("· ").strip()
                    entry["secrets"] = secrets.strip()
                elif ln.startswith("- **Trust note:**"):
                    entry["note"] = ln.split("**Trust note:**", 1)[1].strip()
                elif ln.strip() == "```text":
                    buf = []
                    j += 1
                    while j < n and lines[j].strip() != "```":
                        buf.append(lines[j])
                        j += 1
                    entry["prompt"] = "\n".join(buf).strip()
                j += 1
            cur["entries"].append(entry)
            i = j
            continue
        i += 1
    return groups


def render(groups):
    out = []
    for g in groups:
        out.append('    <div class="catgroup">')
        out.append('      <p class="gh">%s</p>' % esc(g["gh"]))
        out.append('      <p class="gd">%s</p>' % esc(g["gd"]))
        out.append('    </div>')
        for e in g["entries"]:
            cls = trust_class(e["trust"])
            meta = ''
            if e["skill"]:
                meta += '<b>Invoke:</b> %s &nbsp;·&nbsp; ' % esc(e["skill"], keep_ticks=True)
            meta += '<b>Needs:</b> %s &nbsp;·&nbsp; <b>Secrets:</b> %s' % (
                esc(e["needs"]), esc(e["secrets"]))
            out.append(
                '    <details class="ext"><summary>'
                '<span class="caret">▸</span>'
                '<span class="nm">%s</span>'
                '<span class="adds">%s</span>'
                '<span class="pill %s">%s</span>'
                '<span class="tier">%s</span></summary>' % (
                    esc(e["name"]), esc(e["adds"]), cls, esc(e["trust"]), esc(e["tier"])))
            out.append('      <div class="body"><p class="meta">%s</p>' % meta)
            out.append(
                '      <div class="prompt">'
                '<button class="copy" onclick="amanuCopy(this)">Copy prompt</button>'
                '<pre><code>%s</code></pre></div>' % esc(e["prompt"], keep_ticks=True))
            out.append('      <p class="trust">Trust — %s</p></div>' % esc(e["note"]))
            out.append('    </details>')
    return "\n".join(out)


def main():
    check = "--check" in sys.argv
    with open(SRC, encoding="utf-8") as f:
        groups = parse(f.read())
    total = sum(len(g["entries"]) for g in groups)
    block = render(groups)
    with open(HTML, encoding="utf-8") as f:
        page = f.read()
    if START not in page or END not in page:
        sys.exit("error: CATALOGUE markers not found in %s" % HTML)
    new = re.sub(re.escape(START) + r".*?" + re.escape(END),
                 START + "\n" + block + "\n    " + END, page, flags=re.DOTALL)
    if check:
        if new != page:
            sys.exit("OUT OF SYNC: run `python3 tools/gen-catalogue.py` and commit.")
        print("in sync — %d extensions" % total)
        return
    if new != page:
        with open(HTML, "w", encoding="utf-8") as f:
            f.write(new)
        print("regenerated catalogue: %d extensions across %d categories" % (total, len(groups)))
    else:
        print("no change — %d extensions" % total)


if __name__ == "__main__":
    main()
