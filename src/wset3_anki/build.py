from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

import genanki

from wset3_anki.ids import (
    BASIC_MODEL_ID,
    BILINGUAL_BASIC_MODEL_ID,
    BILINGUAL_CLOZE_MODEL_ID,
    BILINGUAL_MCQ_MODEL_ID,
    CLOZE_MODEL_ID,
    MCQ_MODEL_ID,
    ROOT_DECK_NAME,
    ancestor_paths,
    deck_id_for,
    deck_path,
    note_guid,
)
from wset3_anki.render import (
    load_ui,
    read_template,
    render_choices_back,
    render_choices_front,
    render_markdown,
    wrap_explanation,
)
from wset3_anki.schema import BasicCard, Card, ClozeCard, McqCard, Status

Lang = Literal["en", "fr"]
BuildLang = Literal["en", "fr", "bilingual"]

PACKAGE_NAMES = {
    "en": "wset3-vin-en.apkg",
    "fr": "wset3-vin-fr.apkg",
    "bilingual": "wset3-vin-bilingual.apkg",
}

MONOLINGUAL_MODELS = {"mcq": "mcq", "basic": "basic", "cloze": "cloze"}
BILINGUAL_MODELS = {
    "mcq": "mcq-bilingual",
    "basic": "basic-bilingual",
    "cloze": "cloze-bilingual",
}


@dataclass
class PreparedNote:
    guid: str
    deck: str
    tags: list[str]
    model: str
    card: Card
    lang: Lang | None = None
    fields: list[str] = field(default_factory=list)


@dataclass
class BuildResult:
    notes: list[PreparedNote] = field(default_factory=list)
    skipped_drafts: int = 0
    skipped_untranslated: int = 0


def select_cards(cards: Iterable[Card], *, include_drafts: bool) -> tuple[list[Card], int]:
    selected: list[Card] = []
    skipped = 0
    for card in cards:
        if card.status is Status.DRAFT and not include_drafts:
            skipped += 1
            continue
        selected.append(card)
    return selected, skipped


def has_locale(card: Card, lang: Lang) -> bool:
    return getattr(card, lang) is not None


def card_tags(card: Card, extra: list[str] | None = None) -> list[str]:
    tags = ["wset3-vin", f"type::{card.type}", f"status::{card.status.value}", *card.tags]
    if extra:
        tags.extend(extra)
    return [tag.replace(" ", "-") for tag in tags]


def _mcq_fields(card: McqCard, lang: Lang, ui: dict[str, str]) -> list[str]:
    content = card.en if lang == "en" else card.fr
    assert content is not None
    return [
        render_markdown(content.question),
        render_choices_front(content.choices),
        render_choices_back(content.choices),
        wrap_explanation(render_markdown(content.explanation), ui["explanation"]),
    ]


def _basic_fields(card: BasicCard, lang: Lang) -> list[str]:
    content = card.en if lang == "en" else card.fr
    assert content is not None
    return [render_markdown(content.front), render_markdown(content.back)]


def _cloze_fields(card: ClozeCard, lang: Lang) -> list[str]:
    content = card.en if lang == "en" else card.fr
    assert content is not None
    extra = render_markdown(content.extra) if content.extra.strip() else ""
    return [content.text, extra]


def fill_fields(
    note: PreparedNote,
    *,
    ui_en: dict[str, str],
    ui_fr: dict[str, str],
    bilingual: bool,
) -> None:
    card = note.card
    if bilingual:
        if isinstance(card, McqCard):
            en = _mcq_fields(card, "en", ui_en)
            fr = _mcq_fields(card, "fr", ui_fr) if card.fr is not None else ["", "", "", ""]
            note.fields = [*en, *fr]
        elif isinstance(card, BasicCard):
            en = _basic_fields(card, "en")
            fr = _basic_fields(card, "fr") if card.fr is not None else ["", ""]
            note.fields = [*en, *fr]
        else:
            en = _cloze_fields(card, "en")
            fr = _cloze_fields(card, "fr") if card.fr is not None else ["", ""]
            note.fields = [*en, *fr]
        return

    assert note.lang is not None
    ui = ui_en if note.lang == "en" else ui_fr
    if isinstance(card, McqCard):
        note.fields = _mcq_fields(card, note.lang, ui)
    elif isinstance(card, BasicCard):
        note.fields = _basic_fields(card, note.lang)
    else:
        note.fields = _cloze_fields(card, note.lang)


