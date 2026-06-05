# amanu — extension catalog

The core (a knowledge base + agent memory, built by `build-with-agent.md`) does
one thing well: turn documents into a cross-referenced, queryable synthesis.
**Extensions** attach at the edges to feed it, surface it, automate it, and
sharpen it — without touching the core.

This file is both a **menu** the build agent reads to offer choices, and a
**reference** humans read to understand the ecosystem. Each entry ships only as a
**build prompt**: the agent scaffolds it, wired to your `SCHEMA.md`, at build
time. The prompts are deliberately complete — they tell the agent exactly what to
build *and* which preferences to ask you for first, because this is a
build-together system.

> **This file is the single source of truth for the catalogue.** The copy-paste
> cards on the website are generated from it by `tools/gen-catalogue.py` — edit
> prompts here, then run the generator to sync the HTML.

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
*Turn the world's documents into sources, automatically.*

### email · inbound · Connected
- **Adds:** A Gmail label becomes an automatic source feed.
- **Skill:** `/ingest-email`
- **Needs:** `gog` (Google Workspace CLI) · **Secrets:** none — `gog` uses its own OAuth login.
- **Trust note:** never sends, replies, or forwards.

```text
Create an `ingest-email` skill, wired to my SCHEMA.md, that turns a Gmail label into an automatic source feed. First ask me: which label marks messages to ingest (suggest `ingest-pending`); whether to file the message body as its own source page or only the attachments; and what to do with a message once handled — relabel it (suggest `ingest-done`), archive it, or leave it. Then, for each matching message oldest-first, write the body to `kb/sources/` with sender, subject and date in frontmatter, download every attachment into `inbox/`, run `/ingest` over the new files, and apply the agreed post-step. Use `gog` (its own OAuth login — no API key). Keep it pull-only (never reply, forward, or send), idempotent (record processed message IDs and skip anything already handled), and resilient (on any failure leave the message's label untouched so the next run retries it). Before processing the batch, show me the first message it would file and confirm; verify by running once and opening the resulting source page together.
```

### drive-sync · inbound · Connected
- **Adds:** A cloud folder mirrors into the inbox.
- **Skill:** `/sync-drive`
- **Needs:** `gog` (Drive) or `rclone` · **Secrets:** none for `gog`; `rclone` keeps its own config (out of git).
- **Trust note:** read-only on the remote; never uploads.

```text
Create a `sync-drive` skill (or watch hook), wired to my SCHEMA.md, that mirrors a cloud folder into `inbox/`. First ask me: which remote and folder to watch; whether to use `gog` (Google Drive) or `rclone` (Dropbox, S3, others); whether to pull on demand or on a schedule; and whether to mirror sub-folders. Then pull new or changed files into `inbox/`, recording each remote file ID and version so re-runs skip unchanged files, and run `/ingest` over whatever arrived. Stay read-only on the remote — never upload or delete there. If you use `rclone`, keep its config file out of git. Verify by syncing once and showing me the files it brought in and the source pages `/ingest` produced.
```

### scan-ocr · inbound · Connected
- **Adds:** Scans and photos become searchable text sources.
- **Skill:** `scan-ocr` (pre-ingest step)
- **Needs:** `ocrmypdf` / `tesseract` · **Secrets:** none.
- **Trust note:** fully local.

```text
Create a `scan-ocr` step, wired to my SCHEMA.md, that makes scanned PDFs and photos searchable before they're ingested. First ask me: which OCR language(s) to use; whether to embed a text layer into the PDF or write a sidecar text file; and whether to keep the original image alongside the text. Then, for image and image-only PDF files landing in `inbox/`, run OCR locally (`ocrmypdf`/`tesseract`) to add the text, keep the original in `raw/`, and let `/ingest` read the now-text-bearing file. Skip files that already carry a text layer so re-runs are cheap. Everything stays on the machine — no network. Verify on one scanned document: show the extracted text and the resulting source page.
```

### web-clipper · inbound · Connected
- **Adds:** A URL becomes a clean Markdown source page.
- **Skill:** `/clip`
- **Needs:** a fetch tool + `pandoc`/readability · **Secrets:** none.
- **Trust note:** fetches public pages only; no private data leaves.

