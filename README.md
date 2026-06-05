# amanu

> An AI agent that maintains a living, cross-referenced knowledge base over your
> own documents — and remembers how you like to work while doing it. **Point an
> agent at this repo and it builds the system *with* you, step by step.**

Named after the *amanuensis* — a scribe who keeps records on someone's behalf.
That's the agent's whole job here.

## The idea — two memories

- **A knowledge base** remembers *what your documents say*: a wiki-style store of
  immutable sources plus a synthesised, cross-linked Markdown layer.
- **An agent memory** remembers *how you want the work done*: durable
  preferences, corrections, and standing instructions, one fact per file.

Plain Markdown, a folder hierarchy, YAML frontmatter, and `[[wiki-links]]`. No
database, no server, no lock-in. Local-first.

## 🤖 For AI agents

If a user has pointed you at this repository:

1. Read **[`build-with-agent.md`](build-with-agent.md)** — it is your operating
   script, not background reading.
2. Run the **capabilities preflight**, then start the guided, eleven-phase
   **co-build** with the user at **Phase 0**. If an `amanu.yaml` manifest already
   exists, offer to **resume** instead of restarting.
3. Work the loop every phase: **explain before doing → ask to tailor → build
   after a confirmed diff → verify together → checkpoint → log to `CHANGELOG.log`**.
4. Offer extensions from **[`extensions.md`](extensions.md)** by category and
   tier; build only what the user picks, respecting each one's trust class and
   keeping secrets in a git-ignored `.env`.

The one-liner a user can give you:

> *"Read `build-with-agent.md` and start the guided build with me at Phase 0.
> Go one phase at a time, explain before you do, confirm before you write, and
> keep the `CHANGELOG.log`."*

## 👤 For humans

Open **[`knowledge-base-architecture.html`](knowledge-base-architecture.html)**
— or the live version at **https://joelgsponer.github.io/amanu/** — for a
human-first guide: what it is, how it's structured, what the agent does, the
memory system, and the **full extension catalogue with copy-paste build
prompts**. Prefer the raw plan? It's all in [`build-with-agent.md`](build-with-agent.md).

## What's inside

| File | Purpose |
|------|---------|
| `build-with-agent.md` | The agent-driven build playbook — the executable spec. |
| `extensions.md` | The extension catalog (**source of truth**) — 28 plug-ins across 5 categories, each with a complete, preference-asking build prompt, trust class, and tier. |
| `knowledge-base-architecture.html` | Human-first guide — how it works, plus the full extension catalogue with copy-paste build prompts. |
| `index.html` | Redirect so GitHub Pages opens the overview. |
| `templates/` | `AGENTS.md` + `CLAUDE.md` entrypoint templates the build copies into a new KB (with `{{PLACEHOLDERS}}`) to wire it into the agent harness. |
| `tools/gen-catalogue.py` | Regenerates the website's catalogue from `extensions.md` (keeps the two in sync). |

### Maintaining the catalogue

`extensions.md` is the single source of truth. After editing a prompt there, run
the generator to update the website's copy-paste cards:

```sh
python3 tools/gen-catalogue.py          # rewrite the HTML catalogue block
python3 tools/gen-catalogue.py --check  # CI-style: non-zero if out of sync
```

The HTML between the `CATALOGUE:START/END` markers is generated — don't hand-edit
it.

## A brain that travels

Memory is split by portability. The **in-folder** `memory/` is the agent's
**portable brain** (conventions, gotchas, learned solutions) and `tools/` is a
**self-arming toolbox** (scripts distilled from the `daily/` logs as recurring
work shows up) — both travel with the folder. The **harness/machine memory**
holds only machine-specific facts (VPN, OS quirks, paths). Move the folder to a
new machine and behaviour is preserved; only machine memory differs. The
auto-loaded `AGENTS.md`/`CLAUDE.md` wire all of this into each session.

## Grows in tiers

The build delivers a **Starter** system (ingest · query · lint, fully offline);
extensions raise it through **Connected** (inbound feeds + outbound consumption)
→ **Automated** (hooks, compile loop, cron, backup) → **Intelligent** (sub-agents,
semantic search, reconciliation). A machine-readable `amanu.yaml` manifest tracks
the shape and makes the build resumable.

## Privacy

The system you build is **local-first**: it stays on your machine, and nothing
leaves it without your explicit say-so. This repository is **generic** — it
contains no personal data. Your agent tailors every category, entity, and example
to *you*, at build time.

## Credits

The optional automation / compile-loop ideas build on
[`coleam00/claude-memory-compiler`](https://github.com/coleam00/claude-memory-compiler).

## License

[MIT](LICENSE).
