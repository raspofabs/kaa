import pytest
from pathlib import Path

def test_build_requirements(tmpdir):
    from kaa.sitter_util import build_library, fetch_source
    try:
        fetch_source(Path("not_here"), None)
    except FileNotFoundError:
        pass
    else:
        assert False

