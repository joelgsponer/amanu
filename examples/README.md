# examples/ — a worked Starter system

A tiny, **fictional** amanu knowledge base, shown after a Starter build (P0–P10)
for an imaginary freelancer tracking client paperwork. It exists so an agent (or a
curious human) can see the *shape* of a finished system — the manifest, the
self-documenting logs, one source page, one entity, one memory fact — without
running a build. **All data here is invented; nothing is personal.**

```
examples/
├── amanu.yaml                     # the manifest — tier, skills, categories
├── CHANGELOG.log                  # the build story (excerpt)
├── kb/
│   ├── index.md                   # the catalog
│   ├── sources/2026-01-12_acme_invoice_4471.md
│   └── entities/acme.md
├── memory/
│   ├── index.md
│   └── ask-before-inferring-amounts.md
└── reports/                       # /healthcheck would write HTML here
```

A real build also has `raw/`, `inbox/`, `tools/`, `daily/`, `SCHEMA.md`, and the
`AGENTS.md`/`CLAUDE.md` entrypoints (generated from `templates/`). Those are
omitted here to keep the example small. The conventions are in
[`../templates/SCHEMA.md`](../templates/SCHEMA.md).
