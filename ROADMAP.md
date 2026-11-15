# Project roadmap

This page is the human-readable checklist for completing Wine Theory Anki. It complements
the two machine-readable editorial ledgers:

- [`import/progress.yaml`](import/progress.yaml) tracks migration of the private legacy
  source notes into original English cards.
- [`import/quality-review.yaml`](import/quality-review.yaml) tracks the chapter-wide card
  quality pass: isolation, credible distractors, balanced choice length, useful
  explanations and natural French.

The figures below are a snapshot from **2026-11-15**. Source notes and finished cards are
different units: one source note may be split into several cards, merged with another note
or rejected.

## Current snapshot

| Measure | Complete | Remaining | Progress |
| --- | ---: | ---: | ---: |
| Legacy source notes resolved | 3,890 / 4,075 | 185 | 95.5% |
| Cards with French | 3,516 / 3,519 | 3 | 99.9% |
| Release-eligible cards with French | 3,516 / 3,516 | 0 | 100% |
| Draft cards | — | 3 | — |
| Chapters with agent review complete | 45 | — | — |

To obtain the live migration count, run:

```bash
uv run wset3-anki import-status
```

All translated MCQs have matching English and French choice counts and correct answer
indexes. Every chapter that has been started is fully migrated, reviewed and bilingual;
the 45 completed chapter passes are recorded as `awaiting-human` in the quality ledger.

Since 2026-11-13, writers and critics verify fragile facts (dates, figures, rankings,
legal rules, named anecdotes) against authoritative external sources and record them in
`review.sources`; see "External fact-checking" in
[`import/AGENT_PLAYBOOK.md`](import/AGENT_PLAYBOOK.md). Chapters completed before that
rule (c07, c08, c09, c33, c38, c39, c43) received a dedicated sourced re-check.

Packages are built and published by CI (`.github/workflows/ci.yml`) on every push to
`main`; there is no manual build step.

## Immediate priorities

### 1. Triage the unclassified notes

All named chapters are migrated. Only the 185 unclassified source notes remain
(`c00-unclassified`). Many will duplicate facts already carded in their proper chapter
and can be rejected or merged.

- [ ] Assign each note to its chapter, or reject it as a duplicate.
- [ ] Convert the remaining notes into original English cards in their chapter files,
  checking fragile facts against external sources, with a critic pass per lot.
- [ ] Translate the new cards and update the chapters' quality-ledger entries.

### 2. Resolve the remaining drafts

- [ ] `wine-natural-001` and `wine-barrique-two-years-001` (Winemaking and Maturation).
- [ ] `vm-canopy-trellis-choice-001` (Vineyard Management).

Each needs stronger distractors and a French block, or a deliberate rejection.

### 3. Final audit (deferred)

- [ ] Once every chapter is migrated, run a final independent audit with Claude Fable over
  all chapters marked `awaiting-human`, in place of a manual human pass. Deferred until
  migration is finished and token budget allows.

## Completed chapters

All chapters below have zero pending source notes, reviewed English cards, aligned
French, and an `awaiting-human` entry in the quality ledger.

- Foundations: SAT, The Vine, Growing Environment, Vineyard Management, Winemaking and
  Maturation, White and Sweet Winemaking, Red and Rosé Winemaking, Price of Wine, Wine
  and the Law.
- France: Introduction, Bordeaux, South West, Burgundy, Beaujolais, Alsace, Loire,
  Northern Rhône, Southern Rhône, Southern France, Jura, Savoie.
- Rest of Europe: Germany, Austria, Tokaj, Greece, Italy (Introduction, Northern,
  Central, Southern), Spain, Portugal.
- New World: USA Introduction, California, Pacific Northwest, Canada, Chile, Argentina,
  South Africa, Australia, New Zealand.
- Sparkling and fortified: Sparkling Production, Sparkling Wines, Sherry, Port,
  Fortified Muscat.

## Quality and release checklist

- [ ] Resolve the three remaining draft cards or deliberately reject them.
- [x] Complete agent quality review for every started chapter.
- [ ] Triage the 185 unclassified notes and review any cards they produce.
- [ ] Run the final Fable audit on chapters marked `awaiting-human` (after migration).
- [ ] Run `make check` after every change.
- [ ] Inspect representative MCQ, basic and cloze cards from the CI packages on desktop
  and mobile.
- [ ] Keep the rolling GitHub release healthy after pushes to `main`.
- [ ] Create a versioned release when migration, translation and final QA reach the desired
  milestone.

## Definition of done for a chapter

A chapter is complete when:

1. its source ledger has no pending or in-progress notes;
2. every retained fact is represented by an original, reviewed English card;
3. every released English card has a natural French block where translation is in scope;
4. English and French MCQs have the same choice count and correct-answer index;
5. isolation, distractor credibility, answer length, explanation quality and French sense
   have been checked across the whole chapter;
6. `make check` passes and the result has been inspected in Anki.
