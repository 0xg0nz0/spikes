#!/usr/bin/env bash

# install pre-commit hooks
export PATH="/usr/local/py-utils/bin/pre-commit:$PATH"
pre-commit install --install-hooks
