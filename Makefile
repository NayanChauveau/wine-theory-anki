.PHONY: check lint format typecheck validate schema test build import-extract import-status

check:
	uv run wset3-anki check

lint:
	uv run ruff check .
	uv run ruff format --check .

format:
	uv run ruff format .
	uv run ruff check --fix .

typecheck:
	uv run basedpyright src tests

validate:
	uv run wset3-anki validate

schema:
	uv run wset3-anki schema

test:
	uv run pytest

build:
	uv run wset3-anki build --lang all --out dist

import-extract:
	uv run wset3-anki import-extract

import-status:
	uv run wset3-anki import-status
