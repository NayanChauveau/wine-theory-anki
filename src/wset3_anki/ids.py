from __future__ import annotations

import hashlib

import genanki

NAMESPACE = "wset3-vin"
ROOT_DECK_NAME = "WSET 3 VIN"

# Hardcoded so re-imports update existing models instead of creating duplicates.
MCQ_MODEL_ID = 1760000101
BASIC_MODEL_ID = 1760000102
CLOZE_MODEL_ID = 1760000103
BILINGUAL_MCQ_MODEL_ID = 1760000104
BILINGUAL_BASIC_MODEL_ID = 1760000105
BILINGUAL_CLOZE_MODEL_ID = 1760000106
ROOT_DECK_ID = 1760001000


def note_guid(card_id: str, lang: str) -> str:
    """Stable Anki GUID. `lang` is en, fr, or bilingual."""
    return genanki.guid_for(NAMESPACE, card_id, lang)


def deck_id_for(deck_path: str) -> int:
    if deck_path == ROOT_DECK_NAME:
        return ROOT_DECK_ID
    digest = hashlib.sha256(f"{NAMESPACE}:{deck_path}".encode()).hexdigest()
    return ROOT_DECK_ID + 1 + (int(digest[:8], 16) % 8_000_000)


def deck_path(chapter: str, *, root: str = ROOT_DECK_NAME) -> str:
    chapter = chapter.strip()
    if not chapter:
        return root
    return f"{root}::{chapter}"


def ancestor_paths(deck_path_name: str) -> list[str]:
    parts = deck_path_name.split("::")
    return ["::".join(parts[: i + 1]) for i in range(len(parts))]
