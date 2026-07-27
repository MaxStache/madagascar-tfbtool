from tfbscript import ScriptFile

ScriptFile.from_path(
    "example_scripts/RW_CrowdSpawned.ai",
    debugOptions={
        "listUnresolvedOps": True,
    },
).print_tree()
