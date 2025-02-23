#!/usr/bin/env bash

# install pants
curl --proto '=https' --tlsv1.2 -sSfL https://pantsbuild.github.io/setup/get-pants.sh | bash

# export the virtualenvs for use in VSCode
pants export

# install pre-commit hooks
export PATH="/usr/local/py-utils/bin/pre-commit:$PATH"
pre-commit install --install-hooks
