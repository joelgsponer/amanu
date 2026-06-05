# Build With Me — an agent-driven co-build of the two-memory knowledge base

> **You (the human):** paste this whole file to your AI agent, or just say
> *"Read `build-with-agent.md` and start the guided build with me at Phase 0."*
>
> **You (the agent):** this file is your operating script. You are not writing a
> report — you are **building a working system together with the user**, one
> phase at a time, teaching as you go, so that by the end the system runs *and*
> you both understand every part of it. The conceptual map is
> `knowledge-base-architecture.html`; the full extension menu is `extensions.md`.
> **This** file is what you execute.

---

## A · Operating contract

You are co-building a **two-memory knowledge base**: a wiki-style store over the
user's documents (the *matter*), plus an in-folder **agent-memory** that is the
system's **portable brain** (the *method* — conventions, gotchas, solutions you
work out, and a self-arming toolbox). Build it *with* the user, never *for* them.
Everything that should travel with the folder lives **inside** it; the
harness/machine memory holds only machine-specific facts (see §C).

**The rules — follow them in every phase:**

1. **Explain before you do.** Open each phase with 2–4 plain sentences: what
   we're about to build and *why it matters*. A tutorial as much as a build.
2. **One question at a time.** Ask, wait, reflect the answer back in your own
   words, then continue. Never dump a survey.
3. **Confirm before every write.** Show the file path and a preview/diff; get a
   yes. No silent changes.
4. **Never invent.** Don't assume categories, entities, tools, or preferences the
   user hasn't confirmed. Prefer the user's own words for names.
5. **Local-first.** Nothing leaves the machine without explicit approval. Cloud /
   web steps are opt-in and named as such.
6. **Check understanding at each checkpoint.** One-line recap + "make sense /
   want to adjust?" If they're lost, slow down — comprehension is a deliverable.
7. **Stay generic until they personalize.** Every concrete category, entity, and
   example comes from the *runner*, at runtime.
8. **Be idempotent and resumable.** Re-running a step must not double-write.
   Record state so a stopped build can resume (see §C).
9. **Credential hygiene.** **Never** write a secret value into any tracked file,
   the manifest, or `CHANGELOG.log`. Secrets live only in a git-ignored `.env`.
   If a *source* contains a secret, stop and flag it for removal.
10. **Done means proven.** A phase isn't done until its *Done when* check passes
    (see §D). State plainly when something failed — don't paper over it.

**Anti-patterns — don't:**
- dump walls of text instead of teaching in small beats;
- invent categories/entities/tools to fill silence;
- skip the confirm-before-write step "to save time";
- over-engineer — build the simplest thing that meets the goal;
- build skills or extensions the user didn't choose;
- fuse inbound and outbound in one step, or commit a secret.

**The per-phase loop** — run all six beats, in order, every phase:

```
TEACH      → explain the concept and why it earns its place
TAILOR     → ask only what you need to shape this phase to the user
BUILD      → create the artifact (after a confirmed diff)
VERIFY     → look at the result together; prove it works
CHECKPOINT → recap in one line; confirm understanding; get a go
LOG        → append a CHANGELOG.log entry + update the manifest
```

If the user stops, the system must be **left working** at the last completed
phase — never half-written.

---

## B · Capabilities preflight (before Phase 0)

Quietly check what you're working with, then adapt — don't assume:

- **File read/write** and **document reading** (PDFs, images). If you can't read a
  format, note which extension covers it (e.g. `scan-ocr`).
- **Persistent memory** for the *method* layer (or a local fallback folder).
- **Installed tools** — probe for `git`, and any the user might want later
  (`gog`, `rg`, `pandoc`, `ocrmypdf`, `rclone`, `whisper`). Missing is fine;
  it just gates which extensions are available now.
- **OS + scheduler** — note the platform (macOS → `launchd`, Linux →
  `systemd`/`cron`) so background tools can be **registered to actually start**.
- **Harness loading** — note whether the harness auto-loads `CLAUDE.md`/`AGENTS.md`
  (Claude Code and most do). If it doesn't, tell the user how their tool pulls in
  context so the entrypoint still gets used.

Record the findings; they inform what you offer in P1 and go in the manifest.

---

## C · Self-documenting, portable & resumable

The system explains itself *and carries its own behaviour*, so neither of you
needs this playbook later — and so the folder works the same on another machine.
You keep that true:

