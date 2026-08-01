from tfbscript import ScriptFile
from tfbscript import open_editor
from contextlib import redirect_stdout

script = ScriptFile.from_path(
    #"PR_Pause_{0974a777-cf50-4185-857d-810db4807d9a}.ai.mod",
    "example_scripts/Alex_RunAsPlayer.ai",
    debugOptions={
        "listUnresolvedOps": True,
    },
)

with open("log.txt", "w", encoding="utf-8") as f, redirect_stdout(f):
    script.print_tree()


open_editor(script)

#with open("PR_Pause_{0974a777-cf50-4185-857d-810db4807d9a}.ai.mod", "wb") as f:
#   script.write(f)