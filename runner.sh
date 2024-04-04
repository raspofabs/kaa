#!/bin/bash
COVERAGE_PARAMS="--cov=kaa --no-cov-on-fail --cov-report term-missing --cov-branch --cov-report html tests/"
PYTEST_PARAMS="--durations=3"
find . -regex ".*\.py\|./tests/test_data/.*\.cpp" | entr poetry run pytest $PYTEST_PARAMS $COVERAGE_PARAMS ;
