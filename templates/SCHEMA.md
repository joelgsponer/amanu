<!--
  TEMPLATE — the build agent copies this into the built knowledge base's root as
  SCHEMA.md (P3) and replaces every {{PLACEHOLDER}} with this project's real
  values. SCHEMA.md is the CONSTITUTION: anyone (human or agent) who reads it can
  run the system. Keep it self-describing; when conventions change, edit it here
  and refresh the entrypoints. Fill every {{...}}; delete guidance comments you
  don't need, but keep the section structure.
-->
# SCHEMA.md — {{KB_NAME}}

The conventions for {{OWNER}}'s amanu knowledge base. This file is authoritative;
the skills below implement exactly what it specifies.

## The three layers (+ supporting folders)

1. **`raw/`** — immutable source documents, organised by category. **Never edit a
   source** except to rename/move it. Categories: {{CATEGORIES}}.
2. **`kb/`** — the synthesis you maintain: `entities/`, `topics/`, `sources/`,
   `queries/`, plus `index.md` (catalog), `log.md` (operations), `overview.md`
   (scope/dashboard). Markdown only; frontmatter on every page; `[[wiki-links]]`.
3. **`memory/`** — the **portable brain**: durable facts about *how to work this
   KB* (conventions, gotchas, solutions), one typed fact per file, cross-linked,
   indexed in `memory/index.md`. (Method, the way `kb/` is matter.)

Supporting: `inbox/` (drop zone for new sources) · `tools/` (self-arming toolbox +
`tools/index.md`) · `daily/` (raw session logs that feed `/compile`) · `reports/`
(`/healthcheck` HTML) · `design/` (the design system, if installed) · `amanu.yaml`
(the manifest) · `CHANGELOG.log` (build story).

**Convention — visual outputs default to the design system, but the user's wishes
win.** Any generated visual output (the `/healthcheck` report, exported reports,
static sites, charts) uses the `design/` tokens **as the default** — applied only
when the user hasn't asked for something different. The manifest records the choice
as **`design: basel-default | custom`** (default `basel-default`); when it's
`custom`, honour the user's own style instead and never impose the predefined
design. The shipped `templates/design/` (Basel defaults) is the fallback when no
`design/` exists yet.

## File naming

- **`raw/`:** `{{RAW_NAMING}}` <!-- e.g. YYYY[-MM[-DD]]_<issuer>_<topic>[_<who>].<ext>; ASCII-only; underscores between fields -->
- **`kb/`:** lowercase, hyphens (e.g. `entity-name.md`, `topic-2026.md`). Source
  pages mirror the `raw/` filename minus extension.

## Frontmatter spec

Every `kb/` page carries YAML frontmatter. Fields:
```yaml
---
type: {{PAGE_TYPES}}          # e.g. source | entity | topic | query | overview
category: {{CATEGORIES}}
date: YYYY-MM-DD
related: [ ... ]              # [[wiki-link]] targets
tags: [ ... ]
{{EXTRA_FIELDS}}             # e.g. issuer, subject, amount, source_url — per type
---
```
`memory/` facts use: `type` (`convention|gotcha|solution|preference|procedure|tool`),
`tags`, and links (`related`/`solves`/`supersedes`/`applies-to`/`implemented-by`).

## The five core recipes

### `/ingest` — file & cross-reference a new document
Consult `memory/` + `tools/index.md` first → read & classify (category, type, date,
issuer, subject) → surface anything notable to the user → rename + move into
`raw/<category>/` → write the `kb/sources/` page → roll up into entity/topic pages →
append one line to `kb/log.md` and a brief observation to today's `daily/` log →
update `kb/index.md`. Confirm before each write. Idempotent: key a source by its
filename so re-ingest updates rather than duplicates.

### `/query` — answer from the synthesis
Read `kb/index.md`, then the relevant pages (prefer the synthesis over re-reading
`raw/`). Answer with citations to the pages used; say plainly when the store lacks
the answer. Offer to save substantial answers to `kb/queries/`. Append a one-line
observation to `daily/`.

### `/lint` — content health check
Scan `kb/` for contradictions, orphan pages, stale claims, missing `[[links]]`, and
data gaps. Write a dated report to `kb/queries/`. Proposes, never auto-edits.

### `/compile` — the self-arming loop *(on demand)*
Read the `daily/YYYY-MM-DD.md` logs since the last compile and:
(1) extract durable lessons/gotchas/preferences; **dedupe by fact title/slug**
(case-insensitive — a new fact whose slug already names a `memory/` file updates it,
never duplicates); write each as a typed+linked fact file `memory/<slug>.md` and
update `memory/index.md`;
(2) detect recurrent tasks/automations — a task that recurs **≥ the threshold**
(default 3; configurable) becomes a candidate `tools/` script, catalogued in
`tools/index.md` with start/stop/status. New facts/tools are **proposed for
approval** by default, or written directly if the user pre-approved auto-write.
**Idempotency key:** record the last compiled date in `memory/index.md` and skip
day-files already processed. (The Automated tier schedules this; here you run it.)
Verify by compiling one day and confirming ≥1 fact/tool, with no duplicate of an
existing fact.

### `/healthcheck` — audit the running system → HTML report
Verify *the machinery* (where `/lint` checks content). Emit **one section per check
area**, each row `pass | warn | fail` with a remediation hint:
1. **manifest vs. reality** — every skill/extension/tool in `amanu.yaml` exists on disk;
2. **services** — each background tool's `status` + boot-persistence + **heartbeat**
   (`tools/<name>.state` `last_ok` newer than 1.5× its manifest `interval`);
3. **secret hygiene** — `.env` git-ignored & untracked; no secret-shaped strings in
   tracked files; `credentials:` are names only;
4. **KB integrity** — frontmatter present, no broken `[[links]]`, no orphans, `kb/index.md` covers disk;
5. **loop freshness** — `daily/` written recently and `/compile` run since;
6. **git** — repo initialized; uncommitted/untracked summary.
**Output:** one self-contained HTML file (**inline CSS, no external/CDN assets**) at
`reports/healthcheck-YYYY-MM-DD.html` — a status banner + the per-section table.
**Style:** read the design tokens (`design/tokens.css` if the `design-system`
extension is installed, else the shipped `templates/design/tokens.css` Basel
default) and **embed their CSS-variable values inline** — never link an external
asset. Honour `design: custom` in the manifest (the user chose another style).
Reports, never auto-fixes. **Idempotency key:** overwrite the same-day report.
Verify by running once and opening the report; a deliberately-stopped service shows
`fail`.

## Privacy & credentials

- **Local-first.** Nothing leaves the machine without explicit approval; cloud/web
  steps are opt-in and named. Privacy stance: {{PRIVACY}}.
- **Secrets** live only in a git-ignored `.env` (names mirrored in `.env.example`);
  **never** in a tracked file, the manifest, or `CHANGELOG.log`. If a *source*
  contains a secret, stop and flag it for removal.
- Account numbers/IBANs/IDs may live in `kb/` entity pages (local repo), but keep
  them out of user-facing summaries and commit messages unless asked.

## Logs & manifest

- **`kb/log.md`** — operations, one line: `[YYYY-MM-DD HH:MM] <verb> <object> · <result>`.
- **`CHANGELOG.log`** — the build/evolution story (decision + artifact + why).
- **`amanu.yaml`** — machine-readable state (tier, categories, entities, skills,
  extensions, credentials [names only], `tools:` run-state + heartbeat, privacy).
