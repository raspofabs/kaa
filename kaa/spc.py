from pathlib import Path

def read_source(source_file: Path):
    with open(source_file,"rb") as fh:
        return fh.read()
    return bytes("","utf8")
