#!/bin/bash

set -e

echo ''

DEBUG=false

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

if [[ "$DEBUG" == true ]]
then
  VERBOSITY='-D -vvv'
else
  VERBOSITY=''
fi

cd "$(dirname "$0")/.."
rm -rf "~/.ansible/collections/ansible_collections/ansibleguy/opnsense"
ansible-galaxy collection install git+https://github.com/ansibleguy/collection_opnsense.git

echo ''
echo '##############################'
echo 'STARTING TESTS!'
echo '##############################'
echo ''

echo ''
echo '##############################'
echo 'RUNNING TESTS for module ALIAS'
echo ''

ansible-playbook tests/alias.yml --extra-vars="ansible_python_interpreter=$(which python)" $VERBOSITY
ansible-playbook tests/alias.yml --check --extra-vars="ansible_python_interpreter=$(which python)" $VERBOSITY

echo ''
echo '##############################'
echo 'RUNNING TESTS for module ALIAS_MULTI'
echo ''

ansible-playbook tests/alias_multi.yml --extra-vars="ansible_python_interpreter=$(which python)" $VERBOSITY
ansible-playbook tests/alias_multi.yml --check --extra-vars="ansible_python_interpreter=$(which python)" $VERBOSITY

echo ''
echo '##############################'
echo 'RUNNING TESTS for module ALIAS_PURGE'
echo ''

ansible-playbook tests/alias_purge.yml --extra-vars="ansible_python_interpreter=$(which python)" $VERBOSITY
ansible-playbook tests/alias_purge.yml --check --extra-vars="ansible_python_interpreter=$(which python)" $VERBOSITY

echo ''
echo '##############################'
echo 'RUNNING TESTS for module RULE'
echo ''

ansible-playbook tests/rule.yml --extra-vars="ansible_python_interpreter=$(which python)" $VERBOSITY
ansible-playbook tests/rule.yml --check --extra-vars="ansible_python_interpreter=$(which python)" $VERBOSITY

echo ''
echo '##############################'
echo 'RUNNING TESTS for module RULE_MULTI'
echo ''

ansible-playbook tests/rule_multi.yml --extra-vars="ansible_python_interpreter=$(which python)" $VERBOSITY
ansible-playbook tests/rule_multi.yml --check --extra-vars="ansible_python_interpreter=$(which python)" $VERBOSITY

echo ''
echo '##############################'
echo 'RUNNING TESTS for module RULE_PURGE'
echo ''

ansible-playbook tests/rule_purge.yml --extra-vars="ansible_python_interpreter=$(which python)" $VERBOSITY
# no task will be executed..
# ansible-playbook tests/rule_purge.yml --check --extra-vars="ansible_python_interpreter=$(which python)" $VERBOSITY

echo ''
echo '##############################'
echo 'RUNNING TESTS for module SAVEPOINT'
echo ''

ansible-playbook tests/savepoint.yml --extra-vars="ansible_python_interpreter=$(which python)" $VERBOSITY
ansible-playbook tests/savepoint.yml --check --extra-vars="ansible_python_interpreter=$(which python)" $VERBOSITY

echo ''
echo '##############################'
echo 'RUNNING TESTS for module SYSTEM'
echo ''

ansible-playbook tests/system.yml --extra-vars="ansible_python_interpreter=$(which python)" $VERBOSITY
ansible-playbook tests/system.yml --check --extra-vars="ansible_python_interpreter=$(which python)" $VERBOSITY

echo ''
echo '##############################'
echo 'RUNNING TESTS for module PACKAGE'
echo ''

ansible-playbook tests/package.yml --extra-vars="ansible_python_interpreter=$(which python)" $VERBOSITY
ansible-playbook tests/package.yml --check --extra-vars="ansible_python_interpreter=$(which python)" $VERBOSITY

echo ''
echo '##############################'
echo 'FINISHED TESTS!'
echo '##############################'
echo ''
