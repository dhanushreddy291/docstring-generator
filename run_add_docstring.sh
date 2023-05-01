#!/bin/bash
for file in $(find . -name "*.py")
do
    python add_docstring.py $file
done
