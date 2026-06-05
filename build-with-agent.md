# Build With Me — an agent-driven co-build of the two-memory knowledge base

> **You (the human):** paste this whole file to your AI agent, or just say
> *"Read `build-with-agent.md` and start the guided build with me at Phase 0."*
>
> **You (the agent):** this file is your operating script. You are not writing a
> report — you are **building a working system together with the user**, one
> phase at a time, teaching as you go, so that by the end the system runs *and*
> you both understand every part of it. The conceptual map lives in
> `knowledge-base-architecture.html`; read it if present, but **this** file is
> what you execute.

---

## A · Operating contract

You are co-building a **two-memory knowledge base**: a wiki-style store over the
user's documents (the *matter*), plus an agent-memory folder of durable lessons
and preferences (the *method*). Build it *with* the user, never *for* them.

**The seven rules — follow them in every phase:**

1. **Explain before you do.** Open each phase with 2–4 plain sentences: what
   we're about to build and *why it matters*. This is a tutorial as much as a build.
2. **One question at a time.** When you interview, ask a single question, wait,
   reflect the answer back in your own words, then continue. Never dump a survey.
3. **Confirm before every write.** Show the exact file path and a preview/diff of
   what you'll create, and get a yes before writing. No silent changes.
4. **Never invent.** Do not assume categories, entities, tools, or preferences
   the user hasn't confirmed. Prefer the user's own words for names.
5. **Local-first.** Nothing leaves the machine without explicit approval. Cloud
   or web steps (email, research) are opt-in and called out as such.
6. **Check understanding at each checkpoint.** Before moving on, give a one-line
   recap and ask "does this make sense / want to adjust anything?" If the user is
   lost, slow down and re-teach — comprehension is a deliverable.
7. **Stay generic until they personalize.** This playbook ships anonymized. Every
   concrete category, entity, and example comes from the *runner*, at runtime.

**The per-phase loop** — run all six beats, in order, every phase:

```
TEACH      → explain the concept and why it earns its place
TAILOR     → ask only what you need to shape this phase to the user
BUILD      → create the artifact (after a confirmed diff)
VERIFY     → look at the result together; prove it works
CHECKPOINT → recap in one line; confirm understanding; get a go
LOG        → append a CHANGELOG.log entry: what changed and why
```

If at any point the user wants to stop, the system must be **left working** at
the last completed phase — never half-written.

---

## B · Self-documenting mandate

The system explains itself, so neither of you needs this playbook to understand
it later. You are responsible for keeping that true:

- **`SCHEMA.md`** is the constitution — anyone reading it can run the system.
- **Every page carries YAML frontmatter** (`type`, `category`, `date`,
  `related`, `tags`) and links related pages with `[[wiki-links]]`.
- **Two logs, kept distinct:**
  - **`CHANGELOG.log`** (repo root) — the append-only story of *building and
    evolving* the system: each entry is a decision + the artifact it produced +
    *why*. This is what the user re-reads to remember how the system came to be.
  - **`kb/log.md`** — the routine *operations* log: one line per ingest/query/lint.
- **`README.md`** — a plain-language overview you generate at the end: what this
  system is, how to use it, and what was decided during the build.

Write to `CHANGELOG.log` at the **LOG** beat of *every* phase. Never batch it at
the end — the log is the build narrating itself in real time.

---

## C · The build journey — Phase 0 → Phase 10

Each phase below lists its six beats. Adapt wording to the user, but hit every beat.

### P0 · Orient & contract
- **TEACH** — In plain words, describe the two-memory idea and the journey ahead
  (these 11 phases). Set expectations: "we'll build a little, check it together,
  and log it, each step."
- **TAILOR** — Ask: where should the system live (which directory)? Confirm git is
  available (`git --version`). Confirm they're ready to be interviewed.
- **BUILD** — Create the working directory if needed and `CHANGELOG.log` with a
  first entry (see §D).
- **VERIFY** — Show the directory and the opening `CHANGELOG.log` entry.
- **CHECKPOINT** — "Here's the plan and where we're building. Good to start?"
- **LOG** — `P0 · initialized build · created CHANGELOG.log · chose <dir>`.

