from pathlib import Path

def read_source(source_file: Path):
    if source_file.is_file():
        with open(source_file,"rb") as fh:
            return fh.read()
    return None
