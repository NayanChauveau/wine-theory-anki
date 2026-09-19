from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import yaml

from wset3_anki.ids import deck_path

DeckLang = Literal["en", "fr", "bilingual"]


@dataclass(frozen=True)
class DeckI18n:
    root: dict[str, str]
    segments: dict[str, dict[str, str]]

    def root_name(self, lang: DeckLang) -> str:
        return self.root[lang]

    def segment(self, key: str, lang: DeckLang) -> str:
        labels = self.segments.get(key)
        if not labels:
            return key
        if lang == "bilingual":
            return labels.get("en", key)
        return labels.get(lang, key)

    def localize(self, chapter: str, lang: DeckLang) -> str:
        parts = [part.strip() for part in chapter.split("::") if part.strip()]
        translated = [self.segment(part, lang) for part in parts]
        return deck_path("::".join(translated), root=self.root_name(lang))


def load_deck_i18n(templates: Path) -> DeckI18n:
    path = templates / "ui" / "decks.yaml"
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError(f"{path} must be a mapping")
    root = {str(key): str(value) for key, value in raw.get("root", {}).items()}
    segments: dict[str, dict[str, str]] = {}
    for key, labels in (raw.get("segments") or {}).items():
        if not isinstance(labels, dict):
            continue
        segments[str(key)] = {str(lang): str(label) for lang, label in labels.items()}
    for required in ("en", "fr", "bilingual"):
        if required not in root:
            raise ValueError(f"{path}: root.{required} is required")
    return DeckI18n(root=root, segments=segments)
