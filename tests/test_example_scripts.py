from pathlib import Path

import pytest

from tfbscript import ScriptFile

SCRIPT_DIR = Path(__file__).parent.parent / "example_scripts"

scripts = list(SCRIPT_DIR.glob("**/*.ai"))


@pytest.mark.parametrize("script", scripts, ids=lambda p: p.name)
def test_parse_script(script: Path):
    ScriptFile.from_path(script, debugOptions={"listUnresolvedOps": True}).print_tree()