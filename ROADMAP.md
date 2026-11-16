# Project roadmap

This page is the human-readable checklist for completing Wine Theory Anki. It complements
the two machine-readable editorial ledgers:

- [`import/progress.yaml`](import/progress.yaml) tracks migration of the private legacy
  source notes into original English cards.
- [`import/quality-review.yaml`](import/quality-review.yaml) tracks the chapter-wide card
  quality pass: isolation, credible distractors, balanced choice length, useful
  explanations and natural French.

The figures below are a snapshot from **2026-11-16**. Source notes and finished cards are
different units: one source note may be split into several cards, merged with another note
or rejected.

## Current snapshot

| Measure | Complete | Remaining | Progress |
| --- | ---: | ---: | ---: |
| Legacy source notes resolved | 4,075 / 4,075 | 0 | 100% |
| Cards with French | 3,539 / 3,539 | 0 | 100% |
| Draft cards | — | 0 | — |
| Chapters with agent review complete | 46 | — | — |
| Cards covered by the final Fable audit | 3,539 / 3,539 | 0 | 100% |

To obtain the live migration count, run:

```bash
uv run wset3-anki import-status
```

All translated MCQs have matching English and French choice counts and correct answer
indexes. Every chapter is fully migrated, reviewed and bilingual. The 185 unclassified
legacy notes were triaged on 2026-11-15/16: 147 duplicated existing cards, 16 were
rejected and 22 became new cards (including the first card of Wine with Food).

Since 2026-11-13, writers and critics verify fragile facts (dates, figures, rankings,
legal rules, named anecdotes) against authoritative external sources and record them in
`review.sources`; see "External fact-checking" in
[`import/AGENT_PLAYBOOK.md`](import/AGENT_PLAYBOOK.md).

Packages are built and published by CI (`.github/workflows/ci.yml`) on every push to
`main`; there is no manual build step.

## Final audit (2026-11-15/16)

An independent final audit by Claude Fable read every card in English and French for
factual accuracy, distractor quality and French sense, and fixed problems in place.
Reports are in [`import/audit/2026-11-15/`](import/audit/2026-11-15/), and each chapter of
the quality ledger carries `final_audit: 2026-11-15`.

- About 17 cards had a wrong key or a foil that was actually correct, and were fixed.
  Examples: Entre-Deux-Mers rouge (2023) and Médoc blanc (2025), Rueda's 75%
  principal-variety rule (2024), Champagne's 42 premier cru villages, the Cava zone now
  named Requena, and the Beaujolais Nouveau bottling deadline.
- About 280 cards received a quality fix: joke or half-true distractors, cue words
  ("only", "always"), self-answering stems, and English/French drift. The early regional
  chapters (Bordeaux, Loire) needed the most work.
- The audit replaces the manual human pass; `human: ok` stays reserved for the maintainer.

## Follow-ups worth checking

- [ ] Tokaj: the specification was amended again in 2026 (EU 2026/1556). Release dates and
  puttonyos optionality should be checked against the full text.
- [ ] Saumur sparkling 60% Chenin / Cabernet Franc minimums and the Champagne Brut "more
  than 90%" share could not be confirmed on an official page.
- [ ] Vin Jaune ageing (about 6 years 3 months, 60 months under veil) rests on secondary
  sources.
- [ ] Minor cleanups noted by auditors: `vm-site-utilities-001` and
  `vm-site-land-labour-001` leak each other's keys; a few older Whys in c08/c09 mention
  New Zealand keys (Waipara Riesling, Gimblett Gravels).

## Completed chapters

All chapters below have zero pending source notes, reviewed English cards, aligned
French, an `awaiting-human` entry in the quality ledger and a final Fable audit.

- Foundations: SAT, Wine with Food, The Vine, Growing Environment, Vineyard Management,
  Winemaking and Maturation, White and Sweet Winemaking, Red and Rosé Winemaking, Price of
  Wine, Wine and the Law.
- France: Introduction, Bordeaux, South West, Burgundy, Beaujolais, Alsace, Loire,
  Northern Rhône, Southern Rhône, Southern France, Jura, Savoie.
- Rest of Europe: Germany, Austria, Tokaj, Greece, Italy (Introduction, Northern,
  Central, Southern), Spain, Portugal.
- New World: USA Introduction, California, Pacific Northwest, Canada, Chile, Argentina,
  South Africa, Australia, New Zealand.
- Sparkling and fortified: Sparkling Production, Sparkling Wines, Sherry, Port,
  Fortified Muscat.

## Quality and release checklist

- [x] Migrate every legacy source note, including the unclassified ones.
- [x] Resolve all draft cards.
- [x] Complete agent quality review for every chapter.
- [x] Run the final Fable audit on every chapter.
- [ ] Run `make check` after every change.
- [ ] Inspect representative MCQ, basic and cloze cards from the CI packages on desktop
  and mobile.
- [ ] Keep the rolling GitHub release healthy after pushes to `main`.
- [ ] Create a versioned release when the follow-ups above are settled.

## Definition of done for a chapter

A chapter is complete when:

1. its source ledger has no pending or in-progress notes;
2. every retained fact is represented by an original, reviewed English card;
3. every released English card has a natural French block where translation is in scope;
4. English and French MCQs have the same choice count and correct-answer index;
5. isolation, distractor credibility, answer length, explanation quality and French sense
   have been checked across the whole chapter;
6. `make check` passes and the result has been inspected in Anki.
