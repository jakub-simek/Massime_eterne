# Massime eterne Meditation Guidelines

## Scope

This project creates Latin meditations on *Massime eterne* by Saint Alphonsus
Maria de Liguori. Each meditation normally treats one individual paragraph of
the Italian base text, not an entire daily meditation, chapter, or theme.

The shared rules in `shared/latin-meditations-guidelines/` apply. This local
overlay defines the Massime-specific source order, paragraph scope, metadata,
and citation practice.

## Source Order

Before writing or revising a meditation, read these files in order:

1. `shared/latin-meditations-guidelines/skills/latin-meditations-core/SKILL.md`
2. The relevant files in `shared/latin-meditations-guidelines/guidelines/`
3. This local overlay: `planning/meditations-guidelines.md`
4. The relevant TEI div in `edition/it/tei/massime-eterne.xml`
5. Any existing meditation on the same TEI div, paragraph, or closely related
   theme

For source control and edition context, consult when needed:

- `docs/editorial-guidelines.md`
- `edition/it/tei/README.md`
- `sources/intratext/manifest.json`
- `data/bibliography.yml`

## Primary Text

The primary source is the Italian TEI file:

```text
edition/it/tei/massime-eterne.xml
```

The normal meditation unit is one textual paragraph, encoded as a `<p>` inside
one of these TEI divs:

- `preparation-p2hq`
- `acts-p2hr`
- `meditation-p2hs`
- `meditation-p2ht`
- `meditation-p2hu`
- `meditation-p2hv`
- `meditation-p2hw`
- `meditation-p2hx`
- `meditation-p2hy`

The `sigla-p2hp` div is a reference section and is not normally a meditation
source.

## Preparatory Method

The opening directions in `preparation-p2hq` are binding methodological
guidance for composing and reading every Latin meditation in this project.
They should shape the meditation's spiritual movement even when they are not
the paragraph being meditated on.

Before writing, the author should recall the acts named there:

- renew faith in the presence of God;
- place the soul before God and adore him;
- humble oneself and ask pardon;
- ask light from God for the love of Jesus Christ;
- commend the meditation to Mary Most Holy and the saints.

The meditation itself should follow the same practical pattern:

- proceed slowly through the selected paragraph;
- draw out the eternal truth contained in it;
- lead toward a concrete resolution against a vice or toward a specific virtue;
- conclude, when appropriate, with acts of thanksgiving, offering, petition,
  Marian recourse, and intercession for the Church, sinners, the just, and the
  souls in purgatory.

Do not turn these preparatory acts into a rigid visible template for every file.
They are the interior grammar of the meditation, not an added checklist to be
recited mechanically.

## Paragraph Locator

Until paragraph-level `xml:id` values are added to the TEI, use this locator:

```text
<tei-div-id>:p<n>
```

The paragraph number is counted among textual `<p>` elements inside the chosen
TEI div, excluding `<head>`, `<milestone>`, and standalone `<pb>` elements.
Printed page breaks embedded inside a paragraph do not change the paragraph
number.

Example:

```text
meditation-p2hs:p2
```

This means the second textual paragraph inside the Sunday meditation div.

## Metadata

Each meditation file should use YAML front matter with these fields:

```yaml
---
id: "me-la-0001"
title: "Meditatio ..."
lang: "la"
status: "draft"
primary_source: "edition/it/tei/massime-eterne.xml#meditation-p2hs:p2"
primary_div: "meditation-p2hs"
primary_paragraph: 2
primary_incipit: "Considera, come in punto di morte..."
source_language: "it"
source_status: "first-pass TEI from IntraText"
---
```

Use `status: draft`, `review`, or `ready`.

## Required Structure

A normal meditation should use this structure unless there is a clear reason to
adapt it:

```markdown
## Textus fundamentalis
## Expositio spiritualis
## Amplificatio
## Applicatio spiritualis
## Conclusio
```

The `Textus fundamentalis` section should quote the selected Italian paragraph,
or a sufficiently complete excerpt from it, in Italian. The Latin meditation
then unfolds that paragraph contemplatively and ascetically.

## Language

- The meditation itself is written in Ecclesiastical Latin.
- The primary quotation from Alphonsus remains in Italian.
- Italian quotations preserve the source wording and punctuation from the TEI
  unless an editorial correction is explicitly documented.
- German may be used in working notes or translation drafts, but not in the
  final Latin meditation body.

## Citation Style

The first reference to the selected paragraph should use the full locator:

```text
S. Alfonso Maria de Liguori, Massime eterne, meditation-p2hs:p2
```

Later references to the same paragraph may use:

```text
Massime eterne, meditation-p2hs:p2
```

If a printed page is relevant, add the TEI page marker:

```text
Massime eterne, meditation-p2hs:p2, p. 383
```

Direct quotations from the Italian base text are italicized and followed by the
locator in parentheses. Paraphrases use `cf.`.

## Required Source Families

For each paragraph meditation, use sources only where they genuinely illuminate
the selected paragraph. Do not force all families into every meditation.

Normally preferred:

- Scripture, especially eschatological, penitential, sapiential, and Gospel
  texts connected to the paragraph
- traditional Catholic ascetical theology
- St. Alphonsus as the primary author and, when useful, as a parallel witness in
  other works
- Roman Catechism or scholastic theology when doctrinal precision is needed
- patristic or medieval witnesses when they clarify a major theme

Normally not required:

- liturgical context
- feast-day structure
- broad Marian anthology material unrelated to the paragraph

## Marian Integration

A Marian component should normally be present, but it must arise organically
from the paragraph. In *Massime eterne*, this may often be brief: Mary as refuge
of sinners, teacher of repentance, mother at the hour of death, or model of
faithful remembrance of eternal things.

Do not append a Marian paragraph mechanically.

## File Naming

Latin meditations should normally be stored under:

```text
meditations/la/
```

Use stable, sortable filenames:

```text
001-meditation-p2hs-p2.md
002-meditation-p2hs-p3.md
```

If multiple meditations are written on the same paragraph, add a short topic
slug:

```text
001-meditation-p2hs-p2-finis-hominis.md
```

## Review Checklist

Before marking a meditation ready, verify:

- the selected TEI div and paragraph number exist;
- the meditation treats one paragraph, not a whole daily meditation;
- the Italian `Textus fundamentalis` matches the TEI source;
- the opening preparatory directions in `preparation-p2hq` have shaped the
  meditation's movement toward presence of God, humility, light, resolution,
  and prayer;
- all direct quotations are real, traceable, italicized, and immediately cited;
- paraphrases use `cf.`;
- the Latin meditation remains in Ecclesiastical Latin;
- the movement is contemplative and ascetical, not merely explanatory;
- the Marian dimension is organic;
- source references follow the local paragraph locator;
- the final Latin correction pass has been completed.
