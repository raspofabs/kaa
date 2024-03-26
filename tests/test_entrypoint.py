import pytest
from click.testing import CliRunner
from kaa.entrypoint import run

def test_running():
    runner = CliRunner()
    result = runner.invoke(run, ["-v", "tests/test_data/one_if.cpp"])
    assert result.exit_code == 0
    assert "one_if" in result.output
    assert "number_literal" in result.output

def test_non_verbose():
    runner = CliRunner()
    result = runner.invoke(run, ["tests/test_data/simple.cpp"])
    assert result.exit_code == 0
    assert "SPC of hello" in result.output
    assert "number_literal" not in result.output
