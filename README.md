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
2. Start the guided, eleven-phase **co-build** with the user at **Phase 0**.
3. Work the loop every phase: **explain before doing → ask to tailor → build
   after a confirmed diff → verify together → checkpoint → log to `CHANGELOG.log`**.

The one-liner a user can give you:

> *"Read `build-with-agent.md` and start the guided build with me at Phase 0.
> Go one phase at a time, explain before you do, confirm before you write, and
> keep the `CHANGELOG.log`."*

## 👤 For humans

Open **[`knowledge-base-architecture.html`](knowledge-base-architecture.html)**
— or the live version at **https://joelgsponer.github.io/amanu/** — for a visual
overview of how the system is built and how the guided setup runs. Prefer to read
the raw plan? It's all in [`build-with-agent.md`](build-with-agent.md).

## What's inside

| File | Purpose |
|------|---------|
| `build-with-agent.md` | The agent-driven build playbook — the executable spec. |
| `knowledge-base-architecture.html` | Visual blueprint & overview for humans. |
| `index.html` | Redirect so GitHub Pages opens the overview. |

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
