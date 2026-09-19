from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

import yaml

ProgressStatus = Literal["pending", "in_progress", "split", "done", "rejected"]


@dataclass
class ProgressEntry:
    status: ProgressStatus = "pending"
    inbox: str = ""
    target: str = ""
    source_deck: str = ""


@dataclass
class ProgressStore:
    path: Path
    notes: dict[str, ProgressEntry] = field(default_factory=dict)

    @staticmethod
    def progress_path(root: Path) -> Path:
        return root / "import" / "progress.yaml"

    @classmethod
    def load(cls, root: Path) -> ProgressStore:
        path = cls.progress_path(root)
        notes: dict[str, ProgressEntry] = {}
        if path.is_file():
            raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
            for source_id, value in (raw.get("notes") or {}).items():
                notes[str(source_id)] = ProgressEntry(
                    status=value.get("status", "pending"),
                    inbox=value.get("inbox", ""),
                    target=value.get("target", ""),
                    source_deck=value.get("source_deck", ""),
                )
        return cls(path=path, notes=notes)

    def ensure(
        self,
        source_id: str,
        *,
        inbox: str,
        target: str,
        source_deck: str,
    ) -> None:
        existing = self.notes.get(source_id)
        if existing is None:
            self.notes[source_id] = ProgressEntry(
                status="pending",
                inbox=inbox,
                target=target,
                source_deck=source_deck,
            )
            return
        existing.inbox = inbox
        existing.target = target
        existing.source_deck = source_deck

    def set_status(self, source_id: str, status: ProgressStatus) -> None:
        if source_id not in self.notes:
            raise KeyError(source_id)
        self.notes[source_id].status = status

    def save(self) -> Path:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "notes": {
                source_id: {
                    "status": entry.status,
                    "inbox": entry.inbox,
                    "target": entry.target,
                    "source_deck": entry.source_deck,
                }
                for source_id, entry in sorted(self.notes.items())
            }
        }
        self.path.write_text(
            yaml.safe_dump(payload, allow_unicode=True, sort_keys=False),
            encoding="utf-8",
        )
        return self.path

    def counts(self) -> dict[str, int]:
        counter: Counter[str] = Counter(entry.status for entry in self.notes.values())
        return {
            "total": len(self.notes),
            "pending": counter.get("pending", 0),
            "in_progress": counter.get("in_progress", 0),
            "split": counter.get("split", 0),
            "done": counter.get("done", 0),
            "rejected": counter.get("rejected", 0),
        }

    def chapter_counts(self) -> list[tuple[str, int, int]]:
        pending: Counter[str] = Counter()
        total: Counter[str] = Counter()
        for entry in self.notes.values():
            key = entry.inbox or "(none)"
            total[key] += 1
            if entry.status == "pending":
                pending[key] += 1
        return sorted((name, total[name], pending[name]) for name in total)
