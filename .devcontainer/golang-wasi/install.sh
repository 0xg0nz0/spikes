#!/bin/bash

# Use this local version of the script until this issue is resolved:
#
# https://github.com/dev-wasm/dev-wasm-feature/issues/13
#

set -e

# Determine the architecture of the Linux system
ARCH=$(uname -m)

# Sets the exact version to install, with a default and override
TINY_GO_VERSION="${VERSION:-"0.35.0"}"

# Set the URL of the binary to download based on the architecture
if [[ $ARCH == "x86_64" ]]; then
	TINY_GO_ARCH=amd64
elif [[ $ARCH == "arm64" || $ARCH == "aarch64" ]]; then
	TINY_GO_ARCH=arm64
else
	echo "Unsupported architecture: $ARCH"
	exit 1
fi
TINY_GO_DEB="tinygo_${TINY_GO_VERSION}_${TINY_GO_ARCH}.deb"
DOWNLOAD_URL="https://github.com/tinygo-org/tinygo/releases/download/v${TINY_GO_VERSION}/${TINY_GO_DEB}"

# Download and install the binary
curl ${DOWNLOAD_URL} -L --output ${TINY_GO_DEB} && \
    dpkg -i ${TINY_GO_DEB} && \
    rm ${TINY_GO_DEB}
