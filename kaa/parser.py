from tree_sitter import Language, Parser
import tree_sitter_python as tspython
from pathlib import Path
from kaa.sitter_util import get_language_cpp

def get_parser_cpp():
    CPP_LANGUAGE = get_language_cpp()
    if CPP_LANGUAGE is not None:
        parser = Parser()
        parser.set_language(CPP_LANGUAGE)
        return parser
    return None

def get_parser_python():
    PY_LANGUAGE = Language(tspython.language(), "python")
    parser = Parser()
    parser.set_language(PY_LANGUAGE)
    return parser
