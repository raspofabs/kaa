from tree_sitter import Language, Parser
from pathlib import Path
from kaa.sitter_util import get_language_cpp

def get_parser_cpp():
    CPP_LANGUAGE = get_language_cpp()
    if CPP_LANGUAGE is not None:
        parser = Parser()
        parser.set_language(CPP_LANGUAGE)
        return parser
    return None
