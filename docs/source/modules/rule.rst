.. _modules_rule:

.. include:: ../_include/head.rst

====
Rule
====

**STATE**: stable

**TESTS**: `Playbook <https://github.com/oxlorg/collection_opnsense/blob/latest/tests/rule.yml>`_

**API Docs**: `Core - Firewall <https://docs.opnsense.org/development/api/core/firewall.html>`_

**Service Docs**: `Rules <https://docs.opnsense.org/manual/firewall.html#rules.html>`_

Contribution
************

Thanks to `@Rath <https://github.com/superstes>`_ for developing this module!

----

Limitations
***********

This plugin has some limitations you need to know of:

* each of these parameters only takes ONE value per rule:

  * port (*port-number, name, alias or range*)
  * protocol (*or 'any'*)
  * ip-protocol (*IPv4/IPv6*)
  * direction

* the ruleset managed by this plugin is SEPARATE from the default WEB-UI rules (*Firewall - Rules*) - combined usage might bring complications
* interfaces must be provided as used in the network config (*p.e. 'opt1' instead of 'DMZ'*)

  * per example see menu: 'Interface - Assignments - Interface ID (in brackets)'
  * this brings problems if the interface-names are not the same on both nodes when using HA-setups

----

Info
****

Tips
====

* If you want to reference :code:`This firewall` - you need to use :code:`(self)` instead.
* If you want to create a :code:`Floating` rule  - you need to use :code:`[]`.


Savepoint
=========

You can prevent lockout-situations using the savepoint systems:

- :ref:`oxlorg.opnsense.savepoint <modules_savepoint>`

Mass-Manage
===========

If you want to mass-manage rules - take a look at the :ref:`oxlorg.opnsense.rule_multi <modules_rule_multi>` module. It scales better for that use-case!

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
    "interface_invert","boolean","false","false","int_inv, ii, int_not","Use all but selected interfaces"
    "direction","string","false","'in'","d, dir","Direction of the traffic. One of: 'in', 'out', 'any'. Traffic IN is coming into the firewall interface, while traffic OUT is going out of the firewall interface. In visual terms: [Source] -> IN -> [Firewall] -> OUT -> [Destination]. The default policy is to filter inbound traffic, which means the policy applies to the interface on which the traffic is originally received by the firewall from the source. This is more efficient from a traffic processing perspective. In most cases, the default policy will be the most appropriate. Use 'any' to apply the rule to both directions."
    "ip_protocol","string","false","'inet'","ipp, ip_proto","IP protocol to match. One of: 'inet', 'inet6' (*IPv4 = 'inet', IPv6 = 'inet6', Both = 'inet46'*)"
    "protocol","string","false","'any'","p, proto","Protocol like 'TCP', 'UDP', 'ICMP', 'TCP/UDP' and so on. For options see the WEB-UI."
    "source_invert","boolean","false","false","si, src_inv, src_not","Inverted matching of the source"
    "source_net","string","false","'any'","s, src, source","Host, network, alias or 'any'"
    "source_port","string","false","\-","sp, src_port","Leave empty to allow all, valid port-number, name, alias or range"
    "destination_invert","boolean","false","false","di, dest_inv, dest_not","Inverted matching of the destination"
    "destination_net","string","false","'any'","d, dest, destination","Host, network, alias or 'any'"
    "destination_port","string","false","\-","dp, dest_port","Leave empty to allow all, valid port-number, name, alias or range"
    "gateway","string","false","\-","g, gw","Existing gateway to use"
    "replyto","string","false","\-","rt","Determines how packets route back in the opposite direction"
    "disable_replyto","boolean","false","false","\-","Explicit disable reply-to for this rule"
    "log","boolean","false","true","l","If rule matches should be shown in the firewall logs"
    "allow_opts","boolean","false","false","opts","Allows packets with IP options to pass"
    "state_type","string","false","keep","\-","State tracking mechanism to use. One of: 'keep', 'sloppy', 'modulate', 'synproxy' or 'none'"
    "state_policy","string","false","''","\-","State tracking mechanism to use. One of: '', 'if-bound', 'floating'"
    "state_timeout","int","false","\-","\-","State Timeout in seconds (TCP only)"
    "max_states","int","false","\-","\-","Limits the number of concurrent states"
    "max_src_nodes","int","false","\-","\-","Limits the number of source addresses which can simultaneously have state table entries"
    "max_src_states","int","false","\-","\-","Limits the number of simultaneous state entries that a single source address can create"
    "max_src_conn","int","false","\-","\-","Limit the number of simultaneous TCP connections a single host can make"
    "max_src_conn_rate","int","false","\-","\-","Maximum new connections per host, measured over time"
    "max_src_conn_rates","int","false","\-","\-","Time interval (seconds) to measure the number of connections"
    "overload","int","false","\-","ol","Overload table used when max new connections per time interval has been reached"
    "adaptive_start","int","false","\-","\-","When the number of state entries exceeds this value, adaptive scaling begins. All timeout values are scaled linearly with factor (adaptive.end - number of states) / (adaptive.end - adaptive.start)"
    "adaptive_end","int","false","\-","\-","When reaching this number of state entries, all timeout values become zero, effectively purging all state entries immediately. This value is used to define the scale factor, it should not actually be reached (set a lower state limit)"
    "prio","string","false","\-","\-","Match packets which have the given queueing priority assigned. One of: '', '0', '1', '2', '3', '4', '5', '6', '7'"
    "set_prio","string","false","\-","\-","Assigne a specific queueing priority. One of: '', '0', '1', '2', '3', '4', '5', '6', '7'"
    "set_prio_low","string","false","\-","\-","Assigne a specific queueing priority to packets which have a TOS of lowdelay and TCP ACKs with no data payload. One of: '', '0', '1', '2', '3', '4', '5', '6', '7'"
    "tag","string","false","\-","\-","Packets matching this rule will be tagged with the specified string"
    "tagged","string","false","\-","\-","Packets must already be tagged with the given tag in order to match the rule"
    "tcp_flags","list","false","\-","\-","TCP flags that must be set for this rule to match. Selection of: 'syn', 'ack', 'fin', 'rst', 'psh', 'urg', 'ece', 'cwr'"
    "tcp_flags_clear","list","false","\-","\-","TCP flags that must be cleared for this rule to match. Selection of: 'syn', 'ack', 'fin', 'rst', 'psh', 'urg', 'ece', 'cwr'"
    "schedule","string","false","\-","sched","Match packets during the given schedule"
    "tos","string","false","\-","\-","Match packets which have the given TOS/DCSP assigned"
    "description","string","false","\-","name,desc","Description for the rule"
    "state","string","false","'present'","st","State of the rule. One of: 'present', 'absent'"
    "enabled","boolean","false","true","en","If the rule should be en- or disabled"
    "uuid","string","false","\-","\-","Optionally you can supply the uuid of an existing rule"
    "icmp_type","list","false","\-","\-","If protocol is ICMP/IPV6-ICMP you can specify the types. One or more of: 'echoreq', 'echorep', 'unreach', 'squench', 'redir', 'althost', 'routeradv', 'routersol', 'timex', 'paramprob', 'timereq', 'timerep', 'inforeq', 'inforep', 'maskreq', 'maskrep'"
    "reload","boolean","false","true","apply", .. include:: ../_include/param_reload.rst

