from __future__ import annotations

import hashlib

import genanki

NAMESPACE = "wset3-vin"
ROOT_DECK_NAME_EN = "WSET 3 Wine"
ROOT_DECK_NAME_FR = "WSET 3 VIN"
ROOT_DECK_NAME_BILINGUAL = "WSET 3"
ROOT_DECK_NAME = ROOT_DECK_NAME_EN

# Hardcoded so re-imports update existing models instead of creating duplicates.
MCQ_MODEL_ID = 1760000101
BASIC_MODEL_ID = 1760000102
CLOZE_MODEL_ID = 1760000103
BILINGUAL_MCQ_MODEL_ID = 1760000104
BILINGUAL_BASIC_MODEL_ID = 1760000105
BILINGUAL_CLOZE_MODEL_ID = 1760000106
ROOT_DECK_ID = 1760001000
ROOT_DECK_IDS = {
    ROOT_DECK_NAME_EN: 1760001000,
    ROOT_DECK_NAME_FR: 1760001001,
    ROOT_DECK_NAME_BILINGUAL: 1760001002,
}


def note_guid(card_id: str, lang: str) -> str:
    """Stable Anki GUID. `lang` is en, fr, or bilingual."""
    return genanki.guid_for(NAMESPACE, card_id, lang)


def deck_id_for(deck_path_name: str) -> int:
    if deck_path_name in ROOT_DECK_IDS:
        return ROOT_DECK_IDS[deck_path_name]
    digest = hashlib.sha256(f"{NAMESPACE}:{deck_path_name}".encode()).hexdigest()
    return ROOT_DECK_ID + 1 + (int(digest[:8], 16) % 8_000_000)


def deck_path(chapter: str, *, root: str = ROOT_DECK_NAME) -> str:
    chapter = chapter.strip()
    if not chapter:
        return root
    return f"{root}::{chapter}"


def ancestor_paths(deck_path_name: str) -> list[str]:
    parts = deck_path_name.split("::")
    return ["::".join(parts[: i + 1]) for i in range(len(parts))]
