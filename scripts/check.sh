#!/bin/sh
set -eu
python scripts/sync_bundles.py --check
pytest -q
