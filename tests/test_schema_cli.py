from __future__ import annotations

from pathlib import Path

from wset3_anki.cli import main


def test_schema_write_and_check(repo_root: Path, tmp_path: Path) -> None:
    out = tmp_path / "cards.schema.json"
    assert main(["schema", "--root", str(repo_root), "--out", str(out)]) == 0
    assert out.is_file()
    assert main(["schema", "--check", "--root", str(repo_root), "--out", str(out)]) == 0
    out.write_text("stale\n", encoding="utf-8")
    assert main(["schema", "--check", "--root", str(repo_root), "--out", str(out)]) == 1
