#!/usr/bin/env bash
set -e

cd /app/tests
python run_basic_tests.py test
python run_pooled_tests.py test
python run_hiredis_tests.py test
python run_pooled_hiredis_tests.py test