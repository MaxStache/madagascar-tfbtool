from tfbscript import ScriptFile


ScriptFile.from_path("example_scripts/ME_BAllo0ns_floating.ai", debugOptions={
    "listUnresolvedOps": True,
}).print_tree()