def prepare_monolingual(
    cards: Iterable[Card],
    lang: Lang,
    *,
    include_drafts: bool = False,
) -> BuildResult:
    selected, skipped_drafts = select_cards(cards, include_drafts=include_drafts)
    result = BuildResult(skipped_drafts=skipped_drafts)
    for card in selected:
        if not has_locale(card, lang):
            result.skipped_untranslated += 1
            continue
        result.notes.append(
            PreparedNote(
                guid=note_guid(card.id, lang),
                deck=deck_path(card.deck),
                tags=card_tags(card, [f"lang::{lang}"]),
                model=MONOLINGUAL_MODELS[card.type],
                card=card,
                lang=lang,
            )
        )
    return result


def prepare_bilingual(cards: Iterable[Card], *, include_drafts: bool = False) -> BuildResult:
    selected, skipped_drafts = select_cards(cards, include_drafts=include_drafts)
    result = BuildResult(skipped_drafts=skipped_drafts)
    for card in selected:
        extra = ["lang::en"]
        if has_locale(card, "fr"):
            extra.append("lang::fr")
        else:
            extra.append("needs-translation")
        result.notes.append(
            PreparedNote(
                guid=note_guid(card.id, "bilingual"),
                deck=deck_path(card.deck),
                tags=card_tags(card, extra),
                model=BILINGUAL_MODELS[card.type],
                card=card,
            )
        )
    return result


def prepare(
    cards: Iterable[Card],
    lang: BuildLang,
    *,
    include_drafts: bool = False,
) -> BuildResult:
    if lang == "bilingual":
        return prepare_bilingual(cards, include_drafts=include_drafts)
    return prepare_monolingual(cards, lang, include_drafts=include_drafts)


def load_models(templates: Path) -> dict[str, genanki.Model]:
    mcq_css = read_template(templates, "mcq", "style.css")
    basic_css = read_template(templates, "basic", "style.css")
    cloze_css = read_template(templates, "cloze", "style.css")
    mcq_front = read_template(templates, "mcq", "front.html")
    mcq_back = read_template(templates, "mcq", "back.html")
    basic_front = read_template(templates, "basic", "front.html")
    basic_back = read_template(templates, "basic", "back.html")
    cloze_front = read_template(templates, "cloze", "front.html")
    cloze_back = read_template(templates, "cloze", "back.html")

    return {
        "mcq": genanki.Model(
            MCQ_MODEL_ID,
            "WSET 3 VIN MCQ",
            fields=[
                {"name": "Question"},
                {"name": "ChoicesFront"},
                {"name": "ChoicesBack"},
                {"name": "Explanation"},
            ],
            templates=[{"name": "MCQ", "qfmt": mcq_front, "afmt": mcq_back}],
            css=mcq_css,
        ),
        "basic": genanki.Model(
            BASIC_MODEL_ID,
            "WSET 3 VIN Basic",
            fields=[{"name": "Front"}, {"name": "Back"}],
            templates=[{"name": "Basic", "qfmt": basic_front, "afmt": basic_back}],
            css=basic_css,
        ),
        "cloze": genanki.Model(
            CLOZE_MODEL_ID,
            "WSET 3 VIN Cloze",
            fields=[{"name": "Text"}, {"name": "Extra"}],
            templates=[{"name": "Cloze", "qfmt": cloze_front, "afmt": cloze_back}],
            css=cloze_css,
            model_type=genanki.Model.CLOZE,
        ),
        "mcq-bilingual": genanki.Model(
            BILINGUAL_MCQ_MODEL_ID,
            "WSET 3 VIN MCQ Bilingual",
            fields=[
                {"name": "Question_EN"},
                {"name": "ChoicesFront_EN"},
                {"name": "ChoicesBack_EN"},
                {"name": "Explanation_EN"},
                {"name": "Question_FR"},
                {"name": "ChoicesFront_FR"},
                {"name": "ChoicesBack_FR"},
                {"name": "Explanation_FR"},
            ],
            templates=[
                {
                    "name": "EN",
                    "qfmt": _localize_mcq_front(mcq_front, "EN"),
                    "afmt": _localize_mcq_back(mcq_back, "EN"),
                },
                {
                    "name": "FR",
                    "qfmt": _localize_mcq_front(mcq_front, "FR"),
                    "afmt": _localize_mcq_back(mcq_back, "FR"),
                },
            ],
            css=mcq_css,
        ),
        "basic-bilingual": genanki.Model(
            BILINGUAL_BASIC_MODEL_ID,
            "WSET 3 VIN Basic Bilingual",
            fields=[
                {"name": "Front_EN"},
                {"name": "Back_EN"},
                {"name": "Front_FR"},
                {"name": "Back_FR"},
            ],
            templates=[
                {
                    "name": "EN",
                    "qfmt": "{{#Front_EN}}{{Front_EN}}{{/Front_EN}}",
                    "afmt": "{{FrontSide}}\n\n<hr id=answer>\n\n{{Back_EN}}",
                },
                {
                    "name": "FR",
                    "qfmt": "{{#Front_FR}}{{Front_FR}}{{/Front_FR}}",
                    "afmt": "{{FrontSide}}\n\n<hr id=answer>\n\n{{Back_FR}}",
                },
            ],
            css=basic_css,
        ),
        "cloze-bilingual": genanki.Model(
            BILINGUAL_CLOZE_MODEL_ID,
            "WSET 3 VIN Cloze Bilingual",
            fields=[
                {"name": "Text_EN"},
                {"name": "Extra_EN"},
                {"name": "Text_FR"},
                {"name": "Extra_FR"},
            ],
            templates=[
                {
                    "name": "EN",
                    "qfmt": "{{#Text_EN}}{{cloze:Text_EN}}{{/Text_EN}}",
                    "afmt": "{{cloze:Text_EN}}<br>{{Extra_EN}}",
                },
                {
                    "name": "FR",
                    "qfmt": "{{#Text_FR}}{{cloze:Text_FR}}{{/Text_FR}}",
                    "afmt": "{{cloze:Text_FR}}<br>{{Extra_FR}}",
                },
            ],
            css=cloze_css,
            model_type=genanki.Model.CLOZE,
        ),
    }


