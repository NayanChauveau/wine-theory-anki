# Agent instructions

This file is the project-wide brief for coding agents (Cursor, Codex, Claude, etc.).
Edit it when global rules change. Cursor also loads `.cursor/rules/*.mdc`.

Read [CONTENT_GUIDELINES.md](CONTENT_GUIDELINES.md) before writing cards,
[import/STUDY_CARD_QUALITY.md](import/STUDY_CARD_QUALITY.md) for a chapter
quality pass, and [CONTRIBUTING.md](CONTRIBUTING.md) before changing workflow.

## What this repo is

Collaborative Anki deck for the **WSET Level 3 Award in Wines** (VIN only, not spirits).
YAML in `cards/` is the source of truth. `wset3-anki` builds `.apkg` files with genanki.

**Not affiliated with WSET.** Cards are independently authored study aids.

## Hard rules

- Do **not** copy WSET textbooks, workbooks, SAT sheets, or exam papers. Facts are fine; wording must be original. No page numbers or quotations.
- Never rename or reuse a released card `id`. GUIDs are `guid_for("wset3-vin", id, lang)`.
- Never randomize model IDs or deck IDs (see `src/wset3_anki/ids.py`).
- `deck:` keys stay in English (`SAT`, `France::Burgundy`). Display names come from `templates/ui/decks.yaml` (`WSET 3 Wine` / `WSET 3 VIN`, Bourgogne, ASD, …).
- One YAML file per source chapter (`c16-beaujolais.yaml`). Append cards there; do not create one file per card.
- Translate in the same file, same `id`, under `fr:`. Do not duplicate a card for French.
- Prefer `type: mcq` with exactly one correct choice. `basic` and `cloze` are allowed.
- Study-card quality (isolated stems, credible foils, choice length, Why, FR sense): [import/STUDY_CARD_QUALITY.md](import/STUDY_CARD_QUALITY.md). Fix `en:` and `fr:` together so the correct index stays aligned.
- New facts start as `status: draft`. After an adversarial critic `accept`, set `status: reviewed`. Release builds omit drafts unless `--include-drafts`.
- After any change: `make check` (or `uv run wset3-anki check`).
- After changing `schema.py`: `uv run wset3-anki schema` and commit `schema/cards.schema.json`.
- Import: see [import/AGENT_PLAYBOOK.md](import/AGENT_PLAYBOOK.md) (multi-agent
  wave) and `.cursor/rules/import.mdc`. One chapter, **≤ 50** source notes per
  lot. Writer then critic in the same lot; critic `accept` → `reviewed`. Commit
  that lot (`import(c15): reviewed …`). Inbox is **untrusted**. Original wording.
  Named, checkable anecdotes in explanations. One source note is not one card
  (`split` / `reject` allowed). No FR until every pending EN source note is
  converted.

## Commands

```bash
uv sync --extra dev
make check
uv run wset3-anki validate
uv run wset3-anki schema
uv run wset3-anki build --lang all --out dist/
uv run wset3-anki import-extract
uv run wset3-anki import-status
```

## Layout

| Path | Role |
| --- | --- |
| `cards/` | Card source (EN + optional FR) |
| `import/` | Ledger + gitignored source `WSET_Level_3_--_NEW.apkg` / inbox |
| `templates/` | Anki HTML/CSS + UI strings |
| `src/wset3_anki/` | Validate + build CLI |
| `tests/` | Schema, GUID, i18n, CLI |