```text
Create a `clip` skill, wired to my SCHEMA.md, that turns a URL into a clean source page. First ask me: which category clipped pages belong to; whether to store the full article text or a short summary plus the link; and how to tag them. Then fetch the page, extract the main readable content (readability/`pandoc`), convert it to Markdown, and write it to `kb/sources/` with `source_url`, title, author and fetch-date in frontmatter, linking any entities or topics it mentions. De-duplicate by URL so re-clipping updates rather than duplicates. Only the public URL is fetched — no private content leaves the machine. Verify by clipping one URL and reviewing the page together.
```

### audio-transcribe · inbound · Connected
- **Adds:** Voice memos & meetings become text sources.
- **Skill:** `/transcribe`
- **Needs:** a transcription tool (e.g. `whisper`) · **Secrets:** none if local; `TRANSCRIBE_API_KEY` if hosted.
- **Trust note:** prefer a local model to keep audio on-machine.

```text
Create a `transcribe` step, wired to my SCHEMA.md, that turns audio into text sources. First ask me — and flag the privacy trade-off — whether to use a local model (e.g. `whisper`, nothing leaves the machine) or a hosted one (which sends audio to an API and needs a key); the spoken language; and whether to attempt speaker labels. Then transcribe audio files arriving in `inbox/`, write the transcript to `kb/sources/` with date and duration in frontmatter, keep the original audio in `raw/`, and link the people and topics it concerns. Skip already-transcribed files. Default to the local model; if I choose a hosted one, store its key in `.env` and confirm before sending anything. Verify on one clip: show the transcript and its source page.
```

### calendar-pull · inbound · Connected
- **Adds:** Calendar events become dated context.
- **Skill:** `/pull-calendar`
- **Needs:** `gog` (Calendar) · **Secrets:** none.
- **Trust note:** read-only.

```text
Create a `pull-calendar` skill, wired to my SCHEMA.md, that brings calendar events in as dated context. First ask me: which calendar(s) to read; the date window (e.g. the next 30 days, or a fixed range); and whether to import all events or only those matching a keyword. Then read events read-only via `gog`, write each as a dated note/source page with start, end, location and attendees in frontmatter, and link the entities they involve. Key each page by event ID so re-runs update rather than duplicate. Read-only — it never creates or edits events. Verify on the chosen window: show the events it imported and one resulting page.
```

### csv-import · inbound · Connected
- **Adds:** Tabular & financial exports become structured sources.
- **Skill:** `/import-csv`
- **Needs:** a CSV parser (built-in) · **Secrets:** none.
- **Trust note:** local; flag any secrets/account numbers for the user.

```text
Create an `import-csv` skill, wired to my SCHEMA.md, that turns spreadsheets and CSV/financial exports into structured sources. First ask me: which category these belong to; the delimiter and encoding if non-standard; which columns map to which fields (show me the detected header row and let me confirm the mapping); and whether each row becomes a line item or the whole file becomes one table page. Then parse the file from `inbox/` into a normalized table page under `kb/sources/` with the mapping recorded in frontmatter. Crucially, never infer what a transaction or value means — record only what is observable and ask me before drawing any conclusion. Flag any apparent account numbers, IBANs or secrets for me to review rather than storing them silently. Verify on one file: show the parsed table and the column mapping.
```

### messaging-export · inbound · Connected
- **Adds:** Exported chat threads become sources.
- **Skill:** `/import-chat`
- **Needs:** the platform's export + a parser · **Secrets:** none.
- **Trust note:** local; treat content as sensitive.

```text
Create an `import-chat` skill, wired to my SCHEMA.md, that turns an exported chat archive (Signal, Telegram, WhatsApp, …) into sources. First ask me: which platform and export format it is; whether to import the whole thread as one page, or split by day or by conversation; and any redaction rules (names, numbers, anything to drop). Then parse the archive from `inbox/` into dated `kb/sources/` page(s) with participants and date-range in frontmatter, applying the redactions before anything is written to disk. Treat the content as sensitive and keep it fully local. Verify on one export: show the parsed page and confirm the redactions held.
```

### pii-guard · local · Connected
- **Adds:** A safety gate that scans inbound sources for secrets/PII before they're filed.
- **Skill:** `/pii-guard` (runs at ingest)
- **Needs:** a pattern/regex scanner (built-in) · **Secrets:** none.
- **Trust note:** fully local; it only flags, never transmits.

