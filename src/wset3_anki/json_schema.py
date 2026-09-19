from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from wset3_anki.schema import CardFile

SCHEMA_FILENAME = "cards.schema.json"


def card_file_json_schema() -> dict[str, Any]:
    schema = CardFile.model_json_schema()
    schema["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    schema["$id"] = "wset3-vin/cards.schema.json"
    schema["title"] = "WSET 3 VIN card file"
    schema["description"] = (
        "One chapter of Anki cards (EN + optional FR). See CONTENT_GUIDELINES.md."
    )
    return schema


def schema_json() -> str:
    return json.dumps(card_file_json_schema(), indent=2, ensure_ascii=False) + "\n"


def default_schema_path(root: Path) -> Path:
    return root / "schema" / SCHEMA_FILENAME


def write_schema(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(schema_json(), encoding="utf-8")
    return path


def schema_matches(path: Path) -> bool:
    return path.is_file() and path.read_text(encoding="utf-8") == schema_json()
