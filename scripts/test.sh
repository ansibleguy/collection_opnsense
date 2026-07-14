#!/usr/bin/env bash

set -eo pipefail

echo ''

DEBUG=false
TMP_DIR="/tmp/.opnsense_test_$(date +%s)"
TMP_COL_DIR="${TMP_DIR}/collections"

export ANSIBLE_INVENTORY_UNPARSED_WARNING=False
export ANSIBLE_LOCALHOST_WARNING=False
export ANSIBLE_NO_TARGET_SYSLOG=True

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

export SUCCEEDED=''
export FAILED=''
EXIT_CODE=0

set -u

source "$(dirname "$0")/test_prep.sh"  # shared between single/multi test

function run_test_soft() {
  module="$1"
  check_mode="$2"
  run_test "$module" "$check_mode"
  if [[ "$?" == '0' ]]
  then
    if [[ -n "$SUCCEEDED" ]]
    then
      export SUCCEEDED="${SUCCEEDED}, "
    fi
    export SUCCEEDED="${SUCCEEDED}${module}"
  else
    if [[ -n "$FAILED" ]]
    then
      export FAILED="${FAILED}, "
    fi
    export FAILED="${FAILED}${module}"
    EXIT_CODE=1
  fi
}

cd "$TMP_COL_DIR/ansible_collections/oxlorg/opnsense"

echo ''
echo '##############################'
echo '        STARTING TESTS!'
echo '##############################'
echo ''

set +e

run_test_soft '1_version' 0
run_test '1_cleanup' 0
run_test_soft '1_reload' 0

set +e

