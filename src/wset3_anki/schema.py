from __future__ import annotations

import re
from enum import StrEnum
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, TypeAdapter, field_validator, model_validator

CARD_ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)+$")
CARD_ID_PATTERN = r"^[a-z0-9]+(?:-[a-z0-9]+)+$"


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Status(StrEnum):
    DRAFT = "draft"
    REVIEWED = "reviewed"
    NEEDS_TRANSLATION = "needs-translation"


class Choice(StrictModel):
    text: str = Field(min_length=1, description="Choice text shown on the card")
    correct: bool = Field(default=False, description="Exactly one choice per language must be true")


class McqContent(StrictModel):
    question: str = Field(min_length=1, description="Question stem; Markdown allowed")
    choices: list[Choice] = Field(min_length=2, max_length=10)
    explanation: str = Field(
        min_length=1,
        description="Why the answer is correct. Name the answer text, never a letter.",
    )

    @model_validator(mode="after")
    def exactly_one_correct(self) -> McqContent:
        n_correct = sum(1 for choice in self.choices if choice.correct)
        if n_correct != 1:
            raise ValueError(f"MCQ must have exactly one correct choice, found {n_correct}")
        return self


class BasicContent(StrictModel):
    front: str = Field(min_length=1, description="Prompt")
    back: str = Field(min_length=1, description="Answer")


class ClozeContent(StrictModel):
    text: str = Field(min_length=1, description="Text containing at least one {{c1::...}} deletion")
    extra: str = Field(default="", description="Optional extra shown on the back")

    @field_validator("text")
    @classmethod
    def has_cloze(cls, value: str) -> str:
        if "{{c" not in value:
            raise ValueError("cloze text must contain at least one {{cN::...}} deletion")
        return value


class CardBase(StrictModel):
    id: str = Field(
        pattern=CARD_ID_PATTERN,
        description="Permanent lowercase kebab-case id. Never rename after release.",
        examples=["sat-acidity-001"],
    )
    deck: str = Field(
        min_length=1,
        description="Anki subdeck path under 'WSET 3 VIN::', e.g. France::Bordeaux",
        examples=["SAT", "France::Bordeaux"],
    )
    tags: list[str] = Field(default_factory=list, description="Extra Anki tags")
    status: Status = Field(
        default=Status.REVIEWED,
        description="draft is omitted from release builds",
    )

    @field_validator("id")
    @classmethod
    def validate_id(cls, value: str) -> str:
        if not CARD_ID_RE.match(value):
            raise ValueError(
                f"id {value!r} must be lowercase kebab-case with at least one hyphen "
                "(e.g. sat-appearance-001)"
            )
        return value

    @field_validator("deck")
    @classmethod
    def validate_deck(cls, value: str) -> str:
        parts = [part.strip() for part in value.split("::")]
        if not all(parts):
            raise ValueError("deck path must not contain empty segments")
        return "::".join(parts)


class McqCard(CardBase):
    type: Literal["mcq"] = "mcq"
    en: McqContent
    fr: McqContent | None = None


class BasicCard(CardBase):
    type: Literal["basic"] = "basic"
    en: BasicContent
    fr: BasicContent | None = None


class ClozeCard(CardBase):
    type: Literal["cloze"] = "cloze"
    en: ClozeContent
    fr: ClozeContent | None = None


Card = Annotated[McqCard | BasicCard | ClozeCard, Field(discriminator="type")]
CardAdapter: TypeAdapter[McqCard | BasicCard | ClozeCard] = TypeAdapter(Card)


class CardFile(StrictModel):
    cards: list[Card] = Field(default_factory=list, description="Cards in this chapter")
