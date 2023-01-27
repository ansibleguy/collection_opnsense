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

echo ''
echo '##############################'
echo 'STARTING TESTS!'
echo '##############################'
echo ''

# todo: some plugins will be needed as prerequisites - should be installed automatically
#   os-firewall, os-wireguard, os-frr, os-bind
# todo: also: a opt1 interface is needed for some tests

run_test 'reload' 0
run_test 'service' 1
run_test 'alias' 1
run_test 'alias_multi' 1
run_test 'alias_purge' 0
run_test 'rule' 1
run_test 'rule_multi' 1
run_test 'rule_purge' 0
run_test 'savepoint' 1
run_test 'cron' 1
run_test 'route' 1
run_test 'unbound_dot' 1
run_test 'unbound_forward' 1
run_test 'unbound_host' 1
run_test 'unbound_domain' 1
run_test 'unbound_host_alias' 1
run_test 'syslog' 1
run_test 'ipsec_cert' 1
run_test 'shaper_pipe' 1
run_test 'shaper_queue' 1
run_test 'shaper_rule' 1
run_test 'monit_alert' 1
run_test 'monit_test' 1
run_test 'monit_service' 1
run_test 'wireguard_peer' 1
run_test 'wireguard_server' 1
run_test 'wireguard_general' 1
run_test 'wireguard_show' 1
run_test 'interface_vlan' 1
run_test 'interface_vxlan' 1
run_test 'interface_vip' 1
run_test 'source_nat' 1
run_test 'frr_diagnostic' 1
run_test 'frr_bfd_general' 1
run_test 'frr_bfd_neighbor' 1
run_test 'frr_bgp_general' 1
run_test 'frr_bgp_prefix_list' 1
run_test 'frr_bgp_community_list' 1
run_test 'frr_bgp_as_path' 1
run_test 'frr_bgp_route_map' 1
run_test 'frr_bgp_neighbor' 1
run_test 'frr_ospf_general' 1
run_test 'frr_ospf_prefix_list' 1
run_test 'frr_ospf_interface' 1
run_test 'frr_ospf_route_map' 1
run_test 'frr_ospf_network' 1
run_test 'frr_ospf3_general' 1
run_test 'frr_ospf3_interface' 1
run_test 'frr_rip' 1
run_test 'bind_acl' 1
run_test 'bind_general' 1
run_test 'bind_blocklist' 1
run_test 'bind_domain' 1
run_test 'bind_record' 1
run_test 'bind_record_multi' 1
run_test 'webproxy_general' 1
run_test 'webproxy_cache' 1
run_test 'webproxy_parent' 1
run_test 'webproxy_traffic' 1
run_test 'webproxy_forward' 1
run_test 'webproxy_acl' 1
run_test 'webproxy_icap' 1
run_test 'webproxy_auth' 1
run_test 'webproxy_remote_acl' 1
run_test 'webproxy_pac_proxy' 1
run_test 'webproxy_pac_match' 1
run_test 'webproxy_pac_rule' 1
run_test 'system' 1
run_test 'package' 1

echo ''
echo '##############################'
echo 'FINISHED TESTS!'
echo '##############################'
echo ''
