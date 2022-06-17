#!/usr/bin/env bash

set -env

python -c 'from auto_bump import main; main.main()'

exit 0;