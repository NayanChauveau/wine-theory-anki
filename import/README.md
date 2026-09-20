# Import

The source `.apkg` and the raw Front/Back extract are **not** published
(gitignored). Do **not** look in `~/Downloads`.

**Source deck:** `import/WSET_Level_3_--_NEW.apkg`  
(`src/wset3_anki/import_extract.py` → `default_apkg_path`)

1. That file is already in this folder. Re-extract with
   `uv run wset3-anki import-extract` (or `--apkg` only if you must override).
2. Convert notes from `inbox/cNN-….yaml` into the matching `cards/cNN-….yaml`,
   max 50 source notes per session, `status: draft` only.
3. Track EN work in `progress.yaml`. Quality (foils + FR sense):
   `quality-review.yaml`.

Agents continuing the English conversion: read [AGENT_PLAYBOOK.md](AGENT_PLAYBOOK.md)
(parent + parallel writers/critics). Card policy: `.cursor/rules/import.mdc`.

Study-card bar (EN and FR): same-class **credible** distractors — no cartoon
impossibles — French that **makes sense**, not a calque — and a keyed
choice that is **not** the obvious longest. Details in the
playbook section “Study-card quality”. Ledger for that pass:
[quality-review.yaml](quality-review.yaml) (not `progress.yaml`).