run_test_soft 'list' 0
run_test_soft 'service' 1
run_test_soft 'system' 1
run_test_soft 'package' 1
run_test_soft '1_dependencies' 0
run_test_soft 'alias' 1
run_test_soft '1_multi' 1
run_test_soft 'alias_multi' 1
run_test_soft 'alias_purge' 0
run_test_soft 'rule' 1
run_test_soft 'rule_multi' 1
run_test_soft 'rule_purge' 0
run_test_soft 'rule_interface_group' 1
run_test_soft 'savepoint' 1
run_test_soft 'cron' 1
run_test_soft 'route' 1
run_test_soft 'gateway' 1
run_test_soft 'unbound_general' 1
run_test_soft 'unbound_acl' 1
run_test_soft 'unbound_dot' 1
run_test_soft 'unbound_forward' 1
run_test_soft 'unbound_host' 1
run_test_soft 'unbound_host_alias' 1
run_test_soft 'unbound_dnsbl' 1
run_test_soft 'syslog' 1
run_test_soft 'shaper_pipe' 1
run_test_soft 'shaper_queue' 1
run_test_soft 'shaper_rule' 1
run_test_soft 'monit_alert' 1
run_test_soft 'monit_test' 1
run_test_soft 'monit_service' 1
run_test_soft 'wireguard_peer' 1
run_test_soft 'wireguard_server' 1
run_test_soft 'wireguard_general' 1
run_test_soft 'wireguard_show' 1
run_test_soft 'interface_vlan' 1
run_test_soft 'interface_vxlan' 1
run_test_soft 'interface_vip' 1
run_test_soft 'interface_lagg' 1
run_test_soft 'interface_loopback' 1
run_test_soft 'interface_gre' 1
run_test_soft 'interface_bridge' 1
run_test_soft 'interface_gif' 1
run_test_soft 'nat_source' 1
run_test_soft 'nat_one_to_one' 1
run_test_soft 'nat_destination' 1
run_test_soft 'frr_diagnostic' 1
run_test_soft 'frr_general' 1
run_test_soft 'frr_bfd_general' 1
run_test_soft 'frr_bfd_neighbor' 1
run_test_soft 'frr_bgp_general' 1
run_test_soft 'frr_bgp_prefix_list' 1
run_test_soft 'frr_bgp_community_list' 1
run_test_soft 'frr_bgp_as_path' 1
run_test_soft 'frr_bgp_route_map' 1
run_test_soft 'frr_bgp_neighbor' 1
run_test_soft 'frr_bgp_redistribution' 1
run_test_soft 'frr_bgp_peer_group' 1
run_test_soft 'frr_ospf_general' 1
run_test_soft 'frr_ospf_prefix_list' 1
run_test_soft 'frr_ospf_interface' 1
run_test_soft 'frr_ospf_route_map' 1
run_test_soft 'frr_ospf_network' 1
run_test_soft 'frr_ospf_redistribution' 1
run_test_soft 'frr_ospf3_general' 1
run_test_soft 'frr_ospf3_prefix_list' 1
run_test_soft 'frr_ospf3_interface' 1
run_test_soft 'frr_ospf3_route_map' 1
run_test_soft 'frr_ospf3_network' 1
run_test_soft 'frr_ospf3_redistribution' 1
run_test_soft 'frr_rip' 1
run_test_soft 'bind_acl' 1
run_test_soft 'bind_general' 1
run_test_soft 'bind_blocklist' 1
run_test_soft 'bind_domain' 1
run_test_soft 'bind_record' 1
run_test_soft 'bind_record_multi' 1
run_test_soft 'webproxy_general' 1
run_test_soft 'webproxy_cache' 1
run_test_soft 'webproxy_parent' 1
run_test_soft 'webproxy_traffic' 1
run_test_soft 'webproxy_forward' 1
run_test_soft 'webproxy_acl' 1
run_test_soft 'webproxy_icap' 1
run_test_soft 'webproxy_auth' 1
run_test_soft 'webproxy_remote_acl' 1
run_test_soft 'webproxy_pac_proxy' 1
run_test_soft 'webproxy_pac_match' 1
run_test_soft 'webproxy_pac_rule' 1
run_test_soft 'ipsec_cert' 1
run_test_soft 'ipsec_psk' 1
run_test_soft 'ipsec_pool' 1
run_test_soft 'ipsec_connection' 1
run_test_soft 'ipsec_vti' 1
run_test_soft 'ipsec_child' 0  # check mode => dependency on connection-entry
run_test_soft 'ipsec_auth_local' 0  # check mode => dependency on connection/cert-entry
run_test_soft 'ipsec_auth_remote' 0  # check mode => dependency on connection/cert-entry
run_test_soft 'ipsec_manual_spd' 1
run_test_soft 'ipsec_general' 1
run_test_soft 'ids_action' 1
run_test_soft 'ids_general' 1
run_test_soft 'ids_ruleset' 1
run_test_soft 'ids_rule' 1
run_test_soft 'ids_user_rule' 1
run_test_soft 'ids_policy' 1
run_test_soft 'ids_policy_rule' 1
run_test_soft 'openvpn_status' 1
run_test_soft 'openvpn_static_key' 1
run_test_soft 'openvpn_client' 1
run_test_soft 'openvpn_server' 1
run_test_soft 'openvpn_client_override' 0  # check mode => dependency on server-entry
# run_test_soft 'openvpn_client_template' 1
# run_test_soft 'openvpn_client_export' 1
run_test_soft 'nginx_general' 1
run_test_soft 'nginx_upstream_server' 1
run_test_soft 'dhcrelay_destination' 1
run_test_soft 'dhcrelay_relay' 1
run_test_soft 'dhcp_general' 1
run_test_soft 'dhcp_controlagent' 1
run_test_soft 'dhcp_subnet' 1
run_test_soft 'dhcp_reservation' 1
run_test_soft 'acme_general' 1
run_test_soft 'acme_account' 1
run_test_soft 'acme_validation' 1
run_test_soft 'acme_action' 1
run_test_soft 'acme_certificate' 0  # check mode => dependency on other acme-entries
run_test_soft 'postfix_general' 1
run_test_soft 'postfix_domain' 1
run_test_soft 'postfix_recipient' 1
run_test_soft 'postfix_recipientbcc' 1
run_test_soft 'postfix_sender' 1
run_test_soft 'postfix_senderbcc' 1
run_test_soft 'postfix_sendercanonical' 1
run_test_soft 'postfix_headercheck' 1
run_test_soft 'postfix_address' 1
run_test_soft 'hasync_general' 1
run_test_soft 'hasync_service' 0 # check mode => dependency on hasync_general
run_test_soft 'snapshot' 1
run_test_soft 'wazuh_agent' 1
run_test_soft 'raw' 1
run_test_soft 'user' 1
run_test_soft 'group' 1
run_test_soft 'privilege' 0 # check mode => dependency on user and group
run_test_soft 'neighbor' 1
run_test_soft 'dnsmasq_general' 1
run_test_soft 'dnsmasq_domain' 1
run_test_soft 'dnsmasq_host' 1
run_test_soft 'dnsmasq_range' 1
run_test_soft 'dnsmasq_option' 1
run_test_soft 'dnsmasq_boot' 1
run_test_soft 'dnsmasq_tag' 1
run_test_soft 'haproxy_cpu' 1
run_test_soft 'haproxy_user' 1
run_test_soft 'haproxy_group' 1
run_test_soft 'haproxy_general_stats' 1
run_test_soft 'haproxy_maintenance' 1
run_test_soft 'haproxy_general_cache' 1
run_test_soft 'haproxy_general_defaults' 1
run_test_soft 'haproxy_general_logging' 1
run_test_soft 'haproxy_general_peers' 1
run_test_soft 'haproxy_general_settings' 1
run_test_soft 'haproxy_general_tuning' 1
run_test_soft 'haproxy_acl' 1
run_test_soft 'haproxy_action' 1
run_test_soft 'haproxy_lua' 1
run_test_soft 'haproxy_fcgi' 1
run_test_soft 'haproxy_errorfile' 1
run_test_soft 'haproxy_mailer' 1
run_test_soft 'haproxy_mapfile' 1
run_test_soft 'haproxy_resolver' 1
run_test_soft 'haproxy_backend' 1
run_test_soft 'haproxy_frontend' 1
run_test_soft 'haproxy_healthcheck' 1
run_test_soft 'haproxy_server' 1
run_test_soft 'nut' 1
run_test_soft 'nut_diagnostics' 1

run_test_soft '1_cleanup' 0
run_test_soft '1_reload' 0
run_test_soft '1_version' 0

echo ''
echo '##############################'
echo '        FINISHED TESTS!'
echo '##############################'
echo ''

echo '##############################'
echo '           RESULTS:'
if echo "$USER" | grep -q 'test'
then
  echo "SUCCEEDED: ${SUCCEEDED}"
  echo "FAILED: ${FAILED}"
else
  printf "\033[0;32mSUCCEEDED: ${SUCCEEDED}\033[0m\n"
  printf "\033[0;31mFAILED: ${FAILED}\033[0m\n"
fi

echo '##############################'

rm -rf "$TMP_DIR"

exit "$EXIT_CODE"
