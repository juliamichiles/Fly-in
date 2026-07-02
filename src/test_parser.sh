#!/bin/bash
find ../maps/invalid/ -type f -exec sh -c '
    f=${1##*/}
    f=${f%.txt}
    echo "\n=== File: $f ==="
    ./parser.py "$1"
' _ {} \;
