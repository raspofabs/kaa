#!/bin/bash
COVERAGE_PARAMS="--cov=kaa --no-cov-on-fail --cov-report term --cov-branch --cov-report html tests/"
PYTEST_PARAMS="--durations=3"
find . -regex ".*\.py" | entr poetry run pytest $PYTEST_PARAMS $COVERAGE_PARAMS ;
