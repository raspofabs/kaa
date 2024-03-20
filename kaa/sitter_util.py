from tree_sitter import Language, Parser
from pathlib import Path


def fetch_source(source_root, git_repo_url):
    if not source_root.is_dir():
        import subprocess
        if git_repo_url is not None:
            subprocess.run(["git", "clone", git_repo_url, source_root])
    if not source_root.is_dir():
        raise FileNotFoundError(f"unable to fetch source for {git_repo_url} into {source_root}")


def build_library(): 
    tree_sitter_cpp_root = Path("vendor/tree-sitter-cpp")
    fetch_source(tree_sitter_cpp_root, "https://github.com/tree-sitter/tree-sitter-cpp")
    Language.build_library(
        # Store the library in the `build` directory
        "build/my-languages.so",
        # Include one or more languages
        [tree_sitter_cpp_root],
    )

def get_library():
    library_file = Path("build/my-languages.so")
    if not library_file.is_file():
        build_library()
    if library_file.is_file():
        return str(library_file)
    return None


def get_language_cpp():
    library_file = get_library()
    if library_file is not None:
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter(action='ignore', category=FutureWarning)
            return Language(library_file, "cpp")
    return None

