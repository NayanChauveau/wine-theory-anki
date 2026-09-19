from __future__ import annotations

import html
from functools import lru_cache
from pathlib import Path

import markdown
import yaml

from wset3_anki.schema import Choice

LETTERS = "ABCDEFGHIJ"


@lru_cache(maxsize=1)
def _md() -> markdown.Markdown:
    return markdown.Markdown(extensions=["extra", "sane_lists", "nl2br"])


def render_markdown(text: str) -> str:
    converter = _md()
    converter.reset()
    return converter.convert(text.strip())


def escape(text: str) -> str:
    return html.escape(text, quote=True)


def render_choices_front(choices: list[Choice]) -> str:
    items = []
    for index, choice in enumerate(choices):
        items.append(
            '<div class="choice">'
            f'<span class="letter">{LETTERS[index]}</span>'
            f'<span class="text">{escape(choice.text)}</span>'
            "</div>"
        )
    return '<div class="choices">' + "".join(items) + "</div>"


def render_choices_back(choices: list[Choice]) -> str:
    items = []
    for index, choice in enumerate(choices):
        kind = "correct" if choice.correct else "incorrect"
        items.append(
            f'<div class="choice {kind}">'
            f'<span class="letter">{LETTERS[index]}</span>'
            f'<span class="text">{escape(choice.text)}</span>'
            "</div>"
        )
    return '<div class="choices">' + "".join(items) + "</div>"


def load_ui(templates: Path, lang: str) -> dict[str, str]:
    path = templates / "ui" / f"{lang}.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"UI file {path} must be a mapping")
    return {str(key): str(value) for key, value in data.items()}


def wrap_explanation(body_html: str, label: str) -> str:
    return (
        '<section class="explanation">'
        f'<h2 class="explanation-label">{escape(label)}</h2>'
        f'<div class="explanation-body">{body_html}</div>'
        "</section>"
    )


def read_template(templates: Path, note_type: str, filename: str) -> str:
    return (templates / note_type / filename).read_text(encoding="utf-8")
