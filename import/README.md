# Import

The source `.apkg` and the raw Front/Back extract are **not** published.

1. Copy `WSET_Level_3_--_NEW.apkg` into this folder (gitignored).
2. Run `uv run wset3-anki import-extract`.
3. Convert notes from `inbox/cNN-….yaml` into the matching `cards/cNN-….yaml`, max 50 source notes per session, `status: draft` only.
4. Track work in `progress.yaml`.

Agents continuing the English conversion: read [AGENT_PLAYBOOK.md](AGENT_PLAYBOOK.md)
(parent + parallel writers/critics). Card policy: `.cursor/rules/import.mdc`.

Study-card bar (EN and FR): same-class **credible** distractors — no cartoon
impossibles — and French that **makes sense**, not a calque. Details in the
playbook section “Study-card quality”.
