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


def _choice_div(choice: Choice, index: int, *, kind: str | None = None) -> str:
    klass = f' class="choice {kind}"' if kind else ' class="choice"'
    return (
        f'<div{klass} data-i="{index}">'
        f'<span class="letter">{LETTERS[index]}</span>'
        f'<span class="text">{escape(choice.text)}</span>'
        "</div>"
    )


def render_choices_front(choices: list[Choice], card_id: str = "") -> str:
    items = [_choice_div(choice, index) for index, choice in enumerate(choices)]
    return _choices_box(items, card_id)


def render_choices_back(choices: list[Choice], card_id: str = "") -> str:
    items = []
    for index, choice in enumerate(choices):
        kind = "correct" if choice.correct else "incorrect"
        items.append(_choice_div(choice, index, kind=kind))
    return _choices_box(items, card_id)


def _choices_box(items: list[str], card_id: str) -> str:
    attr = f' data-card="{escape(card_id)}"' if card_id else ""
    return f'<div class="choices"{attr}>' + "".join(items) + "</div>"


def inject_mcq_shuffle(template: str, js: str, *, reveal: bool) -> str:
    if "WSET3_SHUFFLE_JS" not in template:
        raise ValueError("MCQ template is missing the shuffle placeholder")
    return template.replace("WSET3_SHUFFLE_JS", js).replace(
        "WSET3_SHUFFLE_REVEAL", "true" if reveal else "false"
    )


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
