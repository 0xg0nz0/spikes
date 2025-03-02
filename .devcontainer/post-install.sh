#!/usr/bin/env bash

# install Bazel CLI tools
go install github.com/bazelbuild/buildtools/buildifier@latest
go install github.com/bazelbuild/buildtools/buildozer@latest

# install the Iggy Docker image
docker pull iggyrs/iggy:latest

# install pre-commit hooks
export PATH="/usr/local/py-utils/bin/pre-commit:$PATH"
pre-commit install --install-hooks
