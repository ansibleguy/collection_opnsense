#!/usr/bin/env bash

set -eo pipefail

echo ''

DEBUG=false
TMP_DIR="/tmp/.opnsense_test_$(date +%s)"
TMP_COL_DIR="$TMP_DIR/collections"

export ANSIBLE_INVENTORY_UNPARSED_WARNING=False
export ANSIBLE_LOCALHOST_WARNING=False

if [ -z "$1" ] || [ -z "$2" ] || [ -z "$3" ]
then
  echo 'Arguments:'
  echo '  1: firewall'
  echo '  2: api key file'
  echo "  3: path to local collection - set to '0' to clone from github"
  echo '  4: path to virtual environment (optional)'
  echo ''
  exit 1
else
  export TEST_FIREWALL="$1"
  export TEST_API_KEY="$2"
fi

LOCAL_COLLECTION="$3"

if [ -n "$4" ]
then
  source "$4/bin/activate"
fi

if [[ "$DEBUG" == true ]]
then
  VERBOSITY='-D -vvv'
else
  VERBOSITY=''
fi

set -u

source "$(dirname "$0")/test_prep.sh"  # shared between single/multi test

cd "$TMP_COL_DIR/ansible_collections/ansibleguy/opnsense"

echo ''
echo '##############################'
echo 'STARTING TESTS!'
echo '##############################'
echo ''

run_test 'list' 0
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
run_test 'unbound_general' 1
run_test 'unbound_acl' 1
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
run_test 'frr_general' 1
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
run_test 'ipsec_pool' 1
run_test 'ipsec_connection' 1
run_test 'ipsec_vti' 1
run_test 'ipsec_child' 0  # check mode => dependency on connection-entry
run_test 'ipsec_auth_local' 0  # check mode => dependency on connection/cert-entry
run_test 'ipsec_auth_remote' 0  # check mode => dependency on connection/cert-entry
run_test 'ids_action' 1
run_test 'ids_general' 1
run_test 'ids_ruleset' 1
run_test 'ids_rule' 1
run_test 'ids_user_rule' 1
run_test 'ids_policy' 1
run_test 'ids_policy_rule' 1
run_test 'openvpn_static_key' 1
run_test 'openvpn_client' 1
# run_test 'openvpn_client_override' 1
# run_test 'openvpn_server' 1
run_test 'system' 1
run_test 'package' 1

echo ''
echo '##############################'
echo 'FINISHED TESTS!'
echo '##############################'
echo ''

rm -rf "$TMP_DIR"
