from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import ValidationError

from wset3_anki.schema import Card, CardAdapter, CardFile


class LoadError(Exception):
    def __init__(self, path: Path, message: str) -> None:
        super().__init__(f"{path}: {message}")
        self.path = path
        self.message = message


def load_card_file(path: Path) -> list[Card]:
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if raw is None:
        return []
    try:
        if isinstance(raw, list):
            return [CardAdapter.validate_python(item) for item in raw]
        if isinstance(raw, dict):
            return list(CardFile.model_validate(raw).cards)
    except ValidationError as exc:
        raise LoadError(path, str(exc)) from exc
    raise LoadError(path, "YAML must be a list of cards or a mapping with a 'cards' key")


def load_cards(cards_directory: Path) -> list[Card]:
    files = sorted(cards_directory.glob("*.yaml")) + sorted(cards_directory.glob("*.yml"))
    # glob twice can duplicate if we aren't careful; use a set of paths
    seen: set[Path] = set()
    cards: list[Card] = []
    for path in files:
        resolved = path.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        cards.extend(load_card_file(path))
    return cards
