#!/usr/bin/env bash

set -e

cd "$(dirname "$0")/.."

echo ''
echo 'BUILDING tarball'
echo ''

rm -f ansibleguy-opnsense-*.tar.gz
ansible-galaxy collection build