```text
Create a `pii-guard` step, wired to my SCHEMA.md, that screens files in `inbox/` for sensitive data before `/ingest` files them — reinforcing the credential rules. First ask me: which categories of sensitive data to flag (passwords/recovery phrases, account numbers, IBANs, AHV/SSNs, card numbers, API keys); whether a hit should *block* ingest until I confirm or just *annotate* the resulting source page; and any allow-list of patterns that are safe in this store. Then scan each inbound file's text for those patterns and, on a hit, surface the match (with context, masked) and apply the agreed policy — never auto-deleting the source and never sending anything anywhere. Crucially, if a file contains a true secret (password, recovery phrase, private key), stop and tell me to remove it from the source itself before filing. Fully local. Idempotent — re-scanning a cleared file is cheap and silent. Verify on one file containing a fake account number: show the flag and the policy it applied.
```

---

## Outbound — get value out
*Turn the synthesis into research, reports, events, and tasks.*

### deep-research · outbound · Connected
- **Adds:** Verified, cited external research folded in.
- **Skill:** `/research`
- **Needs:** web search + fetch · **Secrets:** `SEARCH_API_KEY` if using a paid search provider (else none).
- **Trust note:** phrase queries generically; never paste private source content into a search.

```text
Create a `research` skill, wired to my SCHEMA.md, that enriches the store with verified external research. First ask me: which search/fetch tool or provider to use (store any API key in `.env`); how deep to go (a quick scan vs many sources); and the citation style for the saved report. Then take a question, fan out web searches, read the best sources, adversarially verify key claims across independent sources before accepting them, and write a cited report to `kb/queries/` linked to the relevant topics and entities. This is outbound: phrase every query generically and never paste my private source content into a search — if answering well would require private detail, ask me first. Verify by running one research question and reviewing the cited report together.
```

### digest · outbound* · Connected
- **Adds:** A periodic "what changed / needs action" summary.
- **Skill:** `/digest`
- **Needs:** none (reads `kb/log.md` + frontmatter) · **Secrets:** none — `gog` OAuth covers email delivery if you enable it.
- **Trust note:** local if saved to disk; outbound only if you choose to send it.

```text
Create a `digest` skill, wired to my SCHEMA.md, that produces a periodic "what changed and what needs action" summary. First ask me: the cadence (daily, weekly, on demand); what to include (new sources, updated topics, upcoming deadlines, open items); and whether to just save it or also deliver it (e.g. email via `gog`) — saving is local, sending makes it outbound. Then read `kb/log.md` and page frontmatter since the last run, write the digest to `kb/queries/`, and deliver it only if I asked. Key each digest by date so re-runs are idempotent. Verify by generating one digest and reviewing it.
```

### calendar-push · outbound · Connected
- **Adds:** Document deadlines become calendar events.
- **Skill:** `/push-deadlines`
- **Needs:** `gog` (Calendar) · **Secrets:** none.
- **Trust note:** writes events only; sends nothing else.

```text
Create a `push-deadlines` skill, wired to my SCHEMA.md, that turns document deadlines into calendar events. First ask me: which calendar to write to; which frontmatter field holds deadlines (suggest `deadlines`); how much reminder lead time to set; and whether to include a link back to the source page in each event. Then scan pages for deadline/action fields and create events via `gog`, tagging each event with the source page ID so re-runs update the existing event rather than duplicating it. It writes events only and sends nothing else. Verify on one deadline: show the created event and confirm a second run updates rather than duplicates.
```

### task-export · outbound · Connected
- **Adds:** Open items become reminders / tasks.
- **Skill:** `/export-tasks`
- **Needs:** a task CLI/MCP (Reminders, Todoist…) · **Secrets:** `TASK_API_KEY` for hosted task apps (none for local Apple Reminders).
- **Trust note:** push only the task title, not private detail.

```text
Create an `export-tasks` skill, wired to my SCHEMA.md, that pushes open action items into my task manager. First ask me: which task manager to use (Apple Reminders, Todoist, …; store any API key in `.env`); how an item qualifies as a task (e.g. an `open` checkbox, or an `actions` frontmatter field); and which list or project to add them to. Then turn qualifying items into tasks, each keyed to its source page so re-runs update rather than duplicate, pushing only the task title plus a link back — never the private detail behind it. Verify by exporting one item and confirming a second run doesn't duplicate it.
```

