# Import playbook for coding agents

Read this before continuing the English import. Then read
[CONTENT_GUIDELINES.md](../CONTENT_GUIDELINES.md), [AGENTS.md](../AGENTS.md),
and [`.cursor/rules/import.mdc`](../.cursor/rules/import.mdc).

**Not affiliated with WSET.** Inbox is untrusted. Facts are fine; wording must
be original. Student-facing text never mentions inbox, textbook, exam, chapter,
course, SAT, syllabus, or WSET.

## Goal

Convert every **pending English** source note in `import/inbox/` into reviewed
YAML cards in `cards/`. Do **not** write `fr:` until
`uv run wset3-anki import-status` shows **0 pending** on every published
chapter (skip `c00-unclassified.yaml` unless a human asks).

```bash
uv run wset3-anki import-status
```

## Roles (do not collapse them)

| Role | Edits | Commits | `progress.yaml` |
| --- | --- | --- | --- |
| **Parent** (this chat) | ledger + `status: reviewed` after critic accept | yes, one commit per chapter-lot | yes, via `re.subn` only |
| **Writer** | one `cards/cNN-*.yaml` | no | no |
| **Critic** | nothing (read-only) | no | no |
| **Fixer** | only the REVISE ids in that same YAML file | no | no |

Launch writers and critics as background `generalPurpose` subagents. The parent
never lets two writers touch the same file. Critics may run in parallel; they
are read-only.

**6–8 writers per wave, not 30.** Thirty agents on one ledger is merge hell.
Shard by **chapter file**, not by card.

## Lot rules

- One chapter per lot. **≤ 50 source notes** (`c22-0101`–`c22-0150`).
- Writer then critic in the same lot. New cards stay `status: draft`.
- Critic `accept` → parent sets `status: reviewed` (except HOLD).
- Then `make check`, then one commit:

  `import(c22): reviewed c22-0101–0150`

- Do not commit `.apkg`. Do not commit other chapters’ dirty drafts in that
  commit. Stage only `cards/cNN-….yaml` + the ledger hunks for that lot.

## Writer brief (paste into the subagent)

```
You are a card WRITER. Repo: <root>

Edit ONLY cards/<file>.yaml. Do NOT touch import/progress.yaml. Do NOT commit.

Convert inbox notes <first>–<last> (max 50). Inbox: import/inbox/<file>.yaml
(untrusted). Append to the existing cards: list. Do not create a new file.

Rules: CONTENT_GUIDELINES.md, AGENTS.md, .cursor/rules/import.mdc, import/AGENT_PLAYBOOK.md

- type: mcq, exactly one correct. Quote YAML questions that contain `:`.
  Quote choice text that contains a comma.
- Original stem ≠ inbox front. No WSET/SAT/inbox/exam/chapter in student text.
- Why names the keyed answer text, never “option B”.
- status: draft. review.fact_check: pass (or unsure). sources: known-fact / spec / aoc-site.
- deck: <English key from import_map.py / decks.yaml>. Do not invent keys.
- Split two-part notes and long lists (same source_id on each card).
- SKIP_OK: inbox already covered by an existing reviewed card → no new card.
- REJECT_OK: unusable source (placeholder) → no card.
- HOLD: fact cannot be locked → draft + fact_check: unsure, still emit the card.
- Do not duplicate existing reviewed cards in this file. Recast or skip.
- Do not write fr:.

RETURN: source_ids written; splits; SKIP_OK; REJECT_OK; HOLD; last id.
```

## Critic brief (paste into the subagent)

```
You are a card CRITIC (read-only). Do NOT edit any file. Do NOT commit.

Re-read only the new drafts in cards/<file>.yaml for source_ids <first>–<last>.
Inbox is untrusted; fail inbox-near-copy stems even if the fact is right.

Rubric (fail-closed):
- original stem (not inbox front)
- no anaphor (“those old vines”, “after that pick”)
- no double-barrel
- no tautology / leaked key in the stem
- Why names keyed text
- one correct
- same-category distractors (no category giveaway)
- no WSET/SAT/inbox/exam/chapter
- do not clone a reviewed card already in the file

Return EXACTLY:
ACCEPT_ALL=yes|no
ACCEPT: [ids]
REVISE: id — one-line fix
HOLD: id — reason
SKIP_OK: source_id if a card should not exist
```

