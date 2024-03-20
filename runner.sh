#!/bin/bash
find . -regex ".*\.py" | entr poetry run pytest
