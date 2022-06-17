#!/usr/bin/env bash

set -env

if [[ "$CHART_NAME" && "$BUMP_STRATEGY" ]]; then
    python -c 'from auto_bump import main; main.main()'
fi

exit 0;