- **`SCHEMA.md`** — the constitution; anyone reading it can run the system.
- **`CLAUDE.md` + `AGENTS.md`** *(agent entrypoints)* — the conventional files a
  coding agent auto-loads when it opens the project, so any future session is
  instantly oriented; this is what **wires the KB into the harness**. Build them
  from `templates/AGENTS.md` + `templates/CLAUDE.md`, filling the placeholders.
  Keep them **short**: point to `SCHEMA.md`, `memory/`, `tools/`, list the
  available skills, and restate the rules. (`AGENTS.md` is canonical, a.k.a.
  `AGENT.md`; `CLAUDE.md` points to it so they never drift.) **Regenerate them
  whenever skills or extensions change.**

**The portable brain & the toolbox** — two in-folder stores make the system carry
its own behaviour:
- **`memory/`** — the agent-memory: *everything about working this KB* —
  conventions (global + per-project), gotchas, and solutions you work out. It is a
  **cross-linked knowledge graph**, like `kb/` but tuned for *method*: one fact per
  file, each with frontmatter and `[[wiki-links]]` to related nodes;
  `memory/index.md` is the entry point. Keep adding to it as you learn.
  - **Node types** (`type:`): `convention` · `gotcha` · `solution` · `preference`
    · `procedure` · `tool` (a pointer to a `tools/` entry).
  - **Edges** (frontmatter keys + inline links): `related` · `solves`/`caused-by`
    · `supersedes` (retire a stale fact without deleting history) · `applies-to`
    (→ a `kb/` category/entity/topic) · `implemented-by` (→ a `tools/` tool).
  - So **method ↔ matter ↔ toolbox** form one graph — a gotcha can `applies-to`
    a kb topic and be `implemented-by` a tool. Example fact frontmatter:
    ```yaml
    ---
    type: gotcha
    tags: [obsidian, vault]
    applies-to: [[obsidian-vault]]
    implemented-by: [[fix-vault-root]]   # a tool, if one exists
    related: [[kb-conventions]]
    ---
    ```
- **`tools/`** — a **self-arming** toolbox of scripts for this KB's recurring
  work, each catalogued in `tools/index.md` with its purpose and **lifecycle
  (start / stop / status)**. When you process `daily/` logs, turn recurrent
  tasks, repeated problems and obvious automations into tools here.
- **`daily/`** — raw session logs that feed the self-arming loop.

**Machine memory vs portable memory.** The harness's own memory (`~/.claude/…`)
holds **machine-specific** facts only — VPN needs, OS quirks, local paths. The
rule: *anything that should survive moving the folder to another machine goes in
`memory/` or `tools/`; only machine-bound facts go in the harness memory.* Don't
disable harness auto-loading of `CLAUDE.md`/`AGENTS.md` — it's the mechanism that
lifts the entrypoints into context.

**Run-state awareness.** Background tools (watchers, schedulers) are registered
and **started** when built (P8), and recorded in `tools/index.md` and the manifest
with their start/stop/status commands. At session start, check and surface any
service that *should* be running but isn't — never assume a created script is live.
- **Frontmatter on every page** (`type`, `category`, `date`, `related`, `tags`)
  + `[[wiki-links]]`.
- **Two logs, kept distinct:**
  - **`CHANGELOG.log`** — the append-only story of *building/evolving* the
    system: decision + artifact + *why*. Written at every **LOG** beat.
  - **`kb/log.md`** — routine *operations*: one line per ingest/query/lint.
- **`amanu.yaml`** *(the manifest — machine-readable state)* at the built
  system's root:

  ```yaml
  schema_version: 1
  tier: starter            # starter | connected | automated | intelligent
  last_phase: P3           # resume point
  depth: guided            # quick | guided | thorough
  categories: [ ... ]
  entities: [ ... ]
  skills: [ ingest, query, lint ]
  extensions: [ ]          # names from extensions.md
  credentials: [ ]         # env-var NAMES only, never values
  tools:                   # the self-arming toolbox + run-state
    - { name: watch-inbox, kind: service, autostart: true,
        start: "<cmd>", stop: "<cmd>", status: "<cmd>", state: running }
  privacy: local-first
  ```
- **`README.md`** — a plain-language overview generated near the end.

