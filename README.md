# WSET 3 VIN — Anki deck

Collaborative, version-controlled Anki deck for the **WSET Level 3 Award in Wines**.

Source of truth is YAML on GitHub. A small Python toolchain builds `.apkg` files you can import with **File → Import**. No Anki add-on required to contribute.

**This project is not affiliated with, endorsed by, or connected to the Wine & Spirit Education Trust (WSET).** WSET is a registered trademark of the Wine & Spirit Education Trust. Cards are independently authored. Do not copy official textbooks, workbooks, or exam papers.

Deck évolutif et traduisible (EN / FR) pour le WSET 3 VIN. Les cartes vivent en YAML ; le build produit des paquets Anki.

## Study with the deck

1. Download the latest `.apkg` from [GitHub Releases](https://github.com/) (or build it locally).
2. In Anki: **File → Import** and choose one of:
   - `wset3-vin-en.apkg` — English only
   - `wset3-vin-fr.apkg` — French only
   - `wset3-vin-bilingual.apkg` — one note, two card types (`EN` / `FR`)
3. To update later, import the new package. Note GUIDs are stable, so Anki **updates** existing cards instead of duplicating them or resetting scheduling.

Draft cards are excluded from release builds. Cards without a `fr:` block are omitted from the French package.

## Build locally

Requires [uv](https://docs.astral.sh/uv/) and Python 3.12+.

```bash
uv sync --extra dev
make check
uv run wset3-anki build --lang all --out dist/
```

`make check` is the quality gate (Ruff + types + YAML schema + tests), the Python equivalent of ESLint + TypeScript + Prettier.

| Command | Result |
| --- | --- |
| `wset3-anki build --lang en` | `dist/wset3-vin-en.apkg` |
| `wset3-anki build --lang fr` | `dist/wset3-vin-fr.apkg` |
| `wset3-anki build --lang bilingual` | `dist/wset3-vin-bilingual.apkg` |
| `wset3-anki build --lang all` | all three |
| `wset3-anki build --include-drafts` | also emit `status: draft` cards |

Anki deck tree: `WSET 3 VIN::{Chapter}::{optional sub}` (for example `WSET 3 VIN::France::Bordeaux`). In the bilingual package, suspend the `EN` or `FR` card type if you only want one language.

## Repository layout

```
cards/                 YAML source (one file per chapter)
schema/                JSON Schema for editor + CI (generated)
templates/mcq/         QCM front/back HTML + CSS
templates/ui/          UI strings (Pourquoi / Why, …)
src/wset3_anki/        validate + build CLI
tests/
```

## Tooling (JS → this repo)

| JavaScript | Here |
| --- | --- |
| TypeScript / `tsc` | Pydantic + JSON Schema on YAML; basedpyright on Python |
| ESLint | `ruff check` |
| Prettier | `ruff format` |
| `npm test` | `pytest` |
| `npm run lint` | `make check` / `uv run wset3-anki check` |

While you edit `cards/*.yaml`, Cursor/VS Code validates against `schema/cards.schema.json` (Red Hat YAML extension). After changing the Python schema, run `uv run wset3-anki schema` and commit the updated JSON Schema.

See [CONTRIBUTING.md](CONTRIBUTING.md) and [CONTENT_GUIDELINES.md](CONTENT_GUIDELINES.md) before adding cards.

Agents: start with [AGENTS.md](AGENTS.md). Cursor also loads [`.cursor/rules/`](.cursor/rules/).

## License

- **Code** (`src/`, `templates/`, CI): [MIT](LICENSE)
- **Card content** (`cards/`): [CC BY-SA 4.0](LICENSE-CONTENT)
