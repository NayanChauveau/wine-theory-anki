# Wine Theory Anki

An open, version-controlled and bilingual **Anki deck for advanced wine study**, built
around the knowledge expected for the WSET Level 3 Award in Wines.

**Install and keep this deck up to date with [Deck Manager](https://github.com/NayanChauveau/anki-deck-manager).**
Choose an English or French edition, add it once, and receive update offers inside
Anki. You do not need Python or development tools to study.

**[Get Deck Manager on AnkiWeb](https://ankiweb.net/shared/info/932198090)** ·
**[Browse deck releases](https://github.com/NayanChauveau/wine-theory-anki/releases/latest)**

> **Projet francophone ?** Le paquet français, les noms de paquets et l’interface des
> cartes sont localisés. Le code et la documentation du dépôt restent principalement en
> anglais pour faciliter les contributions internationales.

> [!IMPORTANT]
> This is an independent study aid. It is **not affiliated with, endorsed by, or connected
> to the Wine & Spirit Education Trust (WSET)**. WSET is a registered trademark of the
> Wine & Spirit Education Trust. No official textbooks, workbooks or exam questions are
> reproduced here.

## What the project provides

- English and French Anki packages generated from the same card IDs.
- MCQ, basic and cloze cards with localized deck names and interfaces.
- Shuffled MCQ choices on every review.
- Stable note identifiers, so importing a newer release updates existing notes without
  creating duplicates or resetting their scheduling.
- Schema validation, tests and automated release builds.
- A review workflow for factual accuracy, credible distractors and natural French.

The project is a work in progress. English coverage is currently broader than French
coverage. Draft cards are excluded from normal builds, and cards without a `fr:` block
are omitted from the French package.

See the [project roadmap and completion checklist](ROADMAP.md) for the current migration,
translation and quality-review status.

## Install with Deck Manager — recommended

Requires **Anki Desktop 26.09 or later**.

1. Open [Deck Manager on AnkiWeb](https://ankiweb.net/shared/info/932198090)
   and copy the add-on code: **`932198090`**.
2. In Anki, choose **Tools → Add-ons → Get Add-ons**, paste the code, confirm,
   then restart Anki. Open **Tools → Deck Manager**.
3. Open the [latest deck release](https://github.com/NayanChauveau/wine-theory-anki/releases/latest).
   Under **Assets**, copy the link address of your preferred package:

   | Edition | File to follow |
   | --- | --- |
   | English | `wset3-vin-en.apkg` |
   | Français | `wset3-vin-fr.apkg` |

4. Paste that file link into Deck Manager and confirm Anki’s import dialog.

Use a **versioned asset link** containing `/releases/download/vX.Y.Z/` and the
filename. The release page URL and `releases/latest` links are not accepted by
Deck Manager. No GitHub account or token is needed.

Both editions can coexist in the same collection as separate notes and deck trees.
After importing on your computer, sync Anki to study on your other devices.

### Updates without watching GitHub

Deck Manager checks for new versions at startup, at most once every 24 hours.
Choose **Import update** or **Later** when prompted, or use **Check** in Deck Manager
at any time. An update downloads the package and opens Anki’s usual import dialog;
you remain in control of the import settings.

Stable note identities allow Anki to update existing notes. Your import settings
determine how those updates are applied. Cards removed from a package are not
automatically deleted from your collection.

### Manual installation

If you prefer, download the `.apkg` for your language from the
[latest release](https://github.com/NayanChauveau/wine-theory-anki/releases/latest)
and use **File → Import** in Anki. Check for new releases and repeat the import
when you want to update; Deck Manager handles that checking for you.

## Contribute and build locally

For corrections, translations and new cards, read [CONTRIBUTING.md](CONTRIBUTING.md).
The sections below are for contributors; the installation above is enough to study.

## Build from source

### Requirements

- [Python 3.12 or later](https://www.python.org/downloads/)
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- `make` for the short commands below; every command also has a direct `uv` equivalent

From the repository root:

```bash
uv sync --extra dev
make check
make build
```

The generated packages are written to `dist/`:

```text
dist/wset3-vin-en.apkg
dist/wset3-vin-fr.apkg
```

To build only one language:

```bash
uv run wset3-anki build --lang en --out dist
uv run wset3-anki build --lang fr --out dist
```

Normal builds skip `status: draft` cards. For local editorial previews only, you can add
`--include-drafts`.

### Useful commands

| Command | Purpose |
| --- | --- |
| `make check` | Run linting, formatting checks, type checks, schema validation and tests |
| `make build` | Build both English and French `.apkg` packages |
| `make push` | Build French, import it into Anki Desktop and sync AnkiWeb |
| `make push ANKI_LANG=en` | Build, import and sync the English package |
| `make push ANKI_LANG=all` | Build, import and sync both language packages |
| `uv run wset3-anki validate` | Validate only the card YAML files |
| `uv run wset3-anki schema` | Regenerate `schema/cards.schema.json` after a schema change |

If `make` is unavailable, use the equivalent commands directly:

```bash
uv run wset3-anki check
uv run wset3-anki build --lang all --out dist
uv run wset3-anki push --lang fr --out dist
```

## Build, import and sync with AnkiConnect

[`make push`](#useful-commands) provides the shortest local publishing workflow. It
builds the selected package, starts Anki Desktop when possible, imports the `.apkg`, and
asks Anki to synchronize the active profile with AnkiWeb.

### One-time setup

1. Install [Anki Desktop](https://apps.ankiweb.net/) and connect the intended profile to
   your AnkiWeb account.
2. In Anki, open **Tools → Add-ons → Get Add-ons**.
3. Enter the AnkiConnect add-on code **`2055492159`**. See the
   [AnkiWeb add-on page](https://ankiweb.net/shared/info/2055492159) or the
   [AnkiConnect repository](https://github.com/FooSoft/anki-connect) for details.
4. Restart Anki Desktop once so the add-on is loaded.

You can then publish the French package with:

```bash
make push
```

Or select another language:

```bash
make push ANKI_LANG=en
make push ANKI_LANG=all
```

The command prints the number of imported notes and confirms the AnkiWeb sync when it
finishes.

> [!WARNING]
> The final sync concerns the **entire active Anki profile**, not only this deck. Before
> running `make push`, make sure Anki Desktop is using the intended profile and AnkiWeb
> account. Resolve any pending one-way sync prompt in Anki itself first.

By default the tool contacts AnkiConnect only on `http://127.0.0.1:8765`. Do not expose
an unauthenticated AnkiConnect endpoint to the public internet. Advanced installations
can set a custom endpoint or API key:

```bash
ANKI_CONNECT_URL=http://127.0.0.1:8765 \
ANKI_CONNECT_KEY=your-key \
make push
```

To require Anki to be opened manually instead of allowing the command to launch it:

```bash
uv run wset3-anki push --lang fr --out dist --no-launch
```

### AnkiConnect troubleshooting

- **Cannot reach AnkiConnect:** confirm that add-on `2055492159` is installed, restart
  Anki, and leave Anki Desktop open while retrying.
- **Anki cannot be launched automatically:** open it manually and run the command again,
  or use `--no-launch`.
- **Synchronization fails:** check that the active Anki profile is connected to AnkiWeb
  and complete any sync or conflict prompt directly in Anki.
- **Custom AnkiConnect configuration:** set `ANKI_CONNECT_URL` and, if configured in the
  add-on, `ANKI_CONNECT_KEY`.

## Contributing

Contributions are welcome: factual corrections, better distractors, clearer explanations,
French translations, new cards, templates, tests and tooling all help.

If you have found a problem but do not want to edit YAML, use the structured
[issue templates](../../issues/new/choose) to report a card or a build problem.

Before editing cards, read:

- [CONTRIBUTING.md](CONTRIBUTING.md) for the development and pull-request workflow;
- [CONTENT_GUIDELINES.md](CONTENT_GUIDELINES.md) for authorship and card-writing rules;
- [import/STUDY_CARD_QUALITY.md](import/STUDY_CARD_QUALITY.md) for the chapter review rubric.

The short version is:

1. Fork the repository and create a focused branch.
2. Edit the existing chapter file in `cards/`; do not create one file per card.
3. Use original wording and public, checkable sources. Never copy WSET course materials
   or exam questions.
4. Give new facts `status: draft`. Never rename or reuse a released card `id`.
5. If a card is bilingual, keep the same choice count and correct-choice index in `en:`
   and `fr:`.
6. Run `make check`.
7. Open a focused pull request explaining what changed, why, and which sources support
   factual corrections.

Small corrections can go directly to a pull request. For a large new chapter, a schema
change or a substantial workflow change, open an issue first so the approach can be
agreed before a large amount of work is written.

You do **not** need Anki or AnkiConnect to contribute card content. They are only needed
to preview or automatically import a built package.

## Repository layout

```text
cards/                  YAML source of truth, one file per source chapter
import/                 Migration ledger and editorial quality-review material
schema/                 Generated JSON Schema for card YAML
templates/              Anki HTML, CSS, JavaScript and localized UI/deck names
src/wset3_anki/         Validator, builder and AnkiConnect integration
tests/                  Unit and integration tests
.github/                CI, release workflow and pull-request template
dist/                   Locally generated packages; not source
```

The stable `deck:` values in YAML remain in English, for example
`France::Burgundy`. Display names are localized at build time, producing paths such as
`WSET 3 Wine::France::Burgundy` and `WSET 3 VIN::France::Bourgogne`.

Editors with YAML language-server support can use `schema/cards.schema.json` for inline
validation. If `src/wset3_anki/schema.py` changes, regenerate and commit the schema:

```bash
uv run wset3-anki schema
```

## Releases

Each successful push to `main` passes the quality gate, builds both language packages
and publishes the next stable patch release (`vX.Y.Z`). Pull requests run checks and
build packages without publishing. This matches the current CI workflow.

The filenames stay `wset3-vin-en.apkg` and `wset3-vin-fr.apkg`, so Deck Manager can
follow each edition independently. Publish a new version for new content;
replacing a file under an existing version does not trigger an update offer.
Released card, model and deck IDs remain permanent.

## License and attribution

- Code in `src/`, `templates/`, tests and automation is licensed under the
  [MIT License](LICENSE).
- Card content in `cards/` is licensed under
  [CC BY-SA 4.0](LICENSE-CONTENT).

If you redistribute or adapt the cards, provide appropriate attribution and distribute
your card-content changes under the same CC BY-SA 4.0 license.

WSET is a registered trademark of the Wine & Spirit Education Trust. This independent
project is not affiliated with, endorsed by, or connected to WSET.
