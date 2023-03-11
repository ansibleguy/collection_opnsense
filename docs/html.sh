#!/usr/bin/env bash

cd "$(dirname "$0")"

rm -rf build
mkdir build

sphinx-build -b html source/ build/