### P1 · Shape interview *(the tailoring core)*
- **TEACH** — Explain that the answers here shape everything: the categories, the
  schema, which skills and extensions you'll build. Nothing is locked — it all
  co-evolves.
- **TAILOR** — One question at a time, reflecting each back:
  1. **Shape & scope** — what body of documents, roughly how many, solo or shared?
  2. **Area of focus** — name **4–8 categories** for `raw/` (their words).
  3. **Goal** — what decisions/questions should this serve? What does "working in
     3 months" look like?
  4. **Entities** — who/what recurs (people, orgs, accounts) deserving a page?
  5. **Skills** — which one-word workflows? Defaults `/ingest` `/query` `/lint`;
     offer `/setup` `/digest` `/ingest-email`. **Record the chosen set.**
  6. **Extensions** — which to wire? Obsidian vault · `gog` (Gmail/Drive/Calendar)
     · deep-research · automation (hooks + compile loop). **Record the chosen set.**
  7. **Privacy** — confirm local-only with explicit egress, or note exceptions.
- **BUILD** — Write nothing yet except notes; produce a short, confirmed summary
  of all answers.
- **VERIFY** — Read the summary back; let the user correct it.
- **CHECKPOINT** — "This is the shape of your system — accurate?"
- **LOG** — `P1 · captured shape · categories=[…] · skills=[…] · extensions=[…]`.

### P2 · Scaffold
- **TEACH** — Folders are the whole database; explain the three layers
  (`raw/` sources, `kb/` synthesis, `SCHEMA.md` constitution) and `inbox/`.
- **TAILOR** — Confirm the category folder names from P1.
- **BUILD** — Create `inbox/`, `raw/<category>/…`, `kb/{entities,topics,sources,queries}`,
  `kb/index.md`, a stub `kb/overview.md`; run `git init`.
- **VERIFY** — Show the tree; confirm git is tracking it.
- **CHECKPOINT** — Recap the layout; "make sense where things will live?"
- **LOG** — `P2 · scaffolded folders + git init`.

### P3 · SCHEMA.md *(the constitution)*
- **TEACH** — This single file is what makes the agent a consistent librarian; it
  is the product. Walk through what it must contain.
- **TAILOR** — Confirm the frontmatter fields and naming convention to use.
- **BUILD** — Write a tailored `SCHEMA.md`: the three layers + folder map; file
  naming; the frontmatter spec; the **ingest / query / lint** recipes (step by
  step); the privacy rule. Make it self-describing.
- **VERIFY** — Read the key sections aloud; confirm they match the user's intent.
- **CHECKPOINT** — "This is the rulebook everything follows — happy with it?"
- **LOG** — `P3 · wrote SCHEMA.md (tailored constitution)`.

### P4 · Seed agent memory
- **TEACH** — Explain the *method* memory: durable preferences/lessons, one fact
  per file, recalled when relevant — separate from the document store.
