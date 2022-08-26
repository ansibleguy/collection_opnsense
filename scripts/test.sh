#!/bin/bash

set -e

if [ -n "$1" ]
then
  source "$1"
fi

cd "$(dirname "$0")/.."
rm -rf '~/.ansible/collections/ansible_collections/ansibleguy/opnsense'
ansible-galaxy collection install git+https://github.com/ansibleguy/collection_opnsense.git

echo ''
echo 'RUNNING TESTS for module ALIAS'
echo ''

ansible-playbook -D tests/alias.yml

echo ''
echo 'FINISHED TESTS!'
echo ''
