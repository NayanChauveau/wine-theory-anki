from __future__ import annotations

from wset3_anki.ids import ROOT_DECK_ID, ROOT_DECK_NAME, deck_id_for, deck_path, note_guid


def test_note_guid_is_stable_and_language_specific() -> None:
    en_a = note_guid("sat-acidity-001", "en")
    en_b = note_guid("sat-acidity-001", "en")
    fr = note_guid("sat-acidity-001", "fr")
    bilingual = note_guid("sat-acidity-001", "bilingual")
    assert en_a == en_b
    assert en_a != fr
    assert en_a != bilingual
    assert fr != bilingual


def test_deck_ids_are_deterministic() -> None:
    path = deck_path("France::Bordeaux")
    assert path == "WSET 3 VIN::France::Bordeaux"
    assert deck_id_for(ROOT_DECK_NAME) == ROOT_DECK_ID
    assert deck_id_for(path) == deck_id_for(path)
    assert deck_id_for(path) != deck_id_for(deck_path("SAT"))
