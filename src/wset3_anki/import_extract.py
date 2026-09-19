from __future__ import annotations

import json
import sqlite3
import tempfile
import zipfile
from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import yaml

from wset3_anki.htmltext import html_to_text
from wset3_anki.import_map import ChapterTarget, classify_root_text, target_from_deck_name
from wset3_anki.import_progress import ProgressStore


@dataclass
class RawNote:
    source_id: str
    source_deck: str
    front: str
    back: str
    name: str = ""
    tags: str = ""


def default_apkg_path(root: Path) -> Path:
    return root / "import" / "WSET_Level_3_--_NEW.apkg"


def inbox_dir(root: Path) -> Path:
    return root / "import" / "inbox"


def _deck_map(con: sqlite3.Connection) -> dict[int, str]:
    raw = json.loads(con.execute("select decks from col").fetchone()[0])
    return {int(key): value["name"] for key, value in raw.items()}


def _note_fields(flds: str) -> tuple[str, str, str]:
    parts = flds.split("\x1f")
    if len(parts) >= 3:
        return html_to_text(parts[0]), html_to_text(parts[1]), html_to_text(parts[2])
    if len(parts) == 2:
        return "", html_to_text(parts[0]), html_to_text(parts[1])
    return "", html_to_text(parts[0]), ""


def extract_notes(apkg: Path) -> list[tuple[ChapterTarget, RawNote, str]]:
    if not apkg.is_file():
        raise FileNotFoundError(apkg)
    rows: list[tuple[ChapterTarget, RawNote, str]] = []
    with tempfile.TemporaryDirectory() as tmp:
        with zipfile.ZipFile(apkg) as archive:
            archive.extract("collection.anki2", tmp)
        con = sqlite3.connect(Path(tmp) / "collection.anki2")
        decks = _deck_map(con)
        query = """
            select n.id, n.flds, n.tags, c.did
            from notes n
            join cards c on c.nid = n.id
            order by n.id
        """
        counters: dict[str, int] = defaultdict(int)
        seen_notes: set[int] = set()
        for note_id, flds, tags, did in con.execute(query):
            if note_id in seen_notes:
                continue
            seen_notes.add(note_id)
            name, front, back = _note_fields(flds)
            source_deck = decks.get(int(did), "Unknown")
            target = target_from_deck_name(source_deck)
            if target is None:
                target = classify_root_text(front, back, tags)
            counters[target.slug] += 1
            source_id = f"{target.slug}-{counters[target.slug]:04d}"
            rows.append(
                (
                    target,
                    RawNote(
                        source_id=source_id,
                        source_deck=source_deck,
                        front=front,
                        back=back,
                        name=name,
                        tags=tags.strip(),
                    ),
                    target.cards_file,
                )
            )
        con.close()
    return rows


def _dump_yaml(data: Any) -> str:
    return yaml.safe_dump(
        data,
        allow_unicode=True,
        sort_keys=False,
        default_flow_style=False,
        width=88,
    )


def write_inbox(root: Path, rows: list[tuple[ChapterTarget, RawNote, str]]) -> dict[str, int]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for target, note, _cards_file in rows:
        payload = asdict(note)
        grouped[target.inbox_name].append(payload)
    dest = inbox_dir(root)
    dest.mkdir(parents=True, exist_ok=True)
    counts: dict[str, int] = {}
    for filename, notes in grouped.items():
        path = dest / filename
        path.write_text(_dump_yaml({"notes": notes}), encoding="utf-8")
        counts[filename] = len(notes)
    return counts


def run_extract(root: Path, apkg: Path) -> tuple[int, dict[str, int]]:
    rows = extract_notes(apkg)
    counts = write_inbox(root, rows)
    store = ProgressStore.load(root)
    for target, note, cards_file in rows:
        store.ensure(
            note.source_id,
            inbox=target.inbox_name,
            target=cards_file,
            source_deck=note.source_deck,
        )
    store.save()
    return len(rows), counts