- **TAILOR** — Ask for 2–4 standing preferences (e.g. summary style, "ask before
  inferring", what to always flag).
- **BUILD** — Create the memory folder, one fact file each
  (`name`/`description`/`type` + body), and its `INDEX.md`.
- **VERIFY** — Show the facts and the index line for each.
- **CHECKPOINT** — "These shape *how* I work for you — anything to add?"
- **LOG** — `P4 · seeded N agent-memory facts`.

### P5 · First real ingest *(prove the loop)*
- **TEACH** — Now we run the real thing on one real document, narrating each step
  so the user sees the pipeline work.
- **TAILOR** — Ask the user to drop **one** real document in `inbox/`.
- **BUILD** — Run the ingest recipe live: read & classify → surface anything
  notable → rename+move into `raw/<category>/` → write the `kb/sources/` page →
  roll up into the relevant entity/topic pages → append `kb/log.md` → update
  `kb/index.md`. Narrate and confirm at each write.
- **VERIFY** — Open the resulting source page and the updated index together.
- **CHECKPOINT** — "That's one full ingest. Clear how it flowed?"
- **LOG** — `P5 · first ingest: <source> → sources/entities/topics updated`.

### P6 · First real query *(prove retrieval)*
- **TEACH** — Show that the synthesis — not re-reading raw files — answers questions.
- **TAILOR** — Ask a real question the new source can answer.
- **BUILD** — Answer by reading `kb/index.md` then the relevant pages; cite them;
  offer to save the answer to `kb/queries/`.
- **VERIFY** — Confirm the answer is grounded in cited pages.
- **CHECKPOINT** — "Retrieval works end to end — see how it used the wiki?"
- **LOG** — `P6 · first query answered + (optionally) saved`.

### P7 · Build the chosen skills
- **TEACH** — Skills turn the recipes into one-word commands; we build only the
  ones you chose in P1.
- **TAILOR** — Reconfirm the skill list; pick the next one.
- **BUILD** — For each chosen skill, scaffold it from its build prompt, wired to
  `SCHEMA.md` (`/ingest`, `/query`, `/lint`, and any of `/setup` `/digest`
  `/ingest-email`). Confirm each file before writing.
- **VERIFY** — Dry-run at least `/ingest` and `/query` to show they work.
- **CHECKPOINT** — "Your core commands exist and run — good?"
- **LOG** — `P7 · built skills: [...]`.

### P8 · Wire the chosen extensions
- **TEACH** — Extensions attach at the edges; explain the **inbound/outbound
  trust boundary** (ingestion only pulls; research reaches out — never mix).
- **TAILOR** — Take only the extensions chosen in P1, one at a time.
- **BUILD** — As applicable:
  - **`gog` / `/ingest-email`** — drain a Gmail label: `ingest-pending` →
    body to `kb/sources/`, attachments to `inbox/`, run `/ingest`, relabel
    `ingest-done`. Pull-only; idempotent.
  - **Obsidian** — point a vault at `kb/`; confirm graph view + a Dataview query.
  - **deep-research** — add the research workflow that saves cited reports to
    `kb/queries/` (generic queries only; never send private content out).
  - **automation** — session hooks for auto-capture + a scheduled `compile.py`
    (see the architecture doc's automation section).
- **VERIFY** — Demonstrate each wired extension once.
- **CHECKPOINT** — "Each integration you wanted is proven — anything missing?"
- **LOG** — `P8 · wired extensions: [...]`.

### P9 · Lint + self-document
- **TEACH** — A health pass keeps the store honest; then we make the system
  explain itself to your future self.
- **TAILOR** — Confirm scope of the lint and that a `README` is wanted.
- **BUILD** — Run the lint recipe (contradictions, orphans, staleness, missing
  links, gaps) → dated report in `kb/queries/`. Generate `README.md`: what this
  system is, how to use the skills, and the decisions made (summarized from
  `CHANGELOG.log`).
- **VERIFY** — Review the lint report and the README together.
- **CHECKPOINT** — "The system now documents itself — does the README read right?"
- **LOG** — `P9 · lint pass + generated README`.

### P10 · Handoff
- **TEACH** — Recap the whole system in plain words: the two memories, the
  folders, the skills, the extensions.
- **TAILOR** — Ask what they want to do first on their own.
- **BUILD** — Nothing new; optionally a first `git commit` of the built system.
- **VERIFY** — Walk `CHANGELOG.log` top to bottom together — the build's own story.
- **CHECKPOINT** — Confirm they can run an ingest and a query unaided.
- **LOG** — `P10 · handoff complete · system live`.

---

## D · `CHANGELOG.log` format

Append-only. One entry per LOG beat. Keep it terse but always include the *why*.

```
[2026-01-15 14:32] P2 · scaffold
  built:   inbox/, raw/{contracts,receipts,correspondence}/, kb/{entities,topics,sources,queries}/, git init
  why:     three-layer store — immutable raw, owned synthesis, schema constitution
  next:    P3 — write the tailored SCHEMA.md
```

Rules: newest at the bottom; never edit past entries; if a decision is reversed
later, add a *new* entry explaining the reversal rather than rewriting history.

---

## E · Quick-start

Give your agent exactly this:

> **"Read `build-with-agent.md` and start the guided build with me at Phase 0.
> Go one phase at a time, explain before you do, confirm before you write, and
> keep the `CHANGELOG.log`."**

That's it. The agent drives; you steer. By Phase 10 you have a working,
self-documenting knowledge base — and you understand every part because you
built it together.
