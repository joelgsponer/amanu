<!--
  TEMPLATE — the build agent copies this into the built knowledge base's root as
  AGENTS.md and replaces every {{PLACEHOLDER}} with this project's real values.
  This is the file that WIRES THE KB INTO THE HARNESS: coding agents (Claude
  Code and others) auto-load AGENTS.md / CLAUDE.md at session start, so this is
  what orients any future agent. Keep it short — it points, it does not duplicate.
-->
# AGENTS.md — {{KB_NAME}}

You are working inside an **amanu knowledge base**: a self-contained, portable
system over {{OWNER}}'s documents. This file is auto-loaded at the start of a
session to orient you. Read it, then work from the conventions below — **do not
bulk-read the whole store.**

## Orient first
- **`SCHEMA.md`** is the constitution — read it for the full conventions (the
  three layers, file naming, the frontmatter spec, the ingest / query / lint
  recipes, and the privacy + credential rules).
- **`kb/index.md`** is the catalog — read it on demand to find the right pages.
- **`memory/index.md`** and **`tools/index.md`** are your brain and your toolbox
  (below) — consult them before solving a problem from scratch.
- **Do not auto-load `raw/` or all of `kb/sources/`.** Pull only the specific
  pages a task needs; keep context lean.

## Two memories — and the portability rule
This system splits memory by **what travels with the folder**:

- **`memory/` — the portable brain (in this folder).** It owns *everything about
  working this knowledge base*: conventions (global and per-project), important
  **gotchas**, and **solutions you work out** as problems arise here. It's a
  **cross-linked graph**, like `kb/` but tuned for *method*: one fact per file,
  each with frontmatter and `[[wiki-links]]`, indexed in `memory/index.md`.
  - Node `type`: `convention` · `gotcha` · `solution` · `preference` · `procedure`
    · `tool`. Link facts with `related` / `solves` / `supersedes` / `applies-to`
    (→ a `kb/` page) / `implemented-by` (→ a `tools/` tool).
  - Treat it as authoritative and **keep adding to it** — when you learn something
    durable, write a typed fact and **link it** to the related facts, the kb pages
    it concerns, and any tool that implements it; update `memory/index.md`.
- **The harness/machine memory (outside this folder, e.g. `~/.claude/…`).** This
  holds **machine-specific** facts only — "this box needs the VPN for X", "on this
  Mac do Y this way", local install paths. It stays with the *machine*, not the
  folder.

**Invariant:** moving this folder to another machine must preserve your behaviour.
So anything that should travel goes in `memory/` (or `tools/`); only machine-bound
facts go in the harness memory. Do **not** disable harness auto-loading of
`AGENTS.md`/`CLAUDE.md` — that is the mechanism lifting this file into context.

## `tools/` — your self-arming toolbox
`tools/` holds scripts you build over time to handle this KB's recurring work;
each is catalogued in **`tools/index.md`** with its purpose, when to use it, how
it was derived, and its **lifecycle** (how to start / stop / check it).

- **Self-arming:** when you process the `daily/` logs, look for **recurrent tasks,
  repeated problems, and obvious automations**, and turn them into tools here —
  then record them in `tools/index.md`. The toolbox should grow as the KB is used.
- **Run-state awareness:** some tools are background services (watchers,
  schedulers). **At session start, check `tools/index.md` and report any service
  that should be running but isn't** (use each tool's `status` command). Never
  assume a created script is actually running.

## How it's organised
- `raw/` — immutable source documents, by category: {{CATEGORIES}}.
- `kb/` — the synthesis you maintain (`entities/ topics/ sources/ queries/`, plus
  `index.md`, `log.md`, `overview.md`). Frontmatter on every page; `[[wiki-links]]`.
- `memory/` — the portable brain. `tools/` — the toolbox. `daily/` — session logs.
- `amanu.yaml` — the manifest (tier, categories, skills, extensions, and the
  `tools:` list with each tool's run-state).

## Skills — one-word workflows
Invoke these rather than improvising:
{{SKILLS}}
<!-- e.g. /ingest — file & cross-reference a new document (it consults memory/ and
tools/ first, and appends observations to daily/) · /query — answer from the
synthesis · /lint — health check · plus any extensions you added. -->

## Working rules
- **Local-first** — nothing leaves the machine without an explicit OK.
- **Secrets** live only in a git-ignored `.env`; never commit values.
- **Confirm before writing**; record operations in `kb/log.md` and notable
  decisions in `CHANGELOG.log`.

<!-- Keep this file and CLAUDE.md in sync; AGENTS.md is canonical. Regenerate the
     Skills list whenever skills or extensions change. -->
