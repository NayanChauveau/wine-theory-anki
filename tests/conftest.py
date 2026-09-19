from __future__ import annotations

from pathlib import Path

import pytest

from wset3_anki.schema import CardAdapter, McqCard

REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURES = Path(__file__).resolve().parent / "fixtures"


@pytest.fixture
def repo_root() -> Path:
    return REPO_ROOT


@pytest.fixture
def templates_dir(repo_root: Path) -> Path:
    return repo_root / "templates"


def make_mcq(**overrides: object) -> McqCard:
    payload: dict[str, object] = {
        "id": "test-card-001",
        "type": "mcq",
        "deck": "SAT",
        "tags": ["sat"],
        "status": "reviewed",
        "en": {
            "question": "Which is correct?",
            "choices": [
                {"text": "No", "correct": False},
                {"text": "Yes", "correct": True},
            ],
            "explanation": "Because **yes** is right.",
        },
        "fr": {
            "question": "Laquelle est correcte ?",
            "choices": [
                {"text": "Non", "correct": False},
                {"text": "Oui", "correct": True},
            ],
            "explanation": "Parce que **oui** est juste.",
        },
    }
    payload.update(overrides)
    card = CardAdapter.validate_python(payload)
    assert isinstance(card, McqCard)
    return card
