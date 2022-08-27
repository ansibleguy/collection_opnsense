#!/bin/bash

set -e

echo ''

if [ -z "$1" ] || [ -z "$2" ]
then
  echo 'Arguments:'
  echo '  1: firewall'
  echo '  2: api key file'
  echo '  3: path to virtual environment (optional)'
  echo ''
  exit 1
else
  export TEST_FIREWALL="$1"
  export TEST_API_KEY="$2"
fi

if [ -n "$3" ]
then
  source "$3/bin/activate"
fi

cd "$(dirname "$0")/.."
rm -rf "~/.ansible/collections/ansible_collections/ansibleguy/opnsense"
ansible-galaxy collection install git+https://github.com/ansibleguy/collection_opnsense.git

echo ''
echo 'RUNNING CLEANUP'
echo ''

ansible-playbook tests/cleanup.yml --extra-vars="ansible_python_interpreter=$(which python)"

rm -rf "~/.ansible/collections/ansible_collections/ansibleguy/opnsense"

echo ''
echo 'FINISHED CLEANUP!'
echo ''