**Resume protocol.** On start, if `amanu.yaml` + `CHANGELOG.log` already exist,
read them, summarise the state ("you're at `last_phase`, tier X, with these
skills/extensions"), and **offer to resume there** instead of restarting. The
manifest is the single source of truth for the system's shape.

---

## D · Definition of done (per phase)

Every phase carries a **Done when:** line (below). Don't advance until it's true.
Overall, the build is done when: an ingest and a query both run unaided, the
manifest reflects reality, `CHANGELOG.log` tells the full story, and the user can
explain the system back in their own words.

---

## E · Tailoring-depth dial

Ask once, early: **how deep do you want to go?**

- **quick** — minimal questions, sensible defaults, terse teaching. Get to a
  working Starter fast.
- **guided** *(default)* — the full interview, taught in small beats.
- **thorough** — extra teaching, more options surfaced, more verification.

Record it as `depth` in the manifest and scale your interview + explanations
accordingly.

---

## F · The build journey — Phase 0 → Phase 10

Each phase runs the six beats. Adapt wording; hit every beat; honour *Done when*.

### P0 · Orient & contract
- **TEACH** — the two-memory idea + the journey (11 phases). Set the rhythm:
  "build a little, check it together, log it."
- **TAILOR** — run the **preflight** (§B); ask where the system lives; confirm
  `git`; set the **depth dial** (§E). If a manifest exists, offer to **resume**.
- **BUILD** — create the directory (if needed), `CHANGELOG.log`, and a first
  `amanu.yaml` (tier `starter`, `last_phase: P0`, depth).
- **VERIFY** — show the directory, the opening log entry, and the manifest.
- **CHECKPOINT** — "here's the plan and where we're building — good to start?"
- **LOG** — `P0 · initialized · CHANGELOG.log + amanu.yaml · depth=<…>`.
- **Done when:** directory, `CHANGELOG.log`, and `amanu.yaml` exist.

### P1 · Shape interview *(the tailoring core)*
- **TEACH** — these answers shape everything; nothing is locked, it all co-evolves.
- **TAILOR** — one question at a time, reflecting each back:
  1. **Shape & scope** — what body of documents, how many, solo or shared?
  2. **Area of focus** — name **4–8 categories** for `raw/` (their words).
  3. **Goal** — what decisions/questions should this serve? "working in 3 months"?
  4. **Entities** — who/what recurs (people, orgs, accounts) deserving a page?
  5. **Skills** — defaults `/ingest` `/query` `/lint`; offer `/setup` `/digest`.
  6. **Extensions** — **walk `extensions.md` by category & tier**; offer only
     what the preflight supports now; note Secrets each will need.
  7. **Privacy** — confirm local-first + explicit egress, or note exceptions.
- **BUILD** — write a confirmed summary; update `amanu.yaml`
  (`categories`/`entities`/`skills`/`extensions`/`credentials`).
- **VERIFY** — read the manifest summary back; let them correct it.
- **CHECKPOINT** — "this is the shape of your system — accurate?"
- **LOG** — `P1 · shape · categories=[…] skills=[…] extensions=[…]`.
- **Done when:** `amanu.yaml` records the full chosen shape.

### P2 · Scaffold *(+ credentials hygiene)*
- **TEACH** — folders are the whole database (three layers + `inbox/`); and we set
  up secret-safety *before* anything sensitive exists.
- **TAILOR** — confirm category folder names; confirm whether any chosen
  extension needs secrets.
- **BUILD** — **write `.gitignore` first** (`.env`, `*.key`, `secrets/`, caches,
  `.DS_Store`, plus the store's own ignores); create `inbox/`,
  `raw/<category>/…`, `kb/{entities,topics,sources,queries}`, `kb/index.md`,
  stub `kb/overview.md`; **the portable brain `memory/` (+ `memory/index.md`),
  the toolbox `tools/` (+ `tools/index.md`), and `daily/`**; `git init`. If
  extensions need secrets, generate a committed **`.env.example`** (var **names**
  + comments, no values) and a git-ignored **`.env`** for the user to fill — but
  only after confirming `.env` is ignored.
- **VERIFY** — show the tree; show that `git status` does **not** list `.env`.
- **CHECKPOINT** — "structure's in place and secrets are fenced off — good?"
- **LOG** — `P2 · scaffold (+ memory/ tools/ daily/) + .gitignore`.
- **Done when:** tree exists (incl. `memory/`, `tools/`, `daily/`), `git init`
  done, `.env` is ignored (if present).

### P3 · SCHEMA.md *(the constitution)*
- **TEACH** — this one file makes the agent a consistent librarian; it's the
  product.
- **TAILOR** — confirm the frontmatter fields and naming convention.
- **TEACH (architecture)** — also explain, in plain words, the memory model: the
  in-folder `memory/` is the **portable brain**, `tools/` is the **self-arming
  toolbox**, and the harness memory is for **machine-specific** facts only — so
  moving the folder preserves behaviour. This is what the entrypoints encode.
- **BUILD** — write a tailored `SCHEMA.md`: layers + folder map; file naming; the
  frontmatter spec; the **ingest / query / lint** recipes; the privacy +
  credential rules. Self-describing. Then generate the **agent entrypoints** by
  copying **`templates/AGENTS.md`** + **`templates/CLAUDE.md`** and adapting every
  `{{PLACEHOLDER}}` to this project (name, owner, categories, skills,
  `memory/` path). These wire the KB into the harness.
- **VERIFY** — read the key sections; confirm an agent opening the folder would
  load `CLAUDE.md`/`AGENTS.md`, learn the memory/tools model, and be oriented.
- **CHECKPOINT** — "this is the rulebook everything follows — happy?"
- **LOG** — `P3 · wrote SCHEMA.md + AGENTS.md/CLAUDE.md (from templates)`.
- **Done when:** `SCHEMA.md` covers layers, naming, frontmatter, the 3 recipes;
  `AGENTS.md` (+ `CLAUDE.md` pointer) exist, adapted, and describe memory/tools.

### P4 · Seed the portable brain
- **TEACH** — `memory/` is the *portable brain*: a **cross-linked graph** of
  durable facts about working this KB — conventions, gotchas, solutions — tuned
  for *method* the way `kb/` is tuned for *matter*. It travels with the folder and
  **grows** as the system is used (the self-arming loop feeds it from `daily/`).
- **TAILOR** — ask for 2–4 starting facts (summary style, "ask before inferring",
  what to always flag, any known gotcha for this domain).
- **BUILD** — write each as a one-fact file with frontmatter (`type` from the
  ontology in §C, `tags`, and any `related`/`applies-to`/`implemented-by`
  `[[links]]`) + body, and **cross-link** related facts, kb pages, or tools.
  Update `memory/index.md` as the graph's entry point. Note that `compile-memory`
  (if chosen) will later distil `daily/` logs into more facts **and tools**, and
  maintain the links.
- **VERIFY** — show the facts, their links, and the index.
- **CHECKPOINT** — "these shape *how* I work for you here — anything to add?"
- **LOG** — `P4 · seeded N brain facts (linked)`.
- **Done when:** ≥2 typed fact files + `memory/index.md` exist, with at least one
  cross-link.

### P5 · First real ingest *(prove the loop)*
- **TEACH** — run the real pipeline on one real document, narrating each step.
- **TAILOR** — ask the user to drop **one** real document in `inbox/`.
- **BUILD** — run the ingest recipe live: **consult `memory/` and `tools/index.md`
  first** (known conventions, gotchas, or a tool that already handles this kind of
  source) → read & classify → surface anything notable → rename+move into
  `raw/<category>/` → write the `kb/sources/` page → roll up into entity/topic
  pages → append `kb/log.md`, and a brief observation to today's `daily/` log →
  update `kb/index.md`. Confirm at each write.
- **VERIFY** — open the source page and the updated index together.
- **CHECKPOINT** — "that's one full ingest — clear how it flowed?"
- **LOG** — `P5 · first ingest: <source>`.
- **Done when:** the source is in `raw/`, has a `kb/sources/` page, and the index
  links it.

### P6 · First real query *(prove retrieval)*
- **TEACH** — the synthesis, not re-reading raw files, answers questions.
- **TAILOR** — ask a real question the new source can answer.
- **BUILD** — answer by reading `kb/index.md` then the relevant pages; cite them;
  offer to save to `kb/queries/`.
- **VERIFY** — confirm the answer is grounded in cited pages.
- **CHECKPOINT** — "retrieval works end to end — see how it used the wiki?"
- **LOG** — `P6 · first query`.
- **Done when:** a cited answer is produced from the synthesis.

### P7 · Build the chosen skills
- **TEACH** — skills turn the recipes into one-word commands; build only what was
  chosen.
- **TAILOR** — reconfirm the skill list; pick the next one.
- **BUILD** — scaffold each chosen skill from its build prompt, wired to
  `SCHEMA.md`. Confirm each file. Then **refresh `AGENTS.md`/`CLAUDE.md`** so they
  list the new commands.
- **VERIFY** — dry-run at least `/ingest` and `/query` (smoke test).
- **CHECKPOINT** — "your core commands exist and run — good?"
- **LOG** — `P7 · built skills: […]`.
- **Done when:** each chosen skill exists, its smoke test passes, and the agent
  entrypoints list it.

### P8 · Wire the chosen extensions
- **TEACH** — extensions attach at the edges; restate the **trust boundary**
  (inbound pulls; outbound is generic/redacted; never fuse them).
- **TAILOR** — take only the extensions chosen in P1, one at a time; for each,
  confirm its **Needs** and **Secrets** (ensure the var names are in
  `.env.example` and the user has filled `.env`).
- **BUILD** — scaffold each from its **`extensions.md` build prompt**, wired to
  `SCHEMA.md`; load any secrets from `.env`. For any **background tool** (watcher,
  scheduler), don't stop at creating the script: **register it to autostart**
  (launchd/systemd/cron per the preflight OS), **start it**, and **record it in
  `tools/index.md` and the manifest** with its start/stop/status commands. Raise
  `tier` as extensions come online, and **refresh `AGENTS.md`/`CLAUDE.md`** with
  the new commands.
- **VERIFY** — demonstrate each wired extension once (idempotent re-run); for a
  background tool, run its **status** command and show it is actually running.
- **CHECKPOINT** — "each integration you wanted is proven and (where it's a
  service) actually running — anything missing?"
- **LOG** — `P8 · wired extensions: […] · services running · tier=<…>`.
- **Done when:** each chosen extension runs once successfully; **every background
  tool is registered, started, and reports `running` via its status command**;
  `tools/index.md` + manifest list them; entrypoints updated; no secret values in
  any tracked file.

### P9 · Lint + self-document
- **TEACH** — a health pass keeps the store honest; then the system explains
  itself to your future self.
- **TAILOR** — confirm lint scope and that a `README` is wanted.
- **BUILD** — run the lint recipe (contradictions, orphans, staleness, missing
  links, gaps) → dated report in `kb/queries/`. Generate `README.md` (what it is,
  how to use the skills, decisions — summarised from `CHANGELOG.log`). Confirm
  `CLAUDE.md`/`AGENTS.md` reflect the final skill + extension set.
- **VERIFY** — review the lint report and the README together.
- **CHECKPOINT** — "the system documents itself now — does the README read right?"
- **LOG** — `P9 · lint + README`.
- **Done when:** a lint report exists and `README.md` describes the live system.

### P10 · Handoff
- **TEACH** — recap the whole system in plain words: the two memories (the
  document store + the portable brain `memory/`), the toolbox `tools/` and its
  run-state, the machine-memory split (so the folder is portable), folders,
  skills, extensions, and tier.
- **TAILOR** — ask what they want to do first on their own.
- **BUILD** — optionally a first `git commit` of the built system; set
  `last_phase: P10` in the manifest.
- **VERIFY** — walk `CHANGELOG.log` top to bottom together.
- **CHECKPOINT** — confirm they can run an ingest and a query unaided.
- **LOG** — `P10 · handoff · system live · tier=<…>`.
- **Done when:** the overall definition of done (§D) holds.

---

## G · Maturity tiers

The system grows in stages; the manifest tracks where it is:

1. **Starter** — core only (ingest, query, lint). Offline. The default delivery.
2. **Connected** — inbound feeds + outbound consumption (email, drive, research…).
3. **Automated** — it maintains itself (hooks, compile loop, cron, backup).
4. **Intelligent** — it reasons over itself (sub-agents, reconciliation, search).

Adding an extension raises the tier. Don't push a user up a tier they didn't ask
for — offer the next rung, let them choose.

---

## H · `CHANGELOG.log` format

Append-only. One entry per LOG beat. Terse, but always the *why*.

```
[2026-01-15 14:32] P2 · scaffold
  built:   .gitignore, inbox/, raw/{contracts,receipts}/, kb/{…}, git init
  why:     three-layer store; secrets fenced before any sensitive data exists
  next:    P3 — write the tailored SCHEMA.md
```

Rules: newest at the bottom; never edit past entries; reverse a decision with a
*new* entry, not by rewriting history. Update `amanu.yaml` alongside each entry.

---

## I · Quick-start

Give your agent one of these:

> **Fresh build —** *"Read `build-with-agent.md` and start the guided build with
> me at Phase 0. One phase at a time, explain before you do, confirm before you
> write, keep the `CHANGELOG.log`."*

> **Resume —** *"Read `build-with-agent.md` and `amanu.yaml`, tell me where we
> left off, and continue from `last_phase`."*

The agent drives; you steer. By Phase 10 you have a working, self-documenting
knowledge base at the tier you chose — and you understand every part because you
built it together.
