from tfbscript import ScriptFile


ScriptFile.from_path("example_scripts/Melman_RunAsPlayer.ai", debugOptions={
    "listUnresolvedOps": True,
}).print_tree()