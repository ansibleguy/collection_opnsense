.. _modules_rule:

.. include:: ../_include/head.rst

====
Rule
====

**STATE**: unstable

**TESTS**: `Playbook <https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/rule.yml>`_

**API Docs**: `Core - Firewall <https://docs.opnsense.org/development/api/core/firewall.html>`_

**Service Docs**: `Rules <https://docs.opnsense.org/manual/firewall.html#rules.html>`_

Prerequisites
*************

You need to install the following plugin as OPNSense has no core-api for managing its firewall rules:

.. code-block:: bash

    os-firewall

You can also install it using the :ref:`ansibleguy.opnsense.package <modules_package>` module.

Limitations
***********

This plugin has some limitations you need to know of:

* ports don't support aliases
* each of these parameters only takes ONE value per rule:

  * port
  * protocol (*or 'any'; 'TCP/UDP' is NOT valid*)
  * ip-protocol (*IPv4/IPv6*)
  * direction

* gateway-groups are not valid yet => see `OPNSense Forum <https://forum.opnsense.org/index.php?topic=30077.msg146268#msg146268>`_ or `OPNSense Issue <https://github.com/opnsense/plugins/issues/3139>`_
* the ruleset managed by this plugin is SEPARATE from the default WEB-UI rules (*Firewall - Rules*) - combined usage might bring complications
* interfaces must be provided as used in the network config (*p.e. 'opt1' instead of 'DMZ'*)

  * per example see menu: 'Interface - Assignments - Interface ID (in brackets)'
  * this brings problems if the interface-names are not the same on both nodes when using HA-setups

Info
****

Savepoint
=========

You can prevent lockout-situations using the savepoint systems:

- :ref:`ansibleguy.opnsense.savepoint <modules_savepoint>`

Mass-Manage
===========

If you want to mass-manage rules - take a look at the :ref:`ansibleguy.opnsense.rule_multi <modules_rule_multi>` module. It scales better for that use-case!

Web-UI
======

These rules are shown in the separate WEB-UI table.

Menu: 'Firewall - Automation - Filter'

Definition
**********

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "match_fields","list","true","\-","\-","Fields that are used to match configured rules with the running config - if any of those fields are changed, the module will think it's a new rule. At least one of: 'sequence', 'action', 'interface', 'direction', 'ip_protocol', 'protocol', 'source_invert', 'source_net', 'source_port', 'destination_invert', 'destination_net', 'destination_port', 'gateway', 'description', 'uuid'"
    "sequence","int","false","1","seq","Sequence for rule processing, Integer between 1 and 1000000"
    "action","string","false","'pass'","a","Rule action. One of: 'pass', 'block' or 'reject'"
    "quick","boolean","false","true","q","When set to quick, the rule is handled on “first match” basis, which means that the first rule matching the packet will take precedence over rules following in sequence."
    "interface","list","false","['lan']","i, int","One or multiple interfaces use this rule on"
    "direction","string","false","'in'","d, dir","Direction of the traffic. Traffic IN is coming into the firewall interface, while traffic OUT is going out of the firewall interface. In visual terms: [Source] -> IN -> [Firewall] -> OUT -> [Destination]. The default policy is to filter inbound traffic, which means the policy applies to the interface on which the traffic is originally received by the firewall from the source. This is more efficient from a traffic processing perspective. In most cases, the default policy will be the most appropriate."
    "ip_protocol","string","false","'inet'","ipp, ip_proto","IP protocol to match. One of: 'inet', 'inet6' (*IPv4 = 'inet', IPv6 = 'inet6'*)"
    "protocol","string","false","'any'","p, proto","Protocol like 'TCP', 'UDP', 'ICMP' and so on. For options see the WEB-UI. 'TCP/UDP' is NOT valid!"
    "source_invert","boolean","false","false","si, src_inv, src_not","Inverted matching of the source"
    "source_net","string","false","'any'","s, src, source","Host, network, alias or 'any'"
    "source_port","string","false","\-","sp, src_port","Leave empty to allow all, alias not supported"
    "destination_invert","boolean","false","false","di, dest_inv, dest_not","Inverted matching of the destination"
    "destination_net","string","false","'any'","d, dest, destination","Host, network, alias or 'any'"
    "destination_port","string","false","\-","dp, dest_port","Leave empty to allow all, alias not supported"
    "gateway","string","false","\-","g, gw","Existing gateway to use"
    "log","boolean","false","true","l","If rule matches should be shown in the firewall logs"
    "description","string","false","\-","desc","Description for the rule"
    "state","string","false","'present'","st","State of the rule. One of: 'present', 'absent'"
    "enabled","boolean","false","true","en","If the rule should be en- or disabled"
    "uuid","string","false","\-","\-","Optionally you can supply the uuid of an existing rule"

.. include:: ../_include/param_basic.rst


Usage
*****

First you will have to know about **rule-matching**.

The module somehow needs to link the configured and existing rules to manage them.

You need to set how this matching is done by setting the 'match_fields' parameter!

It is **recommended** to use/set **unique identifiers** like 'description' to make sure rules can be matched without overlapping.

