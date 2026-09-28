from __future__ import annotations

from pathlib import Path

import pytest

import wset3_anki.cli
from wset3_anki.cli import main


def test_cli_validate(repo_root: Path) -> None:
    assert main(["validate", "--root", str(repo_root)]) == 0


def test_cli_build_all(repo_root: Path, tmp_path: Path) -> None:
    assert main(["build", "--root", str(repo_root), "--lang", "all", "--out", str(tmp_path)]) == 0
    assert (tmp_path / "wset3-vin-en.apkg").exists()
    assert (tmp_path / "wset3-vin-fr.apkg").exists()
    assert not (tmp_path / "wset3-vin-bilingual.apkg").exists()


def test_cli_push_builds_imports_and_syncs(
    repo_root: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    pushed: list[Path] = []

    def fake_push(packages: list[Path], **_kwargs: object) -> None:
        pushed.extend(packages)

    monkeypatch.setattr(wset3_anki.cli, "push_packages", fake_push)

    assert main(["push", "--root", str(repo_root), "--lang", "fr", "--out", str(tmp_path)]) == 0
    assert pushed == [tmp_path / "wset3-vin-fr.apkg"]
