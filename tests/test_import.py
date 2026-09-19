from __future__ import annotations

from pathlib import Path

from wset3_anki.htmltext import html_to_text
from wset3_anki.import_map import (
    CHAPTERS,
    classify_root_text,
    published_targets,
    target_from_deck_name,
)
from wset3_anki.import_progress import ProgressStore
from wset3_anki.schema import CardAdapter, FactCheck


def test_html_to_text_strips_markup() -> None:
    assert html_to_text("<p>CO2</p>") == "CO2"
    assert html_to_text("low&nbsp;&amp; high<br />next") == "low & high\nnext"


def test_cxx_mapping() -> None:
    target = target_from_deck_name("WSET Level 3::WSET Level 3 C16 - Beaujolais")
    assert target is not None
    assert target.slug == "c16"
    assert target.cards_file == "c16-beaujolais.yaml"
    assert target.deck == "France::Beaujolais"
    assert 33 in CHAPTERS
    assert CHAPTERS[33].deck == "USA::California"


def test_root_heuristic_sat_and_vine() -> None:
    sat = classify_root_text("How should red wine color be assessed?", "look at the rim", "c1_sat")
    assert sat.slug == "c01"
    vine = classify_root_text("List the key stages of a vine's growth cycle", "Budburst")
    assert vine.slug == "c03"


def test_progress_keeps_existing_status(tmp_path: Path) -> None:
    store = ProgressStore.load(tmp_path)
    store.ensure("c16-0001", inbox="c16-beaujolais.yaml", target="x.yaml", source_deck="Beaujolais")
    store.set_status("c16-0001", "done")
    store.ensure("c16-0001", inbox="c16-beaujolais.yaml", target="y.yaml", source_deck="Beaujolais")
    assert store.notes["c16-0001"].status == "done"
    assert store.notes["c16-0001"].target == "y.yaml"
    store.save()
    reloaded = ProgressStore.load(tmp_path)
    assert reloaded.notes["c16-0001"].status == "done"
    assert reloaded.notes["c16-0001"].target == "y.yaml"


def test_beaujolais_cards_are_reviewed_with_source_ids(repo_root: Path) -> None:
    from wset3_anki.load import load_card_file

    cards = load_card_file(repo_root / "cards" / "c16-beaujolais.yaml")
    assert len(cards) >= 30
    assert all(card.status.value == "reviewed" for card in cards)
    assert all(card.source_id and card.source_id.startswith("c16-") for card in cards)
    assert {card.source_id for card in cards} >= {f"c16-{i:04d}" for i in range(1, 31)}


def test_south_west_cards_are_reviewed_with_source_ids(repo_root: Path) -> None:
    from wset3_anki.load import load_card_file

    cards = load_card_file(repo_root / "cards" / "c14-south-west.yaml")
    assert len(cards) >= 25
    assert all(card.status.value == "reviewed" for card in cards)
    assert all(card.source_id and card.source_id.startswith("c14-") for card in cards)
    assert {card.source_id for card in cards} >= {f"c14-{i:04d}" for i in range(1, 26)}


def test_cards_files_match_source_chapters(repo_root: Path) -> None:
    cards_dir = repo_root / "cards"
    published = published_targets()
    expected = {target.cards_file for target in published}
    actual = {path.name for path in cards_dir.glob("*.yaml")}
    assert expected == actual
    assert all(target.cards_file == target.inbox_name for target in published)


def test_card_schema_accepts_source_and_review() -> None:
    card = CardAdapter.validate_python(
        {
            "id": "beaujolais-gamay-001",
            "type": "mcq",
            "deck": "France::Beaujolais",
            "status": "draft",
            "source_id": "c16-0001",
            "review": {"fact_check": "pass", "sources": ["known-fact"]},
            "en": {
                "question": "Which grape is traditional in Beaujolais?",
                "choices": [
                    {"text": "Gamay", "correct": True},
                    {"text": "Pinot Noir", "correct": False},
                ],
                "explanation": "Beaujolais is **Gamay** country.",
            },
        }
    )
    assert card.source_id == "c16-0001"
    assert card.review is not None
    assert card.review.fact_check is FactCheck.PASS
