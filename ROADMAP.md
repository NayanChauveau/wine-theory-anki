# Project roadmap

This page is the human-readable checklist for completing Wine Theory Anki. It complements
the two machine-readable editorial ledgers:

- [`import/progress.yaml`](import/progress.yaml) tracks migration of the private legacy
  source notes into original English cards.
- [`import/quality-review.yaml`](import/quality-review.yaml) tracks the chapter-wide card
  quality pass: isolation, credible distractors, balanced choice length, useful
  explanations and natural French.

The figures below are a snapshot from **2026-10-12**. Source notes and finished cards are
different units: one source note may be split into several cards, merged with another note
or rejected.

## Current snapshot

| Measure | Complete | Remaining | Progress |
| --- | ---: | ---: | ---: |
| Legacy source notes resolved | 2,236 / 4,075 | 1,839 | 54.9% |
| Cards with French | 2,011 / 2,364 | 353 | 85.1% |
| Release-eligible cards with French | 2,011 / 2,359 | 348 | 85.2% |
| Draft cards | — | 5 | — |

To obtain the live migration count, run:

```bash
uv run wset3-anki import-status
```

All translated MCQs currently have matching English and French choice counts and correct
answer indexes. Twenty-nine completed chapter passes are recorded as `awaiting-human` in
the quality ledger; agent review is complete for those chapters, but human sign-off remains
open.

## Immediate priorities

### 1. Spain — editorial pass complete

- [x] Resolve all 237 legacy source notes.
- [x] Complete the English factual and study-card quality pass on 228 cards.
- [x] Translate and check the first 80 cards.
- [x] Translate and check the remaining 148 cards.
- [x] Record the completed chapter pass in `import/quality-review.yaml`.
- [ ] Build and inspect the complete Spanish section in Anki.

### 2. Audit and translate Portugal

- [x] Resolve all 63 legacy source notes.
- [x] Run a full factual and adversarial study-card quality pass on the 78 English cards.
- [x] Translate only after the English pass is complete.
- [x] Record the bilingual chapter pass in `import/quality-review.yaml`.
- [ ] Build and inspect the complete Portuguese section in Anki.

### 3. SAT, Growing Environment, Price of Wine and Wine and the Law — editorial passes complete

- [x] Resolve the available English source notes.
- [x] Run a full factual and adversarial quality pass on all 6 SAT cards.
- [x] Run a full factual and adversarial quality pass on all 31 Growing Environment cards.
- [x] Rewrite and quality-check all 44 Price of Wine cards.
- [x] Rewrite, fact-check and quality-check all 46 Wine and the Law cards in lots of ten.
- [x] Complete and align the French translations in all four chapters.
- [x] Record all four chapter passes in `import/quality-review.yaml`.
- [ ] Build and inspect all four sections in Anki.

### 4. Translate other chapters whose English source migration is already complete

These chapters can be translated now without getting ahead of pending English source
notes.

| Chapter | Missing French cards |
| --- | ---: |
| Pacific Northwest | 50 |
| **Subtotal** | **50** |

- [x] Fact-check, rewrite and translate all 6 USA Introduction cards.
- [x] Record the USA Introduction pass in `import/quality-review.yaml`.
- [ ] Translate Pacific Northwest in its existing YAML file.
- [ ] Recheck English and French together for sense, difficulty and answer alignment.
- [ ] Add or complete the Pacific Northwest entry in `import/quality-review.yaml`.

### 5. Finish partially migrated English chapters before translating them

Project rules require all pending English source notes in a chapter to be resolved before
starting or completing its French pass.

| Chapter | Pending source notes | Current cards missing French |
| --- | ---: | ---: |
| The Vine | 52 | 61 |
| Vineyard Management | 135 | 64 |
| Winemaking and Maturation | 173 | 64 |
| California | 62 | 114 |
| **Subtotal** | **422** | **303** |

- [ ] Convert the remaining English source notes in reviewed lots.
- [ ] Run an adversarial chapter-wide English quality pass.
- [ ] Translate only after the chapter reaches zero pending source notes.
- [ ] Complete the bilingual quality ledger entry.

### 6. Migrate untouched legacy-source chapters

| Chapter | Pending source notes |
| --- | ---: |
| Unclassified — triage into chapters or reject | 185 |
| White and Sweet Winemaking | 162 |
| Red and Rosé Winemaking | 148 |
| Canada | 34 |
| Chile | 119 |
| Argentina | 105 |
| South Africa | 128 |
| Australia | 179 |
| New Zealand | 90 |
| Sherry | 136 |
| Port | 106 |
| Fortified Muscat | 25 |
| **Subtotal** | **1,417** |

For each chapter:

- [ ] Convert source notes into original English cards in lots of at most 50 notes.
- [ ] Have each lot critically reviewed before changing cards to `reviewed`.
- [ ] Resolve the source ledger to zero pending notes.
- [ ] Perform the full chapter-wide quality pass.
- [ ] Translate into natural wine French and recheck both languages together.

## Quality and release checklist

- [ ] Resolve the five remaining draft cards or deliberately reject them.
- [ ] Complete agent quality review for every chapter.
- [ ] Perform human sign-off or a documented human sampling pass on chapters marked
  `awaiting-human`.
- [ ] Run `make check` after every change.
- [ ] Build both packages and inspect representative MCQ, basic and cloze cards on desktop
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
