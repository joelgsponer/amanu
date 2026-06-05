# amanu design system — the Basel School (Armin Hofmann)

The default visual language for every generated output. It is oriented on the
**Basel School of Design** (Schule für Gestaltung Basel) as taught by **Armin
Hofmann** (1920–2020) and set out in his *Graphic Design Manual / Methodik der
Form- und Bildgestaltung* (1965). The point is not a "look" but a method:
objective, reduced, timeless form. `tokens.css` and `report.html` implement it;
this file explains *why* so any agent tuning the system stays inside the tradition.

## The principles → how the tokens serve them

1. **The elemental — point · line · plane.** Form is built from the three
   irreducible elements (*Punkt, Linie, Fläche*). Encoded as three rule weights:
   `--w-hair` (line), `--w-rule` (a drawn structural edge), `--w-plane` (a solid
   band that reads as mass). A pill is a *point*; a divider is a *line*; the black
   header band is a *plane*.

2. **Contrast is the generative force.** A composition comes alive from opposing
   pairs — large/small, light/bold, dynamic/static, dense/open. So the type scale
   jumps hard (`--fs-display` ≈ 3.16rem against a 1rem body) and weight is paired
   deliberately: a **light** large display set against **bold tracked** labels.

3. **Economy of means.** Maximum effect from the minimum vocabulary; clarity
   through omission. Hence `--radius: 0`, and no shadows, gradients, or ornament —
   nothing that does not carry information.

4. **Activated white space.** Negative space is a working element, not emptiness;
   form and counter-form carry equal weight. Spacing is generous and on a strict
   8px grid (`--s-*`); body text is held to a `--measure` of ~66ch, flush-left,
   ragged-right.

5. **Typography as form.** The grotesque (Akzidenz-Grotesk → Helvetica lineage) is
   treated as both objective message and abstract texture. A dependency-free system
   stack leads with Helvetica; labels use tracked caps (`--track-caps`); display
   leading is tight (`--lh-tight`).

6. **The grid as latent order.** An underlying structure (`--grid-cols: 12`),
   applied with discipline but not mechanically — asymmetric, flush-left balance
   over centred symmetry.

7. **Black-and-white primacy, colour as structure.** The palette is near-black ink
   on a restrained near-white, with **one** red (`--accent`) used *structurally* —
   never to decorate. Semantic report colours are muted so the red stays the only
   loud voice.

8. **Objectivity / timelessness.** Universal, ahistorical solutions over fashion;
   the designer's hand subordinate to the problem. When in doubt, remove rather
   than add, and prefer the neutral choice.

## Using it in outputs

Every generated visual output (the `/healthcheck` report, exported reports, static
sites, charts) **inlines these tokens by default** and follows the rules above —
**this is the default, not a mandate**. It applies whenever the user hasn't asked
for something different; if the user wants another style (for one output or in
general), honour that instead — never impose this design over an explicit wish.
When you *are* tuning it (the `design-system` extension guides you), keep the
principles: if a change adds ornament, breaks the black-&-white-plus-one-red
discipline, or softens the contrast, it is leaving the tradition.
