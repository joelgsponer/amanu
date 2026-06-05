# amanu — extension catalog

The core (a knowledge base + agent memory, built by `build-with-agent.md`) does
one thing well: turn documents into a cross-referenced, queryable synthesis.
**Extensions** attach at the edges to feed it, surface it, automate it, and
sharpen it — without touching the core.

This file is both a **menu** the build agent reads to offer choices, and a
**reference** humans read to understand the ecosystem. Each entry ships only as a
**build prompt**: the agent scaffolds it, wired to your `SCHEMA.md`, at build
time.

---

## The extension contract

Every extension is some combination of three parts:

- **Skill** — a one-word command the user (or agent) invokes (`/ingest-email`).
- **Hook** — an automatic trigger (a filesystem watch, a session-end hook, cron).
- **Tool** — an external CLI or MCP it leans on (`gog`, `rclone`, `whisper`).

An extension may read and write the knowledge base **only through the SCHEMA
conventions** — `inbox/` → ingest, `kb/sources|entities|topics|queries/`, YAML
frontmatter, `[[wiki-links]]`, and the `kb/log.md` operations log. It never
invents its own storage shape. That is what keeps the ecosystem composable: any
extension's output is another's input.

Each extension declares four things:

| Field | Meaning |
|-------|---------|
| **Trust class** | `inbound` (pulls data in, **never sends**) · `outbound` (sends queries/data out — **generic / redacted only**) · `local` (no network at all). |
| **Tier** | The maturity level it belongs to (see below). |
| **Needs** | Tools/CLIs required. |
| **Secrets** | Env vars it needs — **names only, never values**. OAuth-login tools (`gog`) need no env. Secrets live in a git-ignored `.env`; names are mirrored into `.env.example`. |

