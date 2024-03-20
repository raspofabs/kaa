#!/bin/bash
find . -regex ".*\.py" | entr poetry run pytest --cov=kaa --no-cov-on-fail --cov-report term --cov-branch --cov-report html  tests/;
