#!/bin/sh
[ "$(checkimpcont.py < ./tests/contorted.py \
    | grep -o "warning: string literal concatenation" \
    | wc -l | tr -d '[:space:]')" = 10 ]
