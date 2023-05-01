#!/bin/bash
for file in $(find . -name "add_docstring.py" -prune -o -name "*.py" -print)
do
    python add_docstring.py $file
done