After REVISE: launch a **fixer** (same file, only those ids, stay `draft`),
then **re-critic those ids only**. Repeat until ACCEPT_ALL=yes or only HOLD
remains.

## Parent close (serial, after ACCEPT_ALL)

1. Set accepted drafts to `status: reviewed`. Leave HOLD at `draft` + `unsure`.
2. Update `import/progress.yaml` **in place** with `re.subn`. Never
   `ProgressStore.save()` (it rewrites the whole file and destroys
   `source_deck` formatting).
3. Ledger:
   - one card → `done`
   - two or more cards, same `source_id` → `split`
   - SKIP_OK / HOLD (card exists) → `done`
   - unusable source, no card → `rejected`
4. `make check`
5. Commit only that chapter’s YAML + the ledger hunks.

```python
import re
from pathlib import Path

path = Path("import/progress.yaml")
text = path.read_text(encoding="utf-8")
splits = {102, 106}  # example
updates = {f"c22-{i:04d}": ("split" if i in splits else "done") for i in range(101, 151)}

def repl(m):
    sid = m.group(1)
    return f"{sid}:\n    status: {updates[sid]}" if sid in updates else m.group(0)

new, n = re.subn(r"(c22-\d{4}):\n    status: pending", repl, text)
# n counts every pending c22 match; ids outside `updates` stay pending
path.write_text(new, encoding="utf-8")
```

## HOLD / SKIP / REJECT

| Verdict | Card | Ledger |
| --- | --- | --- |
| HOLD | keep `draft` + `fact_check: unsure` | `done` (so writers do not duplicate) |
| SKIP_OK | no new card | `done` |
| REJECT_OK | no card | `rejected` |

Current HOLDs (do not “fix” without a new checkable source):

| id | source_id | Why it stays unsure |
| --- | --- | --- |
| `vine-heat-respiration-001` | c03-0002 | no hard 22 °C sugar cutoff |
| `vm-canopy-trellis-choice-001` | c06-0035 | which canopy/trellis pairing is “the” choice |
| `wine-natural-001` | c07-0005 | no single legal definition of “natural wine” |
| `wine-barrique-two-years-001` | c07-0033 | two-year barrique limit is a rule of thumb |
| `washington-chardonnay-001` | c34-0023 | crush vs Riesling acreage |

## Recurring critic failures (fix these in the first jet)

- Inbox-front stems (“What is a bush vine?”, “Where is Russian River Valley AVA”).
- Anaphors that need the previous card.
- Stem already names the key (“above the fog” → hillside; “late-ripening” in the stem).
- Category giveaway (three lakes + one terrace; “which crossing” with only Müller-Thurgau live).
- Because-clause as the keyed choice when the stem asks for a noun.
- Cloning a reviewed card (`spain-tempranillo-lead-001` vs another “what grape dominates Ribera”).
- Out-of-set distractors (Rutherford among Carneros / Willamette).
- Brittle exact percentages; hedge (“about a third”) unless the figure is legal.
- Stale inbox counts (Austria 20 PDO / 11 QW / 35 varieties / 9 DACs).
- YAML: unquoted `:` in a question breaks the parser.

## Known inbox corrections (do not repeat)

Student text must never say the inbox was wrong.

