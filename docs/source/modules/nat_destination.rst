.. _modules_nat_destination:

.. include:: ../_include/head.rst

===============
NAT Destination
===============

**STATE**: unstable

**TESTS**: `Playbook <https://github.com/O-X-L/ansible-opnsense/blob/latest/tests/nat_destination.yml>`_

**API Docs**: `Core - Firewall <https://docs.opnsense.org/development/api/core/firewall.html>`_

**Service Docs**: `Port Forward (Destination NAT) <https://docs.opnsense.org/manual/nat.html#port-forwards>`_

----

Info
****

Savepoint
=========

You can prevent lockout-situations using the savepoint systems:

- :ref:`oxlorg.opnsense.savepoint <modules_savepoint>`

Web-UI
======

These rules are shown in the separate WEB-UI table.

Menu: 'Firewall - NAT - Port Forward'

Definition
**********

Module alias: oxlorg.opnsense.dnat

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "match_fields","list","true","\-","\-","Fields that are used to match configured rules with the running config - if any of those fields are changed, the module will think it's a new rule. At least one of: 'sequence', 'interface', 'ip_protocol', 'protocol', 'source_invert', 'source_net', 'source_port', 'destination_invert', 'destination_net', 'destination_port', 'target', 'local_port', 'description', 'uuid', 'no_port_forward'"
    "sequence","int","false","1","seq","Sequence for rule processing, Integer between 1 and 999999"
    "interface","list","false for deletion, else true","['lan']","int, i","One or multiple interfaces to match this rule on"
    "ip_protocol","string","false","'inet'","ip, ip_proto","IP protocol to match. One of: 'inet', 'inet6', 'inet46' (*IPv4 = 'inet', IPv6 = 'inet6', Both = 'inet46'*)"
    "protocol","string","false","'any'","proto, p","Protocol like 'TCP', 'UDP', 'ICMP', 'TCP/UDP' and so on. For options see the WEB-UI."
    "source_invert","boolean","false","false","src_inv, si, src_not","Inverted matching of the source"
    "source_net","string","false","'any'","source, src, s","Host, network, alias or 'any'"
    "source_port","string","false","\-","src_port, sp","Leave empty to allow all, valid port-number, name, alias or range"
    "destination_invert","boolean","false","false","dest_inv, di, dest_not","Inverted matching of the destination"
    "destination_net","string","false","'any'","destination, dest, d","Host, network, alias or 'any'"
    "destination_port","string","false","\-","dest_port, dp","Leave empty to allow all, valid port-number, name, alias or range"
    "target","string","false for deletion, else true","\-","tgt, t","NAT translation target - IP-Address or alias the matching traffic will be redirected to. Grouped aliases (with multiple entries) can be used for load-balancing."
    "local_port","string","false","\-","nat_port, np","Port the packet will be redirected to - port-number, well-known name or alias"
    "pool_opts","string","false","''","pool_options","Only used if 'target' resolves to multiple entries (load-balancing pool). One of: '', 'round-robin', 'round-robin sticky-address', 'random', 'random sticky-address', 'source-hash', 'bitmask'. Empty uses the system default."
    "nat_reflection","string","false","''","\-","One of: '', 'purenat', 'disable'. Empty uses the system default."
    "associated_rule","string","false","''","pass","Whether and how a matching firewall-rule should be created for this port-forward. One of: '' (*manual - you have to create the matching filter-rule yourself*), 'pass' (*automatically allow the redirected traffic*), 'rule' (*register an associated but separately editable filter-rule*)"
    "no_port_forward","boolean","false","false","nordr","Packets matching this rule will be passed without a port-forward being applied - useful to define exceptions on top of a more general rule"
    "log","boolean","false","true","l","If rule matches should be shown in the firewall logs"
    "description","string","false","\-","name, desc","Description for the rule"
    "tag","string","false","\-","\-","Set a tag on matching packets - can be used with 'tagged' on other rules to build rule-chains"
    "tagged","string","false","\-","\-","Match packets that were tagged with the given value"
    "state","string","false","'present'","st","State of the rule. One of: 'present', 'absent'"
    "enabled","boolean","false","true","en","If the rule should be en- or disabled"
    "uuid","string","false","\-","\-","Optionally you can supply the uuid of an existing rule"
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

Note that this module only manages the port-forward (destination-NAT) rule itself. If you don't set 'associated_rule' to
automatically pass the traffic - you will also need a matching :ref:`oxlorg.opnsense.rule <modules_rule>` to allow it through the filter.

----

Examples
********

.. code-block:: yaml

    - hosts: firewalls
      connection: local
      gather_facts: false
      module_defaults:
        group/oxlorg.opnsense.all:
          firewall: 'opnsense.template.opnsense.oxl.app'
          api_credential_file: '/home/guy/.secret/opn.key'

        oxlorg.opnsense.nat_destination:
          match_fields: ['description']

        oxlorg.opnsense.list:
          target: 'nat_destination'

      tasks:
        - name: Example
          oxlorg.opnsense.nat_destination:
            description: 'example'
            match_fields: ['description']
            interface: ['wan']
            destination_net: '1.2.3.4'
            destination_port: '443'
            target: '192.168.0.10'
            local_port: '8443'
            # sequence: 1
            # ip_protocol: 'inet'
            # protocol: 'TCP'
            # source_invert: false
            # source_net: 'any'
            # source_port: 'any'
            # pool_opts: ''
            # nat_reflection: ''
            # associated_rule: 'pass'
            # no_port_forward: false
            # log: true
            # enabled: true
            # debug: false
            # state: 'present'
            # reload: true

        - name: Adding a port-forward
          oxlorg.opnsense.nat_destination:
            description: 'web-server'
            interface: ['wan']
            protocol: 'TCP'
            destination_net: 'wanip'
            destination_port: '443'
            target: '192.168.0.10'
            local_port: '8443'
            associated_rule: 'pass'

        - name: Disabling the rule
          oxlorg.opnsense.nat_destination:
            description: 'web-server'
            enabled: false

        - name: Listing
          oxlorg.opnsense.list:
          #  target: 'nat_destination'
          register: existing_entries

        - name: Printing
          ansible.builtin.debug:
            var: existing_entries.data

        - name: Removing the rule
          oxlorg.opnsense.nat_destination:
            description: 'web-server'
            state: 'absent'
