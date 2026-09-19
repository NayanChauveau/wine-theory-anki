from __future__ import annotations

from tests.conftest import make_mcq
from wset3_anki.validate import validate_cards


def test_duplicate_ids_are_rejected() -> None:
    issues = validate_cards([make_mcq(), make_mcq()])
    assert any("duplicate" in issue.message for issue in issues)


def test_fr_must_match_en_choice_count() -> None:
    card = make_mcq()
    assert card.fr is not None
    card.fr.choices.pop()
    issues = validate_cards([card])
    assert any("same number of choices" in issue.message for issue in issues)


def test_correct_index_must_align() -> None:
    card = make_mcq()
    assert card.fr is not None
    card.fr.choices[0].correct = True
    card.fr.choices[1].correct = False
    issues = validate_cards([card])
    assert any("same index" in issue.message for issue in issues)


def test_valid_collection_is_clean() -> None:
    assert validate_cards([make_mcq(), make_mcq(id="test-card-002")]) == []
