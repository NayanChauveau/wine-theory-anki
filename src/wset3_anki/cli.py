from __future__ import annotations

import argparse
import subprocess
import sys
from collections.abc import Sequence
from pathlib import Path

from wset3_anki.build import BuildLang, build_language
from wset3_anki.json_schema import default_schema_path, schema_matches, write_schema
from wset3_anki.load import LoadError, load_cards
from wset3_anki.paths import cards_dir, find_repo_root, templates_dir
from wset3_anki.validate import validate_cards


def _add_root_cards(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--cards", type=Path, default=None, help="Cards directory")
    parser.add_argument("--root", type=Path, default=None, help="Repository root")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="wset3-anki",
        description="Validate and build the WSET 3 VIN Anki deck from YAML sources.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_validate = sub.add_parser("validate", help="Validate card YAML against the schema")
    _add_root_cards(p_validate)

    p_schema = sub.add_parser("schema", help="Write or check schema/cards.schema.json")
    p_schema.add_argument(
        "--check",
        action="store_true",
        help="Fail if the committed JSON Schema is out of date",
    )
    p_schema.add_argument("--out", type=Path, default=None, help="Override output path")
    p_schema.add_argument("--root", type=Path, default=None, help="Repository root")

    p_check = sub.add_parser("check", help="Run the full quality gate (lint, types, tests, cards)")
    p_check.add_argument("--root", type=Path, default=None, help="Repository root")

    p_build = sub.add_parser("build", help="Generate .apkg packages")
    p_build.add_argument(
        "--lang",
        choices=("en", "fr", "all", "bilingual"),
        default="all",
        help="Which package(s) to emit",
    )
    p_build.add_argument("--out", type=Path, default=Path("dist"), help="Output directory")
    p_build.add_argument(
        "--include-drafts",
        action="store_true",
        help="Include cards with status: draft",
    )
    _add_root_cards(p_build)

    args = parser.parse_args(argv)
    root = find_repo_root(args.root) if getattr(args, "root", None) else find_repo_root()

    if args.command == "schema":
        return _schema_command(root, check=args.check, out=args.out)
    if args.command == "check":
        return _check_command(root)

    source = args.cards or cards_dir(root)
    templates = templates_dir(root)

    try:
        cards = load_cards(source)
    except LoadError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    issues = validate_cards(cards)
    if issues:
        for issue in issues:
            print(f"error: {issue}", file=sys.stderr)
        return 1

    if args.command == "validate":
        print(f"{len(cards)} card(s) OK")
        return 0

    languages: list[BuildLang] = ["en", "fr", "bilingual"] if args.lang == "all" else [args.lang]

    out_dir = args.out if args.out.is_absolute() else Path.cwd() / args.out
    for lang in languages:
        path, result = build_language(
            cards,
            lang,
            templates=templates,
            out_dir=out_dir,
            include_drafts=args.include_drafts,
        )
        print(
            f"wrote {path} ({len(result.notes)} notes, "
            f"{result.skipped_drafts} drafts skipped, "
            f"{result.skipped_untranslated} untranslated skipped)"
        )
    return 0


def _schema_command(root: Path, *, check: bool, out: Path | None) -> int:
    path = out or default_schema_path(root)
    if check:
        if schema_matches(path):
            print(f"{path} is up to date")
            return 0
        print(f"error: {path} is missing or stale; run `wset3-anki schema`", file=sys.stderr)
        return 1
    write_schema(path)
    print(f"wrote {path}")
    return 0


def _check_command(root: Path) -> int:
    steps: list[tuple[str, list[str]]] = [
        ("ruff lint", ["ruff", "check", str(root)]),
        ("ruff format", ["ruff", "format", "--check", str(root)]),
        ("basedpyright", ["basedpyright", str(root / "src"), str(root / "tests")]),
        ("json schema", ["wset3-anki", "schema", "--check", "--root", str(root)]),
        ("cards", ["wset3-anki", "validate", "--root", str(root)]),
        ("pytest", ["pytest", str(root / "tests")]),
    ]
    failed = 0
    for label, command in steps:
        print(f"→ {label}", flush=True)
        result = subprocess.run(command, cwd=root, check=False)
        if result.returncode != 0:
            print(f"✗ {label} failed", file=sys.stderr)
            failed = 1
    if failed:
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
