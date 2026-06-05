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

**Convention — visual outputs default to the design system.** Any generated visual
output (the `/healthcheck` report, exported reports, static sites, charts) uses the
`design/` tokens by default unless that output explicitly opts out. The shipped
`templates/design/` (Swiss defaults) is the fallback when no `design/` exists yet.

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
Read the `daily/` logs and (1) extract durable lessons/gotchas/preferences, dedupe
against existing `memory/` facts, write new typed+linked fact files, update
`memory/index.md`; (2) detect recurrent tasks/automations and propose or generate a
`tools/` script (catalogued with start/stop/status). Idempotent: skip
already-compiled days. (The Automated tier schedules this; here you run it.)

### `/healthcheck` — audit the running system → HTML report
Verify *the machinery* (where `/lint` checks content): manifest vs. reality (every
skill/extension/tool exists); each background service's `status` + boot-persistence
+ heartbeat freshness; secret hygiene (`.env` ignored & untracked, no secrets in
tracked files); KB integrity (frontmatter, no broken links, no orphans, index
coverage); self-arming-loop freshness (`daily/` written, `/compile` run recently).
Write a single self-contained HTML file (**inline CSS, no external/CDN assets**) to
`reports/healthcheck-YYYY-MM-DD.html` with a status banner and a per-section
pass/warn/fail table + remediation hints. **Style it with the design system** —
`design/tokens.css` if the `design-system` extension is installed, else the shipped
`templates/design/report.html` Swiss default. Reports, never auto-fixes. Idempotent:
overwrite the same-day report.

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