def _localize_mcq_front(template: str, suffix: str) -> str:
    body = template.replace("{{Question}}", f"{{{{Question_{suffix}}}}}").replace(
        "{{ChoicesFront}}", f"{{{{ChoicesFront_{suffix}}}}}"
    )
    return f"{{{{#Question_{suffix}}}}}{body}{{{{/Question_{suffix}}}}}"


def _localize_mcq_back(template: str, suffix: str) -> str:
    return (
        template.replace("{{Question}}", f"{{{{Question_{suffix}}}}}")
        .replace("{{ChoicesBack}}", f"{{{{ChoicesBack_{suffix}}}}}")
        .replace("{{Explanation}}", f"{{{{Explanation_{suffix}}}}}")
    )


def _ensure_decks(names: Iterable[str]) -> dict[str, genanki.Deck]:
    decks: dict[str, genanki.Deck] = {}
    for name in names:
        for path in ancestor_paths(name):
            if path not in decks:
                decks[path] = genanki.Deck(deck_id_for(path), path)
    if ROOT_DECK_NAME not in decks:
        decks[ROOT_DECK_NAME] = genanki.Deck(deck_id_for(ROOT_DECK_NAME), ROOT_DECK_NAME)
    return decks


def write_package(
    result: BuildResult,
    *,
    templates: Path,
    output: Path,
    mode: BuildLang,
) -> Path:
    models = load_models(templates)
    ui_en = load_ui(templates, "en")
    ui_fr = load_ui(templates, "fr")
    bilingual = mode == "bilingual"

    for note in result.notes:
        fill_fields(note, ui_en=ui_en, ui_fr=ui_fr, bilingual=bilingual)

    decks = _ensure_decks(note.deck for note in result.notes)
    for prepared in result.notes:
        decks[prepared.deck].add_note(
            genanki.Note(
                guid=prepared.guid,
                model=models[prepared.model],
                fields=prepared.fields,
                tags=prepared.tags,
            )
        )

    output.parent.mkdir(parents=True, exist_ok=True)
    package = genanki.Package(list(decks.values()))
    package.write_to_file(str(output))
    return output


def build_language(
    cards: list[Card],
    lang: BuildLang,
    *,
    templates: Path,
    out_dir: Path,
    include_drafts: bool = False,
) -> tuple[Path, BuildResult]:
    result = prepare(cards, lang, include_drafts=include_drafts)
    path = out_dir / PACKAGE_NAMES[lang]
    write_package(result, templates=templates, output=path, mode=lang)
    return path, result
