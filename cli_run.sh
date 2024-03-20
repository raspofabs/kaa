#!/bin/bash
find kaa/ | entr kaa_spc tests/test_data/multiple.cpp
# find kaa/ | entr kaa_spc tests/test_data/main.cpp
