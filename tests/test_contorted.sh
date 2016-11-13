#!/bin/sh
[ "$(checkimpcont.py < ./tests/contorted.py \
    | grep "shouldfind" | wc -l | tr -d '[:space:]')" = 7 ]
