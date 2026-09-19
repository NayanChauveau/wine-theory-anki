from __future__ import annotations

import pytest
from pydantic import ValidationError

from tests.conftest import make_mcq
from wset3_anki.schema import CardAdapter


def test_mcq_requires_exactly_one_correct() -> None:
    with pytest.raises(ValidationError, match="exactly one correct"):
        CardAdapter.validate_python(
            {
                "id": "bad-card-001",
                "type": "mcq",
                "deck": "SAT",
                "en": {
                    "question": "Q?",
                    "choices": [
                        {"text": "A", "correct": True},
                        {"text": "B", "correct": True},
                    ],
                    "explanation": "Nope.",
                },
            }
        )


def test_id_must_be_kebab_case() -> None:
    with pytest.raises(ValidationError, match="pattern"):
        make_mcq(id="NotValid")


def test_cloze_requires_deletion() -> None:
    with pytest.raises(ValidationError, match="cloze"):
        CardAdapter.validate_python(
            {
                "id": "cloze-bad-001",
                "type": "cloze",
                "deck": "Bordeaux",
                "en": {"text": "No deletion here"},
            }
        )


def test_optional_french_is_allowed() -> None:
    card = make_mcq(fr=None)
    assert card.fr is None