### redacted-publish · outbound · Intelligent
- **Adds:** A safe, public subset as a static site.
- **Skill:** `/publish`
- **Needs:** a static-site step + a redaction pass · **Secrets:** none.
- **Trust note:** gated behind an explicit redaction check.

```text
Create a `publish` skill, wired to my SCHEMA.md, that emits a safe public subset of the store as a static site. First ask me: which tag marks a page publishable (suggest `public`); the redaction rules (what patterns or fields must never ship — names, numbers, addresses); and where it deploys. Then select only pages carrying the public tag, run a redaction-and-lint pass that strips or masks anything matching the rules, and build a static site from the result — refusing to publish and reporting back if the check finds any residual risk. This is outbound and gated: nothing ships unless the redaction check passes. Verify on a couple of pages: show what would publish and what the redaction pass caught.
```

### report-export · outbound* · Connected
- **Adds:** A polished PDF / report from a topic or query.
- **Skill:** `/export-report`
- **Needs:** `pandoc` (+ LaTeX/typst for PDF) · **Secrets:** none.
- **Trust note:** local; sharing the file is your call.

```text
Create an `export-report` skill, wired to my SCHEMA.md, that renders a topic or query into a polished document. First ask me: the output format (PDF via LaTeX/typst, or DOCX/HTML); which template or styling to use; and whether to inline the linked source pages or just reference them. Then render the chosen page and its linked sources with `pandoc` into a styled file under an `exports/` folder. It's local — generating the file leaves nothing; sharing it afterwards is my call. Verify by exporting one report and opening it together.
```

---

## Interface — browse & ask
*New ways to read, search, and talk to your store.*

### obsidian-vault · local · Connected
- **Adds:** Colour-coded graph, backlinks, live queries — over the kb and (optionally) the method graph.
- **Skill:** — (Obsidian vault setup)
- **Needs:** Obsidian + Dataview plugin · **Secrets:** none.
- **Trust note:** fully local.

