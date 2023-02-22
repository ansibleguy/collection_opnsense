#!/bin/bash

set -e

echo ''

DEBUG=false

export ANSIBLE_INVENTORY_UNPARSED_WARNING=False
export ANSIBLE_LOCALHOST_WARNING=False

if [ -z "$1" ] || [ -z "$2" ] || [ -z "$3" ] || [ -z "$4" ]
then
  echo 'Arguments:'
  echo '  1: firewall'
  echo '  2: api key file'
  echo "  3: path to local collection - set to '0' to clone from github"
  echo '  4: name of test to run'
  echo '  5: if test mode should be ran (optional; 0/1; default=1)'
  echo '  6: path to virtual environment (optional)'
  echo ''
  exit 1
else
  export TEST_FIREWALL="$1"
  export TEST_API_KEY="$2"
fi

LOCAL_COLLECTION="$3"
TEST="$4"

if [ -n "$5" ]
then
  CHECK_MODE="$5"
else
  CHECK_MODE='1'
fi

if [ -n "$6" ]
then
  source "$6/bin/activate"
fi

if [[ "$DEBUG" == true ]]
then
  VERBOSITY='-D -vvv'
else
  VERBOSITY=''
fi

cd "$(dirname "$0")/.."
rm -rf "$HOME/.ansible/collections/ansible_collections/ansibleguy/opnsense"

if [[ "$LOCAL_COLLECTION" == '0' ]]
then
  ansible-galaxy collection install git+https://github.com/ansibleguy/collection_opnsense.git
else
  if [ -d "$LOCAL_COLLECTION" ]
  then
    ln -s "$LOCAL_COLLECTION" "$HOME/.ansible/collections/ansible_collections/ansibleguy/opnsense"
  else
    echo "Provided collection path does not exist: '$LOCAL_COLLECTION'"
    exit 1
  fi
fi

function run_test() {
  module="$1"
  check_mode="$2"

  echo ''
  echo '##############################'
  echo "RUNNING TESTS of module: '$module'"
  echo ''

  ansible-playbook "tests/$module.yml" --extra-vars="ansible_python_interpreter=$(which python)" $VERBOSITY
  if [[ "$check_mode" == '1' ]]
  then
    ansible-playbook "tests/$module.yml" --check --extra-vars="ansible_python_interpreter=$(which python)" $VERBOSITY
  fi
}

run_test "$TEST" "$CHECK_MODE"