.. _modules_list:

.. include:: ../_include/head.rst

========
2 - List
========

**STATE**: stable

**TESTS**: Used in multiple ones

Info
****

This module can list existing items/entries of a specified part of the OPNSense system.

In most cases the returned type of this module ist a list of dictionaries.

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "target","string","true","\-","tgt, t","What part of the running config should be queried/listed. One of: 'alias', 'rule', 'route', 'cron', 'syslog', 'package', 'unbound_host', 'unbound_domain', 'unbound_dot', 'unbound_forward', 'unbound_host_alias', 'ipsec_cert', 'shaper_pipe', 'shaper_queue', 'shaper_rule', 'monit_service', 'monit_test', 'monit_alert', 'wireguard_server', 'wireguard_peer', 'interface_vlan', 'interface_vxlan', 'source_nat', 'frr_bfd', 'frr_bgp_general', 'frr_bgp_neighbor', 'frr_bgp_prefix_list', 'frr_bgp_community_list', 'frr_bgp_as_path', 'frr_ospf_general', 'frr_ospf_prefix_list', 'frr_ospf_interface', 'frr_ospf_route_map', 'frr_ospf_network', 'frr_ospf3_general', 'frr_ospf3_interface', 'frr_rip', 'bind_general', 'bind_blocklist', 'bind_acl', 'bind_domain', 'bind_record', 'interface_vip', 'webproxy_general', 'webproxy_cache', 'webproxy_parent', 'webproxy_traffic', 'webproxy_forward'"

.. include:: ../_include/param_basic.rst

Examples
********

.. code-block:: yaml

    - hosts: localhost
      gather_facts: no
      module_defaults:
        ansibleguy.opnsense.list:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'

      tasks:
        - name: Pulling aliases
          ansibleguy.opnsense.list:
            target: 'alias'
          register: existing_aliases

        - name: Printing
          ansible.builtin.debug:
            var: existing_aliases.data

        - name: Pulling routes
          ansibleguy.opnsense.list:
            target: 'route'
          register: existing_routes

        - name: Printing
          ansible.builtin.debug:
            var: existing_routes.data
