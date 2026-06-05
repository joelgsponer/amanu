---
type: gotcha
tags: [figures, invoices, taxes]
applies-to: [[2026-01-12_acme_invoice_4471]]
related: []
---

# Never infer figures the source doesn't state

When a document is missing a number (VAT, a total, a rate), record what's observable
and **flag the gap** — don't compute or assume it. Distilled by `/compile` from the
2026-01-12 ingest, where the Acme invoice omitted VAT and the owner wanted it
surfaced, not guessed.

**How to apply:** in `/ingest`, write `Source does not specify` for any absent
figure and add a note; raise it again at tax time rather than silently filling it in.