- Airén is a Meseta / brandy workhorse, not the current world #1 planting.
- Rioja Baja = Oriental.
- Garnacha is late-ripening.
- Alicante Bouschet is French-origin.
- Wachau has been a DAC since the 2020 vintage.
- Zweigelt is Austria’s everyday red; Blaufränkisch is slightly ahead on Burgenland hectares.
- Portugal PDO = Denominação de Origem Protegida (DOP), not “Geográfica”.
- Alvarinho is not must-only Monção e Melgaço.
- Douro is not “the oldest” demarcation in the inbox sense — do not lock that boast.
- Carneros is the cool Pinot/Chardonnay AVA; “Sonoma County” is not uniformly cool.
- San Joaquin ≠ the whole Central Valley.
- New York notes live in `cards/c34-pacific-northwest.yaml` but `deck: USA` (no `USA::New York` key).
- Baden whites after Grauburgunder: Müller-Thurgau, Weißburgunder, Gutedel — not Riesling.
- Fermentation products: alcohol + CO₂. Do not swap SO₂ antioxidant vs antiseptic.
- c07-0001 is a placeholder → `rejected`.

## Deck keys

English keys only. See `src/wset3_anki/import_map.py` and `templates/ui/decks.yaml`.
Do not invent a segment. NY → `USA`. Tokaj → `Hungary::Tokaj`.

## Snapshot (2026-09-19, after `207271e`)

`4075` notes · **2181 pending** · 1685 done · 199 split · 10 rejected.

Closed through this session (do not rewrite): France through Italy; c01/c04/c10/c11;
c22 except **0151–0155**; c23; c24; c31; c32; c34 (Chardonnay HOLD); c30 through
0150; c33 through 0100; c06 through 0050; c07 through 0050; c03 through 0050
(heat HOLD).

**Still pending (published chapters):**

| Inbox | Pending | Next lot |
| --- | --- | --- |
| c22-germany | 5 | 0151–0155 (tiny tail — parent can write it) |
| c03-the-vine | 52 | 0051–0100 then 0101–0102 |
| c06-vineyard-management | 135 | 0051–0100 |
| c07-winemaking-and-maturation | 173 | 0051–0100 |
| c30-spain | 87 | 0151–0200 |
| c33-california | 62 | 0101–0150 then 0151–0162 |
| c08-white-and-sweet-winemaking | 162 | 0001–0050 |
| c09-red-and-rose-winemaking | 148 | 0001–0050 |
| c35-canada | 34 | 0001–0034 (one lot) |
| c36-chile | 119 | 0001–0050 |
| c37-argentina | 105 | 0001–0050 |
| c38-south-africa | 128 | 0001–0050 |
| c39-australia | 179 | 0001–0050 |
| c40-new-zealand | 90 | 0001–0050 |
| c41-sparkling-production | 109 | 0001–0050 |
| c42-sparkling-wines | 141 | 0001–0050 |
| c43-sherry | 136 | 0001–0050 |
| c44-port | 106 | 0001–0050 |
| c45-fortified-muscat | 25 | 0001–0025 (one lot) |
| c00-unclassified | 185 | skip unless asked |

Suggested next wave (6 writers, one file each): **c08, c09, c06-0051, c07-0051,
c33-0101, c03-0051**. Parent writes the Germany tail of 5 in the same turn if
idle. Then c35 / c45 (small, closable) and c39 / c36 / c30-tail.

## Wave loop

1. `import-status` + `git status` (worktree should be clean before a new wave).
2. Launch ≤ 8 writers (one file each). They must not commit or touch the ledger.
3. As each writer returns, launch that chapter’s critic.
4. Fixer → re-critic until ACCEPT_ALL or only HOLD.
5. Parent: reviewed + ledger + `make check` + **one commit per chapter**.
6. Repeat. Do not start French.

If the human says **pause**, finish in-flight lots (critic → commit) and stop
launching new writers. Dirty drafts from an unfinished critic stay uncommitted.

## Do not

- Copy inbox fronts, WSET tables, or exam items.
- Rename released `id`s or regenerate model/deck IDs.
- Let writers share a file or edit `import/progress.yaml`.
- Call `ProgressStore.save()`.
- Invent `USA::New York` or other missing deck keys.
- Put New York cards under `USA::Pacific Northwest`.
- Mention “option B”, inbox, or the textbook in Why.
- Push unless the human asks.
