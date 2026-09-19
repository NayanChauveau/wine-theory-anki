from __future__ import annotations

from pathlib import Path

from tests.conftest import make_mcq
from wset3_anki.build import prepare
from wset3_anki.decks import load_deck_i18n
from wset3_anki.ids import ROOT_DECK_ID, ROOT_DECK_IDS, deck_id_for, deck_path


def test_english_root_is_wine(templates_dir: Path) -> None:
    i18n = load_deck_i18n(templates_dir)
    assert i18n.localize("SAT", "en") == "WSET 3 Wine::SAT"
    assert i18n.localize("France::Bordeaux", "en") == "WSET 3 Wine::France::Bordeaux"


def test_french_root_and_translated_categories(templates_dir: Path) -> None:
    i18n = load_deck_i18n(templates_dir)
    assert i18n.localize("SAT", "fr") == "WSET 3 VIN::ASD"
    assert i18n.localize("France::Burgundy", "fr") == "WSET 3 VIN::France::Bourgogne"
    assert i18n.localize("Germany", "fr") == "WSET 3 VIN::Allemagne"
    assert i18n.localize("Sherry", "fr") == "WSET 3 VIN::Xérès"
    assert i18n.localize("Port", "fr") == "WSET 3 VIN::Porto"


def test_proper_nouns_stay_the_same(templates_dir: Path) -> None:
    i18n = load_deck_i18n(templates_dir)
    assert i18n.localize("France::Bordeaux", "fr") == "WSET 3 VIN::France::Bordeaux"
    assert i18n.localize("Alsace", "fr") == "WSET 3 VIN::Alsace"


def test_bilingual_root_is_neutral(templates_dir: Path) -> None:
    i18n = load_deck_i18n(templates_dir)
    assert i18n.localize("SAT", "bilingual") == "WSET 3::SAT"


def test_unknown_segment_is_kept(templates_dir: Path) -> None:
    i18n = load_deck_i18n(templates_dir)
    assert i18n.localize("Mystery Region", "fr") == "WSET 3 VIN::Mystery Region"


def test_prepare_uses_localized_deck_names(templates_dir: Path) -> None:
    card = make_mcq(deck="France::Burgundy")
    en = prepare([card], "en", templates=templates_dir)
    fr = prepare([card], "fr", templates=templates_dir)
    assert en.notes[0].deck == "WSET 3 Wine::France::Burgundy"
    assert fr.notes[0].deck == "WSET 3 VIN::France::Bourgogne"


def test_root_deck_ids_are_stable() -> None:
    assert deck_id_for("WSET 3 Wine") == ROOT_DECK_ID
    assert deck_id_for("WSET 3 VIN") == ROOT_DECK_IDS["WSET 3 VIN"]
    assert deck_id_for("WSET 3 Wine") != deck_id_for("WSET 3 VIN")
    left = deck_path("France::Bordeaux", root="WSET 3 Wine")
    right = deck_path("France::Bordeaux", root="WSET 3 VIN")
    assert deck_id_for(left) != deck_id_for(right)
