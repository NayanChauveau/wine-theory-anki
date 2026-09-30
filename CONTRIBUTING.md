# Contributing to Terroir Recall

Thank you for helping improve this open, bilingual wine-study deck. Contributions can
be as small as a typo fix or as substantial as a reviewed chapter, but each pull request
should remain easy to understand and verify.

You do not need Anki or AnkiConnect to edit cards. They are only required if you want to
preview a generated package or test the automatic import workflow.

## Ways to contribute

- Correct a factual error using public, checkable sources.
- Replace an implausible or giveaway distractor.
- Clarify an ambiguous question or strengthen its explanation.
- Translate cards into natural wine French.
- Add missing WSET Level 3 knowledge in original wording.
- Improve card templates, accessibility, tests or build tooling.
- Report a problem when you are not ready to write the fix yourself.

Small, focused fixes can go directly to a pull request. Please open an issue before
starting a new chapter, changing the YAML schema, redesigning the Anki models, or making
another change that would affect many contributors or existing users.

## Development setup

Requirements:

- Python 3.12 or later
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- `make` for convenience; direct `uv run` commands work on systems without it

From the repository root:

```bash
uv sync --extra dev
make check
```

`make check` is the required quality gate. It runs Ruff, formatting checks,
basedpyright, JSON Schema consistency, card validation and pytest.

| Command | What it does |
| --- | --- |
| `make check` | Run the complete quality gate |
| `make format` | Apply Python formatting and safe Ruff fixes |
| `make build` | Build both language packages in `dist/` |
| `uv run wset3-anki validate` | Validate card YAML only |
| `uv run wset3-anki schema` | Regenerate the committed JSON Schema |
| `uv run wset3-anki build --lang all --out dist` | Build English and French packages |
| `make push` | Build French, import through AnkiConnect and sync AnkiWeb |

## Recommended Git workflow

1. Fork the repository.
2. Create a branch with a focused name, such as `cards/fix-cahors-terroirs` or
   `translation/italy-introduction`.
3. Make one coherent change or work on one chapter.
4. Run `make check`.
5. Review your diff for accidental card-ID, language or correct-answer changes.
6. Open a pull request using the repository template.

Keeping card PRs to one chapter makes factual and linguistic review much easier. A tiny
cross-repository typo or tooling fix can naturally be handled in one PR.

## Edit or add a card

1. Find the chapter file in [`cards/`](cards/). Files contain many cards; do not create
   one YAML file per card.
2. Read [CONTENT_GUIDELINES.md](CONTENT_GUIDELINES.md) and, for a chapter-wide pass,
   [import/STUDY_CARD_QUALITY.md](import/STUDY_CARD_QUALITY.md).
3. Edit the English and French blocks together when changing a bilingual fact or choice.
4. Give every new fact `status: draft` until another reviewer has checked it.
5. Run `uv run wset3-anki validate`, then `make check` before opening the PR.

### Non-negotiable compatibility rules

- Never rename or reuse a released `id`. Anki update compatibility depends on it.
- Keep `deck:` keys in English, such as `France::Burgundy`; the build localizes display
  names.
- Keep a card in its existing chapter file.
- A bilingual MCQ must have the same number of choices and the same correct-choice index
  in `en:` and `fr:`.
- New or unverified facts start as `status: draft`.
- Do not hand-edit generated `.apkg` files or commit `dist/`.
- If `src/wset3_anki/schema.py` changes, run `uv run wset3-anki schema` and commit the
  resulting `schema/cards.schema.json`.

## Example MCQ

This is an illustrative example, not an ID to copy into a real chapter:

```yaml
- id: example-muscadet-grape-001
  type: mcq
  deck: France::Loire
  tags: [france, loire, muscadet]
  status: draft
  en:
    question: Which grape variety is used for Muscadet?
    choices:
      - { text: Melon, correct: true }
      - { text: Chenin Blanc, correct: false }
      - { text: Sauvignon Blanc, correct: false }
      - { text: Folle Blanche, correct: false }
    explanation: |
      Melon is naturally high in acidity and relatively neutral in aroma. This makes it
      well suited to the light, dry style of Muscadet and to maturation on lees.
  fr:
    question: Quel cépage est utilisé pour élaborer le Muscadet ?
    choices:
      - { text: Melon, correct: true }
      - { text: Chenin Blanc, correct: false }
      - { text: Sauvignon Blanc, correct: false }
      - { text: Folle Blanche, correct: false }
    explanation: |
      Le Melon possède naturellement une acidité élevée et un profil aromatique assez
      neutre. Il convient ainsi au style léger et sec du Muscadet et à l’élevage sur lie.
```

The explanation should teach something beyond merely repeating the keyed choice. Wrong
choices should belong to the same category and remain plausible to a candidate who only
partly remembers the chapter.

## Facts, sources and copyright

All card wording must be original.

- Facts such as grape varieties, climate patterns, production methods and appellation
  rules can be researched and restated.
- Do not copy sentences, tables, diagrams, tasting notes or questions from WSET books,
  workbooks, SAT materials, mock exams or past papers.
- Do not include textbook page numbers or quotations.
- Prefer primary public sources for contested or changing facts: official appellation
  specifications, government bodies, producer consortia or current regulations.
- Link the supporting sources in the pull-request description. The reviewer should be
  able to verify the correction without access to paid course materials.

This protects both the project and contributors while keeping factual review possible.

## Translation contributions

Add French under `fr:` on the existing card; never create a second card ID merely for a
translation.

The goal is natural, precise wine French, not word-for-word equivalence. Preserve the
meaning, difficulty and correct-choice index. A distractor that is credible in English
must remain credible in French. If an English factual change affects the translation,
update both in the same pull request.

If the English card is ready but no reliable French translation is available yet, use
`status: needs-translation` and omit `fr:`.

## Pull-request expectations

A useful pull request tells reviewers:

- which chapter and card IDs changed;
- whether the change is factual, editorial, linguistic or technical;
- why the change improves the deck;
- which public sources support factual additions or corrections;
- which checks were run locally.

Before submitting, confirm that:

- `make check` passes;
- new wording is original;
- new facts remain `draft` until reviewed;
- distractors are credible and similar in form and length;
- explanations answer the question and add useful reasoning;
- English and French choices remain aligned;
- no released card ID has been renamed.

CI repeats the full quality gate and builds both packages. A maintainer may ask for
factual, linguistic or card-design changes before marking new content as `reviewed`.

## Preview with Anki

To inspect the rendered cards locally:

```bash
uv run wset3-anki build --lang all --out dist
```

Import the resulting package manually with **File → Import**, or follow the AnkiConnect
instructions in the [README](README.md#build-import-and-sync-with-ankiconnect).

Using `--include-drafts` is appropriate for a local editorial preview, but draft cards
must remain excluded from public releases.

## Maintainer import workflow

The repository also contains a ledger for migrating an older private source package.
That source `.apkg` and the raw `import/inbox/` extraction are intentionally ignored and
must never be committed or redistributed.

Maintainers working on that migration should follow
[import/AGENT_PLAYBOOK.md](import/AGENT_PLAYBOOK.md). Useful commands are:

```bash
uv run wset3-anki import-extract
uv run wset3-anki import-status
```

This internal migration is not required for ordinary card or code contributions.

## Releases

Maintainers create a release by pushing a `vX.Y.Z` tag. GitHub Actions runs all checks,
builds `wset3-vin-en.apkg` and `wset3-vin-fr.apkg`, and attaches both files to the GitHub
release.

Stable note GUIDs are derived from the permanent card ID and language. That is why ID
compatibility is treated as a release contract rather than a cosmetic convention.
