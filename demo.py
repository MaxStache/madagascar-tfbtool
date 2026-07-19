from tfbscript import ScriptFile


ScriptFile.from_path("example_scripts/DG_Coin_Collectable.ai", debugOptions={
    "listUnresolvedOps": True,
}).print_tree()