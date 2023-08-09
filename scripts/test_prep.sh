#!/usr/bin/env bash

set -u

mkdir -p "$TMP_COL_DIR"
cd "$TMP_DIR"
export ANSIBLE_COLLECTIONS_PATH="$TMP_COL_DIR"

if [[ "$LOCAL_COLLECTION" == '0' ]]
then
  ansible-galaxy collection install git+https://github.com/ansibleguy/collection_opnsense.git -p "$TMP_COL_DIR"
else
  if [ -d "$LOCAL_COLLECTION" ]
  then
    echo "### TESTING COLLECTION: '$LOCAL_COLLECTION' ###"
    mkdir -p "$TMP_COL_DIR/ansible_collections/ansibleguy/"
    ln -s "$LOCAL_COLLECTION" "$TMP_COL_DIR/ansible_collections/ansibleguy/opnsense"
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
