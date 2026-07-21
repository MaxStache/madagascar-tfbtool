from tfbscript import ScriptFile


ScriptFile.from_path("example_scripts/pr_zoovenir_master.ai", debugOptions={
    "listUnresolvedOps": True,
}).print_tree()