You could also use the UUID of existing rules as ID - but you would have to pull (*list*) and configure those 'manually'.

Examples
********

Basic
=====

.. code-block:: yaml

    - hosts: localhost
      gather_facts: no
      module_defaults:
        ansibleguy.opnsense.rule:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'

        ansibleguy.opnsense.list:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'
          target: 'rule'

      tasks:
        - name: Example
          ansibleguy.opnsense.rule:
            source_net: '192.168.0.0/24'  # host, network, alias or 'any'
            destination_net: '192.168.10.0/24'
            destination_port: 443  # alias not supported, leave unset for 'any'
            protocol: 'TCP'
            description: 'Generic test'
            match_fields: ['description']
            # sequence: 1
            # action: 'pass'
            # quick: true
            # interface: 'lan'
            # direction: 'in'
            # ip_protocol: 'inet' or 'inet6'
            # source_invert: false
            # source_port: ''
            # destination_invert: false
            # log: true
            # gateway: 'LAN_GW'
            # state: 'present'
            # enabled: true
            # uuid: 'a9d85c00-0aa2-4705-b855-96aae16e05d7'  # optionally use uuid to identify existing rules
            # debug: true

        - name: Listing
          ansibleguy.opnsense.list:
          #  target: 'rule'
          register: existing_entries

        - name: Printing rules
          ansible.bultin.debug:
            var: existing_entries.data

With inventory config
=====================

.. code-block:: yaml

    - hosts: localhost
      gather_facts: no
      module_defaults:
        ansibleguy.opnsense.rule:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'
          match_fields: ['description']  # setting description as unique-id field

      # you may want to configure your rules inside the inventory
      vars:
        rules:
          wan_deny_tor_exit_nodes_ipv4:
            src: 'ALIAS_URLTABLE_TOR_EXIT_NODES'
            int: 'wan'
            action: 'block'
          wan_deny_tor_exit_nodes_ipv6:
            src: 'ALIAS_URLTABLE_TOR_EXIT_NODES'
            int: 'wan'
            action: 'block'
            ip_proto: 'inet6'
          lan_to_dmz_https:
            src: 'LAN_net'
            dest: 'DMZ_net'
            dest_port: 443
          lan_to_dmz_http:
            src: 'LAN_net'
            dest: 'DMZ_net'
            dest_port: 80
          internal_to_inet_http:
            src: '172.16.0.0/16'
            dest_invert: true
            dest: 'bogons'
            dest_port: 80
          internal_to_inet_https:
            src: '172.16.0.0/16'
            dest_invert: true
            dest: 'bogons'
            dest_port: 443

      tasks:
        - name: Test
          ansibleguy.opnsense.rule:
            description: "{{ rule_id }}"

            action: "{{ rule.action | default(omit) }}"
            interface: "{{ rule.int | default(omit) }}"
            direction: "{{ rule.dir | default(omit) }}"
            ip_protocol: "{{ rule.ip_proto | default(omit) }}"
            protocol: "{{ rule.proto | default(omit) }}"

            source_invert: "{{ rule.src_invert | default(omit) }}"
            source_net: "{{ rule.src | default(omit) }}"
            source_port: "{{ rule.src_port | default(omit) }}"
            destination_invert: "{{ rule.dest_invert | default(omit) }}"
            destination_net: "{{ rule.dest | default(omit) }}"
            destination_port: "{{ rule.dest_port | default(omit) }}"

            sequence: "{{ rule.seq | default(omit) }}"
            quick: "{{ rule.quick | default(omit) }}"
            log: "{{ rule.log | default(omit) }}"
            gateway: "{{ rule.gw | default(omit) }}"
            state: "{{ rule.state | default(omit) }}"
            enabled: "{{ rule.enabled | default(omit) }}"
            # debug: "{{ rule.debug | default(omit) }}"

          vars:
            rule: "{{ rule_item.value }}"
            rule_id: "{{ rule_item.key }}"

          loop_control:
            loop_var: rule_item
          with_dict: "{{ rules }}"

Purging
=======

If you want to delete all existing rules that are **NOT CONFIGURED**.

You can also use the :ref:`ansibleguy.opnsense.rule_purge <modules_rule_multi>` module to do this in a cleaner way.

.. code-block:: yaml

    - hosts: localhost
      gather_facts: no
      module_defaults:
        ansibleguy.opnsense.list:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'
          target: 'rule'

        ansibleguy.opnsense.rule:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'
          match_fields: ['description']

      vars:
        rules: {...}

      tasks:
        - name: Pulling existing rules
          ansibleguy.opnsense.list:
          #  target: 'rule'
          register: existing_entries

        - name: Purging unconfigured rules
          ansibleguy.opnsense.rule:
            state: 'absent'
            description: "{{ existing_rule_id }}"

          when: existing_rule_id not in rules

          vars:
            existing_rule_id: "{{ existing_rule_item.value.description }}"

          loop_control:
            loop_var: existing_rule_item
          with_dict: "{{ existing_entries.data }}"
