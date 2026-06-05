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
user's documents (the *matter*), plus an agent-memory folder of durable lessons
and preferences (the *method*). Build it *with* the user, never *for* them.

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

Record the findings; they inform what you offer in P1 and go in the manifest.

---

## C · Self-documenting & resumable

The system explains itself, so neither of you needs this playbook later. You keep
that true:

- **`SCHEMA.md`** — the constitution; anyone reading it can run the system.
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
  stub `kb/overview.md`; `git init`. If extensions need secrets, generate a
  committed **`.env.example`** (var **names** + comments, no values) and a
  git-ignored **`.env`** for the user to fill — but only after confirming `.env`
  is ignored.
- **VERIFY** — show the tree; show that `git status` does **not** list `.env`.
- **CHECKPOINT** — "structure's in place and secrets are fenced off — good?"
- **LOG** — `P2 · scaffold + .gitignore (+ .env.example if needed)`.
- **Done when:** tree exists, `git init` done, `.env` is ignored (if present).

### P3 · SCHEMA.md *(the constitution)*
- **TEACH** — this one file makes the agent a consistent librarian; it's the
  product.
- **TAILOR** — confirm the frontmatter fields and naming convention.
- **BUILD** — write a tailored `SCHEMA.md`: layers + folder map; file naming; the
  frontmatter spec; the **ingest / query / lint** recipes; the privacy +
  credential rules. Self-describing.
- **VERIFY** — read the key sections; confirm they match intent.
- **CHECKPOINT** — "this is the rulebook everything follows — happy?"
- **LOG** — `P3 · wrote SCHEMA.md`.
- **Done when:** `SCHEMA.md` covers layers, naming, frontmatter, the 3 recipes.

### P4 · Seed agent memory
- **TEACH** — the *method* memory: durable preferences, one fact per file,
  recalled when relevant — separate from the document store.
- **TAILOR** — ask for 2–4 standing preferences (summary style, "ask before
  inferring", what to always flag).
- **BUILD** — create the memory folder, one fact file each
  (`name`/`description`/`type` + body), and its `INDEX.md`.
- **VERIFY** — show the facts and each index line.
- **CHECKPOINT** — "these shape *how* I work for you — anything to add?"
- **LOG** — `P4 · seeded N memory facts`.
- **Done when:** ≥2 fact files + memory `INDEX.md` exist.

### P5 · First real ingest *(prove the loop)*
- **TEACH** — run the real pipeline on one real document, narrating each step.
- **TAILOR** — ask the user to drop **one** real document in `inbox/`.
- **BUILD** — run the ingest recipe live: read & classify → surface anything
  notable → rename+move into `raw/<category>/` → write the `kb/sources/` page →
  roll up into entity/topic pages → append `kb/log.md` → update `kb/index.md`.
  Confirm at each write.
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
  `SCHEMA.md`. Confirm each file.
- **VERIFY** — dry-run at least `/ingest` and `/query` (smoke test).
- **CHECKPOINT** — "your core commands exist and run — good?"
- **LOG** — `P7 · built skills: […]`.
- **Done when:** each chosen skill exists and its smoke test passes.

### P8 · Wire the chosen extensions
- **TEACH** — extensions attach at the edges; restate the **trust boundary**
  (inbound pulls; outbound is generic/redacted; never fuse them).
- **TAILOR** — take only the extensions chosen in P1, one at a time; for each,
  confirm its **Needs** and **Secrets** (ensure the var names are in
  `.env.example` and the user has filled `.env`).
- **BUILD** — scaffold each from its **`extensions.md` build prompt**, wired to
  `SCHEMA.md`; load any secrets from `.env`. Raise `tier` in the manifest as
  inbound/outbound/automation/intelligence extensions come online.
- **VERIFY** — demonstrate each wired extension once (idempotent re-run).
- **CHECKPOINT** — "each integration you wanted is proven — anything missing?"
- **LOG** — `P8 · wired extensions: […] · tier=<…>`.
- **Done when:** each chosen extension runs once successfully; manifest `tier`
  and `extensions` updated; no secret values in any tracked file.

### P9 · Lint + self-document
- **TEACH** — a health pass keeps the store honest; then the system explains
  itself to your future self.
- **TAILOR** — confirm lint scope and that a `README` is wanted.
- **BUILD** — run the lint recipe (contradictions, orphans, staleness, missing
  links, gaps) → dated report in `kb/queries/`. Generate `README.md` (what it is,
  how to use the skills, decisions — summarised from `CHANGELOG.log`).
- **VERIFY** — review the lint report and the README together.
- **CHECKPOINT** — "the system documents itself now — does the README read right?"
- **LOG** — `P9 · lint + README`.
- **Done when:** a lint report exists and `README.md` describes the live system.

### P10 · Handoff
- **TEACH** — recap the whole system in plain words: two memories, folders,
  skills, extensions, tier.
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