.. include:: ../_include/param_basic.rst

----

Usage
*****

First you will have to know about **rule-matching**.

The module somehow needs to link the configured and existing rules to manage them.

You need to set how this matching is done by setting the 'match_fields' parameter!

It is **recommended** to use/set **unique identifiers** like 'description' to make sure rules can be matched without overlapping.

You could also use the UUID of existing rules as ID - but you would have to pull (*list*) and configure those 'manually'.

----

Examples
********

Basic
=====

.. code-block:: yaml

    - hosts: firewalls
      connection: local
      gather_facts: false
      module_defaults:
        group/oxlorg.opnsense.all:
          firewall: 'opnsense.template.opnsense.oxl.app'
          api_credential_file: '/home/guy/.secret/opn.key'

        oxlorg.opnsense.list:
          target: 'rule'

      tasks:
        - name: Example
          oxlorg.opnsense.rule:
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
            # interface_invert: false
            # direction: 'in'
            # ip_protocol: 'inet' or 'inet6'
            # source_invert: false
            # source_port: ''
            # destination_invert: false
            # gateway: 'LAN_GW'
            # replyto: ''
            # disable_replyto: false
            # log: true
            # allow_opts: false
            # state_type: keep
            # state_policy: None
            # state_timeout: None
            # max_states: None
            # max_src_nodes: None
            # max_src_states: None
            # max_src_conn: None
            # max_src_conn_rate: None
            # max_src_conn_rates: None
            # overload: None
            # adaptive_start: None
            # adaptive_end: None
            # prio: ''
            # set_prio: ''
            # set_prio_low: ''
            # tag: ''
            # tagged: ''
            # tcp_flags: None
            # tcp_flags_clear: None
            # schedule: None
            # tos: None
            # icmp_type: []
            # state: 'present'
            # enabled: true
            # uuid: 'a9d85c00-0aa2-4705-b855-96aae16e05d7'  # optionally use uuid to identify existing rules
            # debug: true
            # reload: true

        - name: Listing
          oxlorg.opnsense.list:
          #  target: 'rule'
          register: existing_entries

        - name: Printing rules
          ansible.builtin.debug:
            var: existing_entries.data

With inventory config
=====================

.. code-block:: yaml

    - hosts: firewalls
      connection: local
      gather_facts: false
      module_defaults:
        group/oxlorg.opnsense.all:
          firewall: 'opnsense.template.opnsense.oxl.app'
          api_credential_file: '/home/guy/.secret/opn.key'

        oxlorg.opnsense.rule:
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
          oxlorg.opnsense.rule:
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
            enabled: "{{ rule.enabled | default(true) }}"
            # debug: "{{ rule.debug | default(false) }}"

          vars:
            rule: "{{ rule_item.value }}"
            rule_id: "{{ rule_item.key }}"

          loop_control:
            loop_var: rule_item
          with_dict: "{{ rules }}"

Purging
=======

If you want to delete all existing rules that are **NOT CONFIGURED**.

You can also use the :ref:`oxlorg.opnsense.rule_purge <modules_rule_multi>` module to do this in a cleaner way.

.. code-block:: yaml

    - hosts: firewalls
      connection: local
      gather_facts: false
      module_defaults:
        group/oxlorg.opnsense.all:
          firewall: 'opnsense.template.opnsense.oxl.app'
          api_credential_file: '/home/guy/.secret/opn.key'

        oxlorg.opnsense.list:
          target: 'rule'

        oxlorg.opnsense.rule:
          match_fields: ['description']

      vars:
        rules: {...}

      tasks:
        - name: Pulling existing rules
          oxlorg.opnsense.list:
          #  target: 'rule'
          register: existing_entries

        - name: Purging unconfigured rules
          oxlorg.opnsense.rule:
            state: 'absent'
            description: "{{ existing_rule_id }}"

          when: existing_rule_id not in rules

          vars:
            existing_rule_id: "{{ existing_rule_item.value.description }}"

          loop_control:
            loop_var: existing_rule_item
          with_dict: "{{ existing_entries.data }}"
