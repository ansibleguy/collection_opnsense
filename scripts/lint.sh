#!/usr/bin/env bash

set -e

cd "$(dirname "$0")/.."

echo ''
echo 'LINTING Python'
echo ''

pylint --recursive=y .

echo ''
echo 'LINTING Yaml'
echo ''
yamllint .

echo ''
echo 'LINTING Ansible'
echo ''
TMP_COL_DIR='/tmp/ansible_lint/collections'
mkdir -p "$TMP_COL_DIR/ansible_collections/ansibleguy"
ln -s "$(pwd)" "$TMP_COL_DIR/ansible_collections/ansibleguy/opnsense"
ANSIBLE_COLLECTIONS_PATH="$TMP_COL_DIR" ansible-lint -c .ansible-lint.yml
rm -rf "$TMP_COL_DIR"

echo ''
echo 'FINISHED LINTING!'
echo ''
