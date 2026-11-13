# Project roadmap

This page is the human-readable checklist for completing Wine Theory Anki. It complements
the two machine-readable editorial ledgers:

- [`import/progress.yaml`](import/progress.yaml) tracks migration of the private legacy
  source notes into original English cards.
- [`import/quality-review.yaml`](import/quality-review.yaml) tracks the chapter-wide card
  quality pass: isolation, credible distractors, balanced choice length, useful
  explanations and natural French.

The figures below are a snapshot from **2026-11-13**. Source notes and finished cards are
different units: one source note may be split into several cards, merged with another note
or rejected.

## Current snapshot

| Measure | Complete | Remaining | Progress |
| --- | ---: | ---: | ---: |
| Legacy source notes resolved | 3,636 / 4,075 | 439 | 89.2% |
| Cards with French | 3,303 / 3,306 | 3 | 99.9% |
| Release-eligible cards with French | 3,303 / 3,303 | 0 | 100% |
| Draft cards | — | 3 | — |
| Chapters with agent review complete | 41 | — | — |

To obtain the live migration count, run:

```bash
uv run wset3-anki import-status
```

All translated MCQs have matching English and French choice counts and correct answer
indexes. Every chapter that has been started is fully migrated, reviewed and bilingual;
the 41 completed chapter passes are recorded as `awaiting-human` in the quality ledger.

Since 2026-11-13, writers and critics verify fragile facts (dates, figures, rankings,
legal rules, named anecdotes) against authoritative external sources and record them in
`review.sources`; see "External fact-checking" in
[`import/AGENT_PLAYBOOK.md`](import/AGENT_PLAYBOOK.md). Chapters completed before that
rule (c07, c08, c09, c33, c38, c39, c43) received a dedicated sourced re-check.

Packages are built and published by CI (`.github/workflows/ci.yml`) on every push to
`main`; there is no manual build step.

## Immediate priorities

### 1. Migrate the remaining untouched chapters

| Chapter | Pending source notes |
| --- | ---: |
| Argentina | 105 |
| New Zealand | 90 |
| Canada | 34 |
| Fortified Muscat | 25 |
| Unclassified — triage into chapters or reject | 185 |
| **Total** | **439** |

For each chapter:

- [ ] Convert source notes into original English cards in lots of at most 50 notes,
  checking fragile facts against external sources.
- [ ] Have each lot critically reviewed (lower lot wins on cross-lot duplicates) before
  changing cards to `reviewed`.
- [ ] Resolve the source ledger to zero pending notes.
- [ ] Translate into natural wine French and recheck both languages together.
- [ ] Record the bilingual chapter pass in `import/quality-review.yaml`.

Unclassified notes should be triaged last: many will duplicate facts already carded in
their proper chapter and can be rejected or merged.

### 2. Resolve the remaining drafts

- [ ] `wine-natural-001` and `wine-barrique-two-years-001` (Winemaking and Maturation).
- [ ] `vm-canopy-trellis-choice-001` (Vineyard Management).

Each needs stronger distractors and a French block, or a deliberate rejection.

### 3. Human sign-off

- [ ] Perform human sign-off, or a documented human sampling pass, on the 41 chapters
  marked `awaiting-human`.

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
- New World: USA Introduction, California, Pacific Northwest, Chile, South Africa,
  Australia.
- Sparkling and fortified: Sparkling Production, Sparkling Wines, Sherry, Port.

## Quality and release checklist

- [ ] Resolve the three remaining draft cards or deliberately reject them.
- [x] Complete agent quality review for every started chapter.
- [ ] Complete agent quality review for the five remaining chapters.
- [ ] Perform human sign-off or a documented human sampling pass on chapters marked
  `awaiting-human`.
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
