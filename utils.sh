#!/bin/bash
rm tags
ctags -R --exclude="**/.mypy_cache/*" --exclude="**/__pycache__/*" src lib/langtools/
