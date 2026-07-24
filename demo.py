from tfbscript import ScriptFile


ScriptFile.from_path("example_scripts/ME_Pigeon.ai", debugOptions={
    "listUnresolvedOps": True,
}).print_tree()