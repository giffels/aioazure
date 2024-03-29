#!/bin/bash
PROJECT=aioazure

source ../venv/bin/activate
sphinx-apidoc --force --module-first --separate -o source/api ../${PROJECT} && \
make html && \
open _build/html/index.html
