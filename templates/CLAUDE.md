<!--
  TEMPLATE — the build agent copies this into the built knowledge base's root as
  CLAUDE.md. It is a thin pointer so Claude Code and other tools that read
  CLAUDE.md land on the canonical AGENTS.md. Keep them in sync; AGENTS.md wins.
-->
# CLAUDE.md — {{KB_NAME}}

This project is an **amanu knowledge base**. The operating guide is
**[AGENTS.md](AGENTS.md)** — read it first.

In short: read `SCHEMA.md` for the conventions; use the listed skills (core:
`/ingest` `/query` `/lint` `/compile` `/healthcheck`); keep the store lean (pull
pages on demand, don't bulk-load `raw/` or `kb/sources/`). Your **portable brain**
is `memory/` (everything about working this KB — keep adding to it; grow it with
`/compile`) and your **toolbox** is `tools/` (self-arming scripts; check
`tools/index.md` and report any background service that should be running but isn't,
or just run `/healthcheck`). The harness memory is for **machine-specific** facts
only, so moving this folder preserves your behaviour.

See **[AGENTS.md](AGENTS.md)** for the full version.
