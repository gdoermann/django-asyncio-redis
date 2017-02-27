#!/usr/bin/env bash
set -e

cd /app/tests
python run_pooled_tests.py test
