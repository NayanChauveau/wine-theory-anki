from __future__ import annotations

import zipfile
from pathlib import Path

import pytest

from tests.conftest import make_mcq
from wset3_anki.build import build_language, load_models, prepare
from wset3_anki.ids import note_guid
from wset3_anki.load import load_cards
from wset3_anki.render import (
    inject_mcq_shuffle,
    render_choices_back,
    render_choices_front,
    render_markdown,
)
from wset3_anki.schema import Status


def test_drafts_are_excluded_by_default() -> None:
    cards = [make_mcq(), make_mcq(id="test-card-draft", status=Status.DRAFT)]
    result = prepare(cards, "en")
    assert [note.card.id for note in result.notes] == ["test-card-001"]
    assert result.skipped_drafts == 1


def test_drafts_can_be_included() -> None:
    cards = [make_mcq(id="test-card-draft", status=Status.DRAFT)]
    result = prepare(cards, "en", include_drafts=True)
    assert len(result.notes) == 1


def test_french_build_skips_untranslated_cards() -> None:
    cards = [make_mcq(fr=None), make_mcq(id="test-card-002")]
    result = prepare(cards, "fr")
    assert [note.card.id for note in result.notes] == ["test-card-002"]
    assert result.skipped_untranslated == 1


def test_english_build_keeps_untranslated_cards() -> None:
    result = prepare([make_mcq(fr=None)], "en")
    assert len(result.notes) == 1
    assert result.notes[0].guid == note_guid("test-card-001", "en")


def test_bilingual_uses_a_distinct_guid() -> None:
    result = prepare([make_mcq()], "bilingual")
    assert result.notes[0].guid == note_guid("test-card-001", "bilingual")
    assert result.notes[0].model == "mcq-bilingual"


def test_markdown_explanation_is_rendered(templates_dir: Path, tmp_path: Path) -> None:
    path, result = build_language(
        [make_mcq()],
        "en",
        templates=templates_dir,
        out_dir=tmp_path,
    )
    assert path.exists()
    explanation = result.notes[0].fields[-1]
    assert "<strong>yes</strong>" in explanation
    assert "Why" in explanation


def test_french_ui_label(templates_dir: Path, tmp_path: Path) -> None:
    _, result = build_language(
        [make_mcq()],
        "fr",
        templates=templates_dir,
        out_dir=tmp_path,
    )
    assert "Pourquoi" in result.notes[0].fields[-1]


def test_apkg_is_a_zip(templates_dir: Path, tmp_path: Path) -> None:
    path, _ = build_language(
        [make_mcq()],
        "bilingual",
        templates=templates_dir,
        out_dir=tmp_path,
    )
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
    assert any(name.startswith("collection.anki") for name in names)


def test_repo_sample_cards_validate_and_build(
    repo_root: Path, templates_dir: Path, tmp_path: Path
) -> None:
    cards = load_cards(repo_root / "cards")
    assert len(cards) >= 5
    path, result = build_language(
        cards,
        "en",
        templates=templates_dir,
        out_dir=tmp_path,
    )
    reviewed = [card for card in cards if card.status.value != "draft"]
    assert result.skipped_drafts == len(cards) - len(reviewed)
    assert path.name == "wset3-vin-en.apkg"
    assert len(result.notes) == len(reviewed)


def test_render_markdown_bold() -> None:
    assert "<strong>mouth-watering</strong>" in render_markdown("**mouth-watering**")


def test_mcq_choices_carry_stable_indexes() -> None:
    card = make_mcq()
    front = render_choices_front(card.en.choices, card.id)
    back = render_choices_back(card.en.choices, card.id)
    assert 'data-card="test-card-001"' in front
    assert 'data-i="0"' in front
    assert 'data-i="1"' in front
    assert 'data-i="1"' in back
    assert "choice correct" in back


def test_mcq_templates_shuffle_each_review(templates_dir: Path) -> None:
    models = load_models(templates_dir)
    front = models["mcq"].templates[0]["qfmt"]
    back = models["mcq"].templates[0]["afmt"]
    assert "wset3ShuffleChoices(false)" in front
    assert "wset3ShuffleChoices(true)" in back
    assert "wset3Choose(" in front
    assert "wset3MarkPick(" in back
    assert "WSET3_SHUFFLE_JS" not in front
    assert "{{" not in (templates_dir / "mcq" / "shuffle.js").read_text()
    bilingual_front = models["mcq-bilingual"].templates[0]["qfmt"]
    assert "wset3ShuffleChoices(false)" in bilingual_front
    assert "{{Question_EN}}" in bilingual_front


def test_inject_mcq_shuffle_requires_placeholder() -> None:
    with pytest.raises(ValueError, match="shuffle placeholder"):
        inject_mcq_shuffle("<div></div>", "function wset3ShuffleChoices() {}", reveal=False)
