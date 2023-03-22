#!/bin/bash
#
# Validate that the repository has the following structure:
# -- README.md
# -- main.tf

failed=0
for file in README.md main.tf; do
    if [ ! -f "$file" ]; then
        echo "FAIL: Missing $file"
        failed=1
    fi
done

if [ $failed -eq 1 ]; then
    echo "Repository structure is not valid. Please fix the errors above."
    exit 1
fi

