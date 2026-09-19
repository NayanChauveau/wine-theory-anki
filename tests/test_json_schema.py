from __future__ import annotations

from pathlib import Path

import jsonschema
import pytest
import yaml
from pydantic import ValidationError

from tests.conftest import make_mcq
from wset3_anki.json_schema import card_file_json_schema, schema_json, schema_matches, write_schema
from wset3_anki.schema import CardAdapter


def test_unknown_fields_are_rejected() -> None:
    with pytest.raises(ValidationError, match="Extra inputs"):
        CardAdapter.validate_python(
            {
                "id": "test-card-001",
                "type": "mcq",
                "deck": "SAT",
                "typo": True,
                "en": {
                    "question": "Q?",
                    "choices": [
                        {"text": "A", "correct": True},
                        {"text": "B", "correct": False},
                    ],
                    "explanation": "Because A.",
                },
            }
        )


def test_committed_schema_is_current(repo_root: Path) -> None:
    assert schema_matches(repo_root / "schema" / "cards.schema.json"), (
        "schema/cards.schema.json is stale; run `uv run wset3-anki schema`"
    )


def test_schema_roundtrip(tmp_path: Path) -> None:
    path = tmp_path / "cards.schema.json"
    write_schema(path)
    assert path.read_text(encoding="utf-8") == schema_json()
    assert schema_matches(path)


def test_all_chapter_files_match_json_schema(repo_root: Path) -> None:
    validator = jsonschema.Draft202012Validator(card_file_json_schema())
    for path in sorted((repo_root / "cards").glob("*.yaml")):
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
        errors = list(validator.iter_errors(raw))
        assert errors == [], f"{path.name}: {errors[0].message}"


def test_sample_mcq_matches_json_schema() -> None:
    card = make_mcq()
    validator = jsonschema.Draft202012Validator(card_file_json_schema())
    validator.validate({"cards": [card.model_dump(mode="json")]})
