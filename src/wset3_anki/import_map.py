from __future__ import annotations

import re
from dataclasses import dataclass

CHAPTER_RE = re.compile(r"C(\d+)", re.IGNORECASE)


@dataclass(frozen=True)
class ChapterTarget:
    slug: str
    inbox_name: str
    deck: str
    publish: bool = True

    @property
    def cards_file(self) -> str:
        return self.inbox_name if self.publish else ""


# Source Cxx decks → inbox / cards filename (same) / deck key.
CHAPTERS: dict[int, ChapterTarget] = {
    6: ChapterTarget("c06", "c06-vineyard-management.yaml", "Vineyard Management"),
    7: ChapterTarget("c07", "c07-winemaking-and-maturation.yaml", "Winemaking and Maturation"),
    8: ChapterTarget("c08", "c08-white-and-sweet-winemaking.yaml", "White and Sweet Winemaking"),
    9: ChapterTarget("c09", "c09-red-and-rose-winemaking.yaml", "Red and Rosé Winemaking"),
    10: ChapterTarget("c10", "c10-price-of-wine.yaml", "Price of Wine"),
    11: ChapterTarget("c11", "c11-wine-and-the-law.yaml", "Wine and the Law"),
    12: ChapterTarget("c12", "c12-france-introduction.yaml", "France"),
    13: ChapterTarget("c13", "c13-bordeaux.yaml", "France::Bordeaux"),
    14: ChapterTarget("c14", "c14-south-west.yaml", "France::South West"),
    15: ChapterTarget("c15", "c15-burgundy.yaml", "France::Burgundy"),
    16: ChapterTarget("c16", "c16-beaujolais.yaml", "France::Beaujolais"),
    17: ChapterTarget("c17", "c17-alsace.yaml", "France::Alsace"),
    18: ChapterTarget("c18", "c18-loire.yaml", "France::Loire"),
    19: ChapterTarget("c19", "c19-northern-rhone.yaml", "France::Northern Rhône"),
    20: ChapterTarget("c20", "c20-southern-rhone.yaml", "France::Southern Rhône"),
    21: ChapterTarget("c21", "c21-southern-france.yaml", "France::Southern France"),
    22: ChapterTarget("c22", "c22-germany.yaml", "Germany"),
    23: ChapterTarget("c23", "c23-austria.yaml", "Austria"),
    24: ChapterTarget("c24", "c24-tokaj.yaml", "Hungary::Tokaj"),
    25: ChapterTarget("c25", "c25-greece.yaml", "Greece"),
    26: ChapterTarget("c26", "c26-italy-introduction.yaml", "Italy"),
    27: ChapterTarget("c27", "c27-northern-italy.yaml", "Italy::Northern Italy"),
    28: ChapterTarget("c28", "c28-central-italy.yaml", "Italy::Central Italy"),
    29: ChapterTarget("c29", "c29-southern-italy.yaml", "Italy::Southern Italy"),
    30: ChapterTarget("c30", "c30-spain.yaml", "Spain"),
    31: ChapterTarget("c31", "c31-portugal.yaml", "Portugal"),
    32: ChapterTarget("c32", "c32-usa-introduction.yaml", "USA"),
    33: ChapterTarget("c33", "c33-california.yaml", "USA::California"),
    34: ChapterTarget("c34", "c34-pacific-northwest.yaml", "USA::Pacific Northwest"),
    35: ChapterTarget("c35", "c35-canada.yaml", "Canada"),
    36: ChapterTarget("c36", "c36-chile.yaml", "Chile"),
    37: ChapterTarget("c37", "c37-argentina.yaml", "Argentina"),
    38: ChapterTarget("c38", "c38-south-africa.yaml", "South Africa"),
    39: ChapterTarget("c39", "c39-australia.yaml", "Australia"),
    40: ChapterTarget("c40", "c40-new-zealand.yaml", "New Zealand"),
    41: ChapterTarget("c41", "c41-sparkling-production.yaml", "Sparkling Production"),
    42: ChapterTarget("c42", "c42-sparkling-wines.yaml", "Sparkling Wines"),
    43: ChapterTarget("c43", "c43-sherry.yaml", "Sherry"),
    44: ChapterTarget("c44", "c44-port.yaml", "Port"),
    45: ChapterTarget("c45", "c45-fortified-muscat.yaml", "Fortified Muscat"),
}

ROOT_TARGETS: dict[str, ChapterTarget] = {
    "sat": ChapterTarget("c01", "c01-sat.yaml", "SAT"),
    "food": ChapterTarget("c02", "c02-wine-with-food.yaml", "Wine with Food"),
    "vine": ChapterTarget("c03", "c03-the-vine.yaml", "The Vine"),
    "climate": ChapterTarget("c04", "c04-growing-environment.yaml", "The Growing Environment"),
    "unclassified": ChapterTarget("c00", "c00-unclassified.yaml", "", publish=False),
}

# Independently researched chapters with no matching Cxx deck in the legacy import.
SUPPLEMENTARY_TARGETS: tuple[ChapterTarget, ...] = (
    ChapterTarget("c46", "c46-jura.yaml", "France::Jura"),
    ChapterTarget("c47", "c47-savoie.yaml", "France::Savoie"),
)

UNCLASSIFIED = ROOT_TARGETS["unclassified"]


def published_targets() -> list[ChapterTarget]:
    return [
        target
        for target in (*CHAPTERS.values(), *ROOT_TARGETS.values(), *SUPPLEMENTARY_TARGETS)
        if target.publish
    ]


def target_from_deck_name(name: str) -> ChapterTarget | None:
    match = CHAPTER_RE.search(name)
    if not match:
        return None
    return CHAPTERS.get(int(match.group(1)))


def classify_root_text(front: str, back: str, tags: str = "") -> ChapterTarget:
    blob = f"{tags} {front} {back}".lower()
    if "c1_sat" in blob or any(
        word in blob
        for word in (
            "sat",
            "tasting",
            "appearance",
            "medium (+)",
            "medium (-)",
            "palate",
            "rim",
            "core of the bowl",
        )
    ):
        return ROOT_TARGETS["sat"]
    if any(word in blob for word in ("pairing", "food and wine", "wine with food", "dish")):
        return ROOT_TARGETS["food"]
    if any(
        word in blob
        for word in (
            "budburst",
            "bud burst",
            "véraison",
            "veraison",
            "flowering",
            "fruit set",
            "vitis",
            "graft",
            "rootstock",
            "photosynthesis",
            "vine's",
            "vine ",
        )
    ):
        return ROOT_TARGETS["vine"]
    if any(
        word in blob
        for word in (
            "climate",
            "weather",
            "latitude",
            "altitude",
            "ocean current",
            "aspect",
            "fog",
            "rainfall",
            "continentality",
        )
    ):
        return ROOT_TARGETS["climate"]
    return UNCLASSIFIED
