#!/bin/bash

set -e

# Determine the architecture of the Linux system
ARCH=$(uname -m)

# Sets the exact version to install, with a default and override
VERSION=${VERSION:-"2.33.0"}

# Set the URL of the binary to download based on the architecture
if [[ $ARCH == "x86_64" ]]; then
	DOWNLOAD_URL="https://github.com/rui314/mold/releases/download/v${VERSION}/mold-${VERSION}-x86_64-linux.tar.gz"
elif [[ $ARCH == "arm64" || $ARCH == "aarch64" ]]; then
	DOWNLOAD_URL="https://github.com/rui314/mold/releases/download/v${VERSION}/mold-${VERSION}-aarch64-linux.tar.gz"
else
	echo "Unsupported architecture: $ARCH"
	exit 1
fi

# Download and install the binary
curl --silent --show-error --remove-on-error --retry 3 --location "$DOWNLOAD_URL" -o mold.tar.gz &&
	tar xzvf mold.tar.gz &&
	cp -r mold-*/* /usr/local &&
	rm -rf mold-* mold.tar.gz
