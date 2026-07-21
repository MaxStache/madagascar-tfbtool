from pathlib import Path

folder = Path("example_scripts")

OP_CODE = b"loop value"

for file in folder.rglob("*.ai"):
    data = file.read_bytes()
    count = data.count(OP_CODE + b"::op-code")

    if count:
        print(f"{file}: {count}")