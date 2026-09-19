from __future__ import annotations

from pathlib import Path

from wset3_anki.cli import main


def test_cli_validate(repo_root: Path) -> None:
    assert main(["validate", "--root", str(repo_root)]) == 0


def test_cli_build_all(repo_root: Path, tmp_path: Path) -> None:
    assert main(["build", "--root", str(repo_root), "--lang", "all", "--out", str(tmp_path)]) == 0
    assert (tmp_path / "wset3-vin-en.apkg").exists()
    assert (tmp_path / "wset3-vin-fr.apkg").exists()
    assert (tmp_path / "wset3-vin-bilingual.apkg").exists()
