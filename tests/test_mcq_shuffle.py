"""Run the shipped JavaScript, including front/back state and the legacy Droid API."""

import shutil
import subprocess
from pathlib import Path

from wset3_anki.build import load_models

ROOT = Path(__file__).resolve().parents[1]


def test_mcq_shuffle_behavior():
    node = shutil.which("node")
    assert node, "Node.js is required to verify the card JavaScript (node --test)."
    result = subprocess.run(
        [node, "--test", str(ROOT / "tests/js/mcq-shuffle.test.cjs")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_monolingual_and_bilingual_models_use_the_same_shuffle():
    models = load_models(ROOT / "templates")
    for name in ("mcq", "mcq-bilingual"):
        for template in models[name].templates:
            assert "wset3ShuffleChoices(false)" in template["qfmt"]
            assert "wset3ShuffleChoices(true)" in template["afmt"]
            assert "function wset3RandomOrder(n)" in template["qfmt"]
            assert "function wset3RandomOrder(n)" in template["afmt"]