```text
Set up an Obsidian vault so I can browse my knowledge base — and, if I want, the method graph too. First ask me: whether to make a **documents-only** vault (just `kb/`) or a **combined** vault that also shows the portable brain (`memory/`) and toolbox (`tools/`) so the cross-links between method and matter render as one graph; which saved Dataview queries I want (for documents: sources by category, recent changes, open deadlines; and for a combined vault, for the brain too: facts by `type`, gotchas and their solutions, tools and what they implement); whether to add note templates; and whether I want a starting dashboard note. Then place the `.obsidian` config at the **correct single root** — for documents-only that's `kb/`; for a combined vault that's the knowledge-base root (the folder that contains `kb/` and `memory/`) — and **never nest it** in a sub-folder or put a second vault inside an existing one (that's what makes a vault show up empty). For a combined vault, set Obsidian's *Excluded files* to hide `raw/`, `.git`, `.env` and other non-note noise so the graph stays about the synthesis, the method graph, and their links. Enable Dataview, add the agreed queries and templates. Also **colour the graph so the different node kinds stand out at a glance**: ask me for a palette (or use sensible defaults), then write Obsidian graph **colour groups** into `.obsidian/graph.json` — give `kb/` entities, topics and sources each their own colour, and in a combined vault colour the `memory/` facts by `type` (gotcha / convention / solution / preference / procedure) with `tools/` its own colour. Use `path:` queries (e.g. `path:kb/entities/`, `path:tools/`) as the reliable baseline, plus tag or property queries (e.g. `tag:#gotcha` or a `type` property) for finer memory typing; keep a small legend in the dashboard note so I remember which colour is which. Then — if Obsidian is installed — register the vault so I can open it directly (add it to Obsidian's vault list, or hand me an `obsidian://open?path=…` link). Fully local — Obsidian only reads the Markdown already there. Verify by opening the vault and confirming it shows the **real content** (not an empty vault), that the graph renders the `[[wiki-links]]` — including, in a combined vault, a `memory/` fact linking to the `kb/` page it `applies-to` — that one Dataview query returns rows, and that the graph is **colour-coded** so entities, topics, sources, memory facts and tools are visually distinct.
```

### semantic-search · outbound* · Intelligent
- **Adds:** Fuzzy "where did I see…" retrieval.
- **Skill:** `/search`
- **Needs:** an embeddings model + a small vector index · **Secrets:** `EMBEDDINGS_API_KEY` if hosted.
- **Trust note:** prefer a local model; if hosted, only page text you accept sending leaves.

```text
Create a `search` skill, wired to my SCHEMA.md, that adds fuzzy semantic retrieval alongside the exact index lookup. First ask me — this matters for privacy — whether to use a local embedding model (nothing leaves the machine) or a hosted one (which sends page text to an API; store `EMBEDDINGS_API_KEY` in `.env` and confirm before enabling); where to keep the index; and how many results to return. Then embed the `kb/` pages into a local vector index, refresh it incrementally as pages change, and answer fuzzy queries by similarity while always citing the pages — used to complement, never replace, the exact `kb/index.md` lookup. Verify with one fuzzy query and check the citations point to real pages.
```

### static-site · local · Connected
- **Adds:** The wiki viewable at a URL.
- **Skill:** `/site`
- **Needs:** a static-site generator or plain HTML + Pages · **Secrets:** none.
- **Trust note:** local to build; outbound only when actually deployed.

```text
Create a `site` skill, wired to my SCHEMA.md, that renders selected `kb/` pages into a browsable static site. First ask me: which pages or categories to include; whether to use a static-site generator or emit plain HTML; the look (minimal is fine); and whether this stays local or will be deployed. Then render the chosen pages, preserving the `[[links]]` as navigation. Building is fully local; if I plan to deploy it publicly, route it through `redacted-publish` first and confirm. Verify by building once and opening the site locally.
```

### chat-over-kb · local · Intelligent
- **Adds:** Conversational Q&A grounded in your store.
- **Skill:** `/ask`
- **Needs:** the agent (+ optional semantic-search) · **Secrets:** none beyond the model.
- **Trust note:** local retrieval; answers stay grounded.

```text
Create an `ask` skill, wired to my SCHEMA.md, that answers natural-language questions grounded in the store. First ask me: whether retrieval should use the exact `kb/index.md` lookup, `semantic-search` if it's installed, or both; and the citation style for answers. Then, for a question, retrieve the most relevant `kb/` pages, answer only from them, cite every page used, and say so plainly when the store doesn't contain the answer — never assert beyond the cited pages. Retrieval is local. Verify by asking a question whose answer is in the store and checking the citations.
```

### design-system · local · Connected
- **Adds:** One visual language for **every** generated output — the Basel School (Armin Hofmann) tradition by default.
- **Skill:** `/design-system` (guided setup)
- **Needs:** none (writes CSS/token files) · **Secrets:** none.
- **Trust note:** fully local; it only styles outputs, never sends anything.

```text
Create a `design-system` setup, wired to my SCHEMA.md, that defines ONE visual language every generated visual output uses **by default** — the core `/healthcheck` report, and any `static-site`, `report-export`, `redacted-publish`, chart or diagram — unless a specific output explicitly opts out. Orient it on the **Basel School of Design (Armin Hofmann)** tradition — read `templates/design/design-system.md` for the principles (the elemental point·line·plane, contrast as the generative force, economy of means, activated white space, black-&-white primacy with a single structural red, no ornament). **Start from the ready-made template in `templates/design/`** (`tokens.css` + `report.html`, Basel defaults) so there's a working design from the first second, then guide me through tuning it as a short, one-question-at-a-time interview, showing a small live preview at each step — and at each step keep the principle in view: (1) **typeface** — default the grotesque (Akzidenz-Grotesk → Helvetica lineage) via a dependency-free system stack, ask if I prefer another; (2) **scale & grid** — a hard-jumping modular scale (so large/small *contrast* reads), an 8px spacing grid, a 12-col latent grid; (3) **colour** — near-black ink on a restrained near-white with **one** structural red (default `#e2231a`), plus muted pass/warn/fail colours so the red stays the only loud voice; (4) **form** — sharp corners (no radius), no shadows/gradients/ornament, flush-left / ragged-right, light large display against bold tracked labels; (5) **light/dark**. Then write the result as a SINGLE source of truth — design tokens as CSS custom properties in `design/tokens.css` (adapted from the template), a `design/design-system.md` documenting the choices against the Basel principles, and the matching self-contained `report.html` shell outputs can **inline** so they stay offline and dependency-free (no external fonts/CDNs — honour local-first). Record in `SCHEMA.md` the convention that **all visual outputs default to the design system unless they state otherwise**, and write a `memory/` fact so future sessions honour it. Fully local. Verify by regenerating one visual output (e.g. run `/healthcheck`) and showing me the before/after — the report should pick up the tokens automatically.
```

---

## Automation — keep it alive
*The store feeds, maintains, and backs up itself.*

### auto-capture · local · Automated
- **Adds:** Feeds the core loop automatically — writes `daily/` observations without anyone remembering to (the core `/ingest`/`/query` already do this; this captures *everything else* too).
- **Skill:** — (session hooks)
- **Needs:** session-end / pre-compaction hooks · **Secrets:** none.
- **Trust note:** local.

```text
Create auto-capture hooks, wired to my SCHEMA.md, that record durable lessons without anyone remembering to save them. First ask me: which moments to capture at (session end, before context compaction, or both); what kinds of thing to capture (decisions, corrections, preferences, gotchas); and where to write them (suggest `daily/YYYY-MM-DD.md`). Then add hooks that append concise raw observations to the daily log, for later distillation by `compile-memory` into the portable brain (`memory/`) and the toolbox (`tools/`). Register the hooks with the harness and **record them in `tools/index.md`** so their state is visible. Fully local. Verify by triggering a capture once and showing the appended entry.
```

### compile-memory · local · Automated
- **Adds:** **Schedules the core `/compile`** so the self-arming loop (daily logs → memory facts **and new tools**) runs unattended instead of on demand.
- **Skill:** schedules `/compile`
- **Needs:** a scheduler + a `compile.py` · **Secrets:** none.
- **Trust note:** local. Builds on coleam00/claude-memory-compiler.

```text
Create a `compile.py`, wired to my SCHEMA.md, that runs the core `/compile` logic on a schedule — distilling the daily logs into the portable brain and arming it with tools, unattended. (The on-demand `/compile` skill already exists; this is its scheduled wrapper.) First ask me: when it should run (e.g. nightly); how aggressively to deduplicate against existing facts; whether new facts and tools are written automatically or staged for my approval; and a threshold for "recurrent" (how many times a task must repeat before it becomes a tool). Then read the `daily/` logs and do two things: (1) extract durable lessons, gotchas and preferences, deduplicate against the existing one-fact files in `memory/`, write new **typed** fact files (frontmatter with `type` — convention/gotcha/solution/preference/procedure — + body), and crucially **cross-link them into the memory graph**: add `[[links]]`/relations (`related`, `solves`, `applies-to` a kb page, `implemented-by` a tool) and `supersede` any fact they make stale, then update `memory/index.md`; (2) detect recurrent tasks, repeated problems, and obvious automations or optimizations, and for each that crosses the threshold, propose or generate a small script into `tools/` and catalogue it in `tools/index.md` (purpose, when to use, how it was derived, and start/stop/status if it runs as a service) — and link the memory fact to the tool with `implemented-by`. This is the self-arming loop: the system builds its own brain and toolbox as it's used. Idempotent — already-compiled days are skipped. Runs unattended and stays local. (Builds on the approach in coleam00/claude-memory-compiler.) Verify by compiling one day's log and reviewing the facts — and any proposed tool — it produced.
```

### scheduled-maintenance · local · Automated
- **Adds:** Ingests & lints itself on a timer.
- **Skill:** `/maintain` (scheduled job)
- **Needs:** cron / launchd · **Secrets:** none.
- **Trust note:** local.

```text
Create a `maintain` job, wired to my SCHEMA.md, that keeps the store healthy on a timer. First ask me: the schedule (e.g. nightly); which steps to run (ingest whatever's in `inbox/`, then `/lint`, and optionally `digest`); and where to write the run summary. Then write the job to `tools/`, **register it on the schedule by filling a `templates/schedulers/` template** (launchd/systemd/cron — idempotently, unregister-then-register), and **record it in `tools/index.md` and `amanu.yaml`** with its start, stop and status commands so its run-state is visible. Each run executes the agreed steps, **refreshes a heartbeat** (`tools/maintain.state` `last_ok`), and appends a short summary to `kb/log.md`. Fully local. Verify by running the job once by hand, showing the summary line it wrote, and confirming the schedule is registered **and boot-persistent** via its status command.
```

### encrypted-backup · outbound · Automated
- **Adds:** Off-machine backup; only ciphertext leaves.
- **Skill:** `/backup` (scheduled job)
- **Needs:** a git remote + `age`/`gpg` · **Secrets:** `BACKUP_KEY` (in `.env`, never committed).
- **Trust note:** outbound, but only ciphertext leaves.

```text
Create a `backup` job, wired to my SCHEMA.md, that backs the store up off-machine without trusting the host with plaintext. First ask me: whether to encrypt with `age` or `gpg`; which remote to push the ciphertext to; the schedule; and how the key is supplied (store the passphrase or key reference as `BACKUP_KEY` in the git-ignored `.env`, never committed). Then encrypt the store and push only the ciphertext to the remote, and verify a test decrypt on each run so a backup is never silently corrupt. It's outbound, but only encrypted bytes leave. Verify by running one backup and confirming the test decrypt succeeds.
```

### restore-from-backup · inbound · Automated
- **Adds:** The recovery counterpart to `encrypted-backup` — rebuilds the store from ciphertext.
- **Skill:** `/restore`
- **Needs:** `age`/`gpg` + access to the backup remote · **Secrets:** `BACKUP_KEY` (in `.env`, never committed).
- **Trust note:** inbound; pulls only your own ciphertext, decrypts locally, sends nothing.

```text
Create a `restore` job, wired to my SCHEMA.md, that rebuilds the store from an `encrypted-backup`. First ask me: which backup remote/snapshot to restore from (latest, or a chosen point in time if the remote keeps history); whether to restore into a **fresh directory** for inspection (default, safest) or in place; and how the key is supplied (`BACKUP_KEY` from the git-ignored `.env`, matching the backup job). Then fetch the chosen ciphertext, decrypt it locally with `age`/`gpg`, and lay the files out — never overwriting an existing store in place without an explicit confirm and a diff of what would change. After restoring, run `/healthcheck` so I can see the recovered system is intact. It pulls only my own ciphertext and sends nothing. Verify by restoring the latest snapshot into a scratch folder and confirming the file count and a sample page match.
```

### watch-inbox · local · Automated
- **Adds:** Ingest fires the moment a source lands.
- **Skill:** — (`watch-inbox` background service)
- **Needs:** a filesystem watcher (`fswatch` / inotify) · **Secrets:** none.
- **Trust note:** local.

```text
Create a `watch-inbox` tool, wired to my SCHEMA.md, that ingests the moment a file lands. First ask me: which watcher to use (`fswatch`/inotify) or whether to fall back to a short poll; whether to first run `ingest-email` and `sync-drive` to gather remote sources; and a debounce window so a burst of files is handled as one batch. Then write the watcher to `tools/`, and — because a created script that never runs is useless — **register it to start automatically by filling a `templates/schedulers/` template** (launchd on macOS, systemd/cron on Linux; idempotently, unregister-then-register), **start it now**, have it **refresh a heartbeat** (`tools/watch-inbox.state` `last_ok`) each time it fires, and **record it in `tools/index.md` and `amanu.yaml`** with its start, stop and status commands. It watches `inbox/` and triggers `/ingest` on new files after the optional gather step. Fully local. Verify by running its **status** command to confirm it's actually running **and boot-persistent** (on macOS flag that a watcher may need Full Disk Access), then dropping a file in `inbox/` and watching the ingest fire.
```

---

## Intelligence — reason over the store
*Agents that audit, reconcile, and clean up the synthesis.*

### sub-agents · local · Intelligent
- **Adds:** Task-focused agents over a slice of the store.
- **Skill:** — (sub-agent definitions)
- **Needs:** the agent platform's sub-agent mechanism · **Secrets:** none.
- **Trust note:** local.

```text
Define specialised sub-agents, wired to my SCHEMA.md, each scoped to a slice of the store so it works from exactly the right context. First ask me: which roles I want (e.g. a filing assistant, a per-topic analyst, a figures/tax checker); the `kb/` paths each may read; and whether any may write or may only propose. Then create each sub-agent with its scope and a short brief, reading only its allotted paths. Fully local. Verify by giving one sub-agent a task in its domain and checking it stayed within scope.
```

### contradiction-detector · local · Intelligent
- **Adds:** Catches two pages that disagree on one fact.
- **Skill:** `/check-contradictions`
- **Needs:** the agent (+ optional semantic-search) · **Secrets:** none.
- **Trust note:** local.

```text
Create a `check-contradictions` skill, wired to my SCHEMA.md, that finds pages disagreeing about the same fact. First ask me: which fields or kinds of claim matter most (e.g. dates, amounts, statuses); how broadly to compare (within a topic, or across the whole store); and where to write the report. Then scan for conflicting claims — two different values for the same field, or contradictory statements — and write a report to `kb/queries/` listing each conflict with its sources for me to resolve. It proposes, never auto-edits. Fully local. Verify by running it and reviewing the flagged conflicts.
```

### source-reconciliation · local · Intelligent
- **Adds:** Cross-checks the synthesis against its sources.
- **Skill:** `/reconcile`
- **Needs:** the agent · **Secrets:** none.
- **Trust note:** local.

```text
Create a `reconcile` skill, wired to my SCHEMA.md, that checks the synthesis against the raw sources behind it. First ask me: which topic or page to reconcile (or all of them); and how strict to be (flag only unsupported claims, or also claims resting on weak or aged sources). Then re-read the raw sources cited by the chosen page and flag any synthesis claim not actually supported by a cited source, writing the findings to `kb/queries/`. It proposes corrections for me to approve. Fully local. Verify on one topic and review the flags.
```

### entity-dedup · local · Intelligent
- **Adds:** Merges duplicate entity pages.
- **Skill:** `/entity-dedup`
- **Needs:** the agent · **Secrets:** none.
- **Trust note:** local.

```text
Create an `entity-dedup` script, wired to my SCHEMA.md, that finds and merges duplicate entity pages. First ask me: the matching signals to trust (near-identical names, shared identifiers, known aliases); and whether merges are proposed for my approval or applied automatically (default: propose). Then detect likely duplicates, and for each propose a merge that combines their facts and rewrites inbound `[[links]]` — applying only what I approve, read-only by default. Fully local. Verify by reviewing one proposed merge before and after.
```

### frontmatter-lint · local · Automated
- **Adds:** Guarantees every page carries its metadata.
- **Skill:** `/frontmatter-lint`
- **Needs:** a small validator script · **Secrets:** none.
- **Trust note:** local.

```text
Create a `frontmatter-lint` script, wired to my SCHEMA.md, that guarantees every page carries its required metadata. First ask me: the required fields per page type (defaulting to what SCHEMA.md specifies); whether to also check the `memory/` graph (every fact has a valid `type`, and no `[[links]]` are dangling); and whether it should only report violations or also offer to fix the safe ones (e.g. fill a missing date from the file). Then validate the frontmatter on every `kb/` page — and, if asked, every `memory/` fact — and report violations grouped by file, applying fixes only where I allowed. Fully local. Verify by running it and reviewing the report.
```

### dead-link-auditor · local · Automated
- **Adds:** Finds broken `[[wiki-links]]` across the store before they rot the graph.
- **Skill:** `/check-links`
- **Needs:** a small link-graph script · **Secrets:** none.
- **Trust note:** fully local.

```text
Create a `check-links` script, wired to my SCHEMA.md, that audits the `[[wiki-links]]` graph for breakage. First ask me: whether to check `kb/` only or also the `memory/` method graph; how to treat a link to a page that doesn't exist yet (a deliberate stub vs a typo — offer to list both separately); and whether to also flag *orphans* (pages with no inbound links). Then resolve every `[[link]]` (and frontmatter `related`/`applies-to`/`implemented-by` targets) against the files on disk, and write a report to `kb/queries/` grouping: broken links (target missing), likely typos (near-match to an existing page), and orphans — each with the file and line. It proposes, never auto-edits. Fully local. Verify by running it and reviewing the grouped report.
```

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
4. **Write the build prompt.** A complete paragraph telling an agent exactly what
   to scaffold *and* which preferences to ask the user for first, including
   idempotency and the trust-boundary rule.
5. **Add an entry here** under the right category and tier, using the template
   above, then run `tools/gen-catalogue.py` to sync the website.
