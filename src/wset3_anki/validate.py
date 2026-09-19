from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from wset3_anki.schema import Card, McqCard


@dataclass(frozen=True)
class ValidationIssue:
    card_id: str | None
    message: str

    def __str__(self) -> str:
        if self.card_id:
            return f"{self.card_id}: {self.message}"
        return self.message


def validate_cards(cards: list[Card]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    counts = Counter(card.id for card in cards)
    for card_id, count in sorted(counts.items()):
        if count > 1:
            issues.append(ValidationIssue(card_id, f"duplicate id ({count} occurrences)"))

    for card in cards:
        if isinstance(card, McqCard) and card.fr is not None:
            if len(card.fr.choices) != len(card.en.choices):
                issues.append(
                    ValidationIssue(
                        card.id,
                        "fr must have the same number of choices as en "
                        f"({len(card.fr.choices)} != {len(card.en.choices)})",
                    )
                )
                continue
            en_correct = [i for i, choice in enumerate(card.en.choices) if choice.correct]
            fr_correct = [i for i, choice in enumerate(card.fr.choices) if choice.correct]
            if en_correct != fr_correct:
                issues.append(
                    ValidationIssue(
                        card.id,
                        "the correct choice must be at the same index in en and fr",
                    )
                )
    return issues
