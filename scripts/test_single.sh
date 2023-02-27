#!/bin/bash

set -eo pipefail

echo ''

DEBUG=false
TMP_DIR="/tmp/.opnsense_test_$(date +%s)"
TMP_COL_DIR="$TMP_DIR/collections"

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

source "$(dirname "$0")/test_prep.sh"  # shared between single/multi test

cd "$TMP_COL_DIR/ansible_collections/ansibleguy/opnsense"

run_test "$TEST" "$CHECK_MODE"
