from __future__ import annotations

from pathlib import Path


def find_repo_root(start: Path | None = None) -> Path:
    here = (start or Path.cwd()).resolve()
    for candidate in [here, *here.parents]:
        if (candidate / "cards").is_dir() and (candidate / "templates").is_dir():
            return candidate
    return here


def cards_dir(root: Path | None = None) -> Path:
    return (root or find_repo_root()) / "cards"


def templates_dir(root: Path | None = None) -> Path:
    return (root or find_repo_root()) / "templates"