Each entry below is headed **`name · trust · tier`** and grouped under its
category section. (`*` on a trust class means "depends how you wire it" — see the
entry's trust note.)

### Maturity tiers

The catalog maps onto a growth path, so you adopt capability in stages:

1. **Starter** — the core only: ingest, query, lint. No network.
2. **Connected** — inbound feeds + outbound consumption (email, drive, research…).
3. **Automated** — it maintains itself (hooks, compile loop, cron, backup).
4. **Intelligent** — it reasons over itself (sub-agents, reconciliation, search).

The build delivers **Starter** by default; every extension you add raises the
tier recorded in your `amanu.yaml` manifest.

### Trust-boundary matrix

| Trust class | Reads | Sends out | Rule |
|-------------|-------|-----------|------|
| `inbound`  | external source → `inbox/`/`kb/` | **nothing** | pull-only; never reply/forward/post |
| `outbound` | `kb/` (generic) → web/service | queries/redacted text | never carry private source content verbatim |
| `local`    | `kb/` | nothing | stays offline |

When in doubt, an extension is the *more* restrictive class. Inbound and outbound
are never fused into one step.

---

## Inbound — feed the store

### email · inbound · Connected
- **Adds:** a Gmail label becomes an automatic source feed.
- **Needs:** `gog` (Google Workspace CLI). **Secrets:** none (`gog` uses its own OAuth login).
- **Build prompt:** *Create an `ingest-email` skill that lists Gmail messages labelled `ingest-pending`; for each (oldest first) writes the body to `kb/sources/` and downloads attachments to `inbox/`, runs `/ingest`, then relabels `ingest-pending`→`ingest-done`. Pull-only, idempotent (skip already-done), leave the label on failure so the next run retries.*
- **Trust note:** never sends, replies, or forwards.

### drive-sync · inbound · Connected
- **Adds:** a cloud folder (Google Drive, Dropbox…) mirrors into `inbox/`.
- **Needs:** `gog` (Drive) or `rclone`. **Secrets:** none for `gog`; `rclone` stores its own config (keep it out of git).
- **Build prompt:** *Create a `sync-drive` skill/hook that pulls new/changed files from a named remote folder into `inbox/`, records synced file IDs for idempotency, then runs `/ingest`.*
- **Trust note:** read-only on the remote; never uploads.

### scan-ocr · inbound · Connected
- **Adds:** scans and photos become searchable text sources.
- **Needs:** `ocrmypdf` / `tesseract`. **Secrets:** none (local).
- **Build prompt:** *Create a `scan-ocr` step that, for image/PDF files in `inbox/`, runs OCR to produce a text layer before `/ingest` reads them; keep the original in `raw/`.*
- **Trust note:** fully local.

### web-clipper · inbound · Connected
- **Adds:** a URL → a clean Markdown source page.
- **Needs:** a fetch tool + `pandoc`/readability. **Secrets:** none.
- **Build prompt:** *Create a `clip` skill that takes a URL, fetches and converts the main content to Markdown, writes it as a `kb/sources/` page with `source_url` in frontmatter, and links relevant entities/topics.*
- **Trust note:** fetches public pages only; outbound fetch, no private data leaves.

### audio-transcribe · inbound · Connected
- **Adds:** voice memos / meeting audio become text sources.
- **Needs:** a local transcription tool (e.g. `whisper`). **Secrets:** none if local; an API key if using a hosted model.
- **Build prompt:** *Create a `transcribe` step that turns audio files in `inbox/` into text, files the transcript as a `kb/sources/` page, and keeps the audio in `raw/`.*
- **Trust note:** prefer a local model to keep audio on-machine.

### calendar-pull · inbound · Connected
- **Adds:** calendar events become dated context the KB can reference.
- **Needs:** `gog` (Calendar). **Secrets:** none.
- **Build prompt:** *Create a `pull-calendar` skill that imports events in a date window as dated notes/source pages, linked to the entities they involve.*
- **Trust note:** read-only.

### csv-import · inbound · Connected
- **Adds:** tabular/financial exports (bank CSVs, spreadsheets) become structured sources.
- **Needs:** a CSV parser (built-in). **Secrets:** none.
- **Build prompt:** *Create an `import-csv` skill that parses a CSV/XLSX in `inbox/` into a normalized table page under `kb/sources/`, with column mapping confirmed by the user; never infers transaction meaning — record observations, ask before interpreting.*
- **Trust note:** local; flag any secrets/account numbers for the user.

### messaging-export · inbound · Connected
- **Adds:** exported chat threads (Signal/Telegram/WhatsApp) become sources.
- **Needs:** the platform's export + a parser. **Secrets:** none.
- **Build prompt:** *Create an `import-chat` skill that parses an exported chat archive into a dated `kb/sources/` page, redacting anything the user marks private.*
- **Trust note:** local; treat content as sensitive.

---

## Outbound — get value out

### deep-research · outbound · Connected
- **Adds:** verified, cited external research folded into the store.
- **Needs:** web search + fetch. **Secrets:** search API key *if* using a paid provider.
- **Build prompt:** *Create a `research` skill that takes a question, fans out web searches, reads sources, adversarially verifies key claims, and writes a cited report to `kb/queries/` linked to the relevant topics.*
- **Trust note:** outbound — phrase queries generically; **never** paste private source content into a search.

### digest · outbound* · Connected
- **Adds:** a periodic "what changed / what needs action" summary.
- **Needs:** none (reads `kb/log.md` + frontmatter). **Secrets:** none unless emailed out.
- **Build prompt:** *Create a `digest` skill that summarises new sources, updated topics, and upcoming deadlines since the last run, and saves it to `kb/queries/`; optionally deliver via `gog` Gmail.*
- **Trust note:** `local` if saved to disk; `outbound` only if you choose to send it.

### calendar-push · outbound · Connected
- **Adds:** document deadlines/actions become calendar events.
- **Needs:** `gog` (Calendar). **Secrets:** none.
- **Build prompt:** *Create a `push-deadlines` skill that scans frontmatter/`deadlines` fields and creates calendar events for them, idempotently (tag events so re-runs update rather than duplicate).*
- **Trust note:** writes events only; sends nothing else.

### task-export · outbound · Connected
- **Adds:** open items become reminders/tasks in your task manager.
- **Needs:** a task CLI/MCP (Reminders, Todoist…). **Secrets:** API key for hosted task apps.
- **Build prompt:** *Create an `export-tasks` skill that turns open action items in the KB into tasks in your task manager, idempotently keyed to the source page.*
- **Trust note:** push only the task title, not private detail.

### redacted-publish · outbound · Intelligent
- **Adds:** a safe, public subset of the KB as a static site.
- **Needs:** a static-site step + a redaction pass. **Secrets:** none.
- **Build prompt:** *Create a `publish` skill that selects only pages tagged `public`, runs a redaction/lint pass to strip anything sensitive, and emits a static site — refusing to publish if the redaction check finds risk.*
- **Trust note:** outbound — publishes; gated behind an explicit redaction check.

### report-export · outbound* · Connected
- **Adds:** a polished PDF/report from a topic or query.
- **Needs:** `pandoc` (+ LaTeX/typst for PDF). **Secrets:** none.
- **Build prompt:** *Create an `export-report` skill that renders a chosen topic/query page (and its linked sources) into a styled PDF in an `exports/` folder.*
- **Trust note:** `local`; sharing the file is your call.

---

## Interface — browse & ask

### obsidian-vault · local · Connected
- **Adds:** graph view, backlinks, and live frontmatter queries over `kb/`.
- **Needs:** Obsidian + Dataview plugin. **Secrets:** none.
- **Build prompt:** *Point an Obsidian vault at `kb/`; add a couple of Dataview queries (e.g. sources by category/date) and confirm the graph renders the `[[links]]`.*
- **Trust note:** fully local.

### semantic-search · outbound* · Intelligent
- **Adds:** fuzzy "where did I see…" retrieval beyond exact frontmatter queries.
- **Needs:** an embeddings model + a small vector index. **Secrets:** embeddings API key (if hosted) — `EMBEDDINGS_API_KEY`.
- **Build prompt:** *Create a `search` skill that embeds `kb/` pages into a local index and answers fuzzy queries by similarity, citing the pages — used alongside, not instead of, the exact index lookup.*
- **Trust note:** prefer a local embedding model; if hosted, only page text you accept sending leaves.

### static-site · local · Connected
- **Adds:** the overview/wiki viewable at a URL (e.g. GitHub Pages).
- **Needs:** a static-site generator or plain HTML + Pages. **Secrets:** none.
- **Build prompt:** *Create a `site` step that renders selected `kb/` pages to a static site; combine with `redacted-publish` before anything goes public.*
- **Trust note:** `local` to build; only `outbound` when actually deployed.

### chat-over-kb · local · Intelligent
- **Adds:** conversational Q&A grounded in your store.
- **Needs:** the agent itself (+ optional `semantic-search`). **Secrets:** none beyond the model.
- **Build prompt:** *Create an `ask` skill that answers a natural-language question by retrieving the most relevant `kb/` pages (index first, semantic-search if present) and replying with citations, never asserting beyond the cited pages.*
- **Trust note:** `local` retrieval; answers stay grounded.

---

## Automation — keep it alive

### auto-capture · local · Automated
- **Adds:** durable lessons captured without anyone remembering to save them.
- **Needs:** session-end / pre-compaction hooks. **Secrets:** none.
- **Build prompt:** *Create hooks that, at session end and before compaction, append raw observations to `daily/YYYY-MM-DD.md` for later compilation.*
- **Trust note:** local.

### compile-memory · local · Automated
- **Adds:** daily logs distilled into clean agent-memory facts on a schedule.
- **Needs:** a scheduler + a `compile.py`. **Secrets:** none.
- **Build prompt:** *Create a `compile.py` that reads `daily/` logs, extracts durable lessons, deduplicates against existing memory files, writes new one-fact files, and updates the memory `INDEX.md`. Runs unattended.*
- **Trust note:** local. (Builds on `coleam00/claude-memory-compiler`.)

### scheduled-maintenance · local · Automated
- **Adds:** the store ingests and lints itself on a timer.
- **Needs:** cron/launchd. **Secrets:** none.
- **Build prompt:** *Create a `maintain` job that runs `/ingest` over `inbox/` then `/lint`, on a schedule, and writes a short run summary to `kb/log.md`.*
- **Trust note:** local.

### encrypted-backup · outbound · Automated
- **Adds:** off-machine backup without trusting the host with plaintext.
- **Needs:** `git` remote + `age`/`gpg`. **Secrets:** the encryption key/passphrase — `BACKUP_KEY` (kept in `.env`, never committed).
- **Build prompt:** *Create a `backup` job that encrypts the store with `age`/`gpg` and pushes the ciphertext to a remote; verify a test decrypt.*
- **Trust note:** outbound, but only ciphertext leaves.

### watch-inbox · local · Automated
- **Adds:** ingest fires the moment a source lands.
- **Needs:** a filesystem watcher (`fswatch`/inotify). **Secrets:** none.
- **Build prompt:** *Create a `watch-inbox` hook that triggers `/ingest` when a new file appears in `inbox/`; optionally chain `ingest-email` + `sync-drive` first.*
- **Trust note:** local.

---

## Intelligence — reason over the store

### sub-agents · local · Intelligent
- **Adds:** task-focused agents that read only a defined slice of the store.
- **Needs:** the agent platform's sub-agent mechanism. **Secrets:** none.
- **Build prompt:** *Define specialised sub-agents (e.g. a filing assistant, a per-topic analyst) each scoped to specific `kb/` paths, so each works from exactly the right context.*
- **Trust note:** local.

### contradiction-detector · local · Intelligent
- **Adds:** catches two pages that assert different things about the same fact.
- **Needs:** the agent (+ optional `semantic-search`). **Secrets:** none.
- **Build prompt:** *Create a `check-contradictions` skill that scans for conflicting claims across pages (e.g. two values for the same field) and writes a report to `kb/queries/` for the user to resolve.*
- **Trust note:** local.

### source-reconciliation · local · Intelligent
- **Adds:** cross-checks the synthesis against the raw sources it came from.
- **Needs:** the agent. **Secrets:** none.
- **Build prompt:** *Create a `reconcile` skill that re-reads the raw sources behind a topic page and flags any synthesis claim not supported by a cited source.*
- **Trust note:** local.

### entity-dedup · local · Intelligent
- **Adds:** merges duplicate entity pages (same person/org, different names).
- **Needs:** the agent. **Secrets:** none.
- **Build prompt:** *Create an `entity-dedup` script that detects likely-duplicate entity pages and proposes merges — read-only by default, you approve.*
- **Trust note:** local.

### frontmatter-lint · local · Automated
- **Adds:** guarantees every page carries its required metadata.
- **Needs:** a small validator script. **Secrets:** none.
- **Build prompt:** *Create a `frontmatter-lint` script that validates required YAML fields on every `kb/` page and reports violations.*
- **Trust note:** local.

---

## Write your own extension

The ecosystem is open — a new extension just follows the contract:

1. **Pick a verb and a trust class.** What does it do, and which way does data
   flow (`inbound` / `outbound` / `local`)? Choose the more restrictive class if
   unsure.
2. **Touch the KB only through the conventions.** Read/write `inbox/` and `kb/`
   pages with proper frontmatter and `[[links]]`; log to `kb/log.md`. Don't
   invent new storage.
3. **Declare Needs + Secrets.** List tools, and any env var *names* (values live
   in the git-ignored `.env`, mirrored by name into `.env.example`).
4. **Write the build prompt.** One paragraph telling an agent exactly what to
   scaffold, including idempotency and the trust-boundary rule.
5. **Add an entry here** under the right category and tier, using the template
   above — and it's part of the catalog.
