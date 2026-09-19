# Contributing

Thanks for helping build an open, translatable WSET 3 VIN deck.

## Quick start

```bash
uv sync --extra dev
make check
```

That one command lints, formats, type-checks, validates every YAML card, and runs pytest. Optional: `uv run pre-commit install` to run the same gates on each commit.

| Command | What it does |
| --- | --- |
| `make check` | Full quality gate |
| `make format` | Auto-fix Python style |
| `uv run wset3-anki validate` | Cards only |
| `uv run wset3-anki schema` | Regenerate `schema/cards.schema.json` |
| `uv run wset3-anki import-extract` | Dump the source `.apkg` into `import/inbox/` |
| `uv run wset3-anki import-status` | Ledger: pending / done / rejected |

You do **not** need Anki installed to add or review cards.

## Add or edit a card

1. Open the YAML file for the chapter in [`cards/`](cards/). One file per source chapter (`c16-beaujolais.yaml`); do not create one file per card.
2. Append a note using the schema in [CONTENT_GUIDELINES.md](CONTENT_GUIDELINES.md).
3. Run `uv run wset3-anki validate`.
4. Optionally `uv run wset3-anki build --lang all --out dist/` and import an `.apkg` to preview.
5. Open a pull request with the template.

Example:

```yaml
- id: alsace-grand-cru-001
  type: mcq
  deck: France::Alsace
  tags: [france, alsace]
  status: draft
  en:
    question: ...
    choices:
      - { text: "...", correct: false }
      - { text: "Quote text if it has a comma", correct: true }
    explanation: |
      ...
  fr:
    question: ...
    choices:
      - { text: "...", correct: false }
      - { text: "Quote text if it has a comma", correct: true }
    explanation: |
      ...
```

## Translate

Edit the `fr:` block of an existing English card. Do not create a second id. If the English is finished but you cannot translate yet, set `status: needs-translation` and omit `fr:`.

## Pull requests

- Keep PRs to one chapter when you can.
- New facts should be `draft` until someone has double-checked them.
- CI must stay green: schema validation, tests, and a full `en` / `fr` / `bilingual` build.

## Releases

Tag `vX.Y.Z`. GitHub Actions attaches `wset3-vin-en.apkg`, `wset3-vin-fr.apkg`, and `wset3-vin-bilingual.apkg`. Importers keep their scheduling because note GUIDs are derived from `id` + language and never change.
