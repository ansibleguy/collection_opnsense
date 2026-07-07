.. _modules_rule_interface_group:

.. include:: ../_include/head.rst

====================
Rule Interface Group
====================

**STATE**: stable

**TESTS**: `Playbook <https://github.com/O-X-L/ansible-opnsense/blob/latest/tests/rule_interface_group.yml>`_

**API Docs**: `Core - Firewall <https://docs.opnsense.org/development/api/core/firewall.html>`_

**Service Docs**: `Interface Groups <https://docs.opnsense.org/manual/firewall_groups.html>`_

Contribution
************

Thanks to `@jiuka <https://github.com/jiuka>`_ for developing this module!

----

Definition
**********

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","ifname","Name of the interface group. Only texts containing letters, digits and underscores with a maximum length of 15 characters are allowed and the name may not end with a digit."
    "members","list","false","\-","ints, interfaces","Member interfaces - you must provide the network port as shown in 'Interfaces - Assignments - Network port"
    "gui_group","boolean","false","true","\-","Grouping these members in the interfaces menu section"
    "sequence","int","false","0","seq","Sequence used in sorting the groups"
    "description","string","false","\-","desc","Optional description"

.. include:: ../_include/param_basic.rst

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

        oxlorg.opnsense.list:
          target: 'rule_interface_group'

      tasks:
        - name: Example
          oxlorg.opnsense.rule_interface_group:
            name: Internal
            members: ['vtnet0', 'vtnet1']
            # gui_group: true
            # sequence: 0
            # description: 'Optional description'

        - name: Adding 1
          oxlorg.opnsense.rule_interface_group:
            name: Internal
            members: ['vtnet0', 'vtnet1']

        # note: you can also use the module alias-name
        - name: Adding 2
          oxlorg.opnsense.rule_if_group:
            name: DMZ
            members: ['vtnet3', 'vtnet4']

        - name: Listing
          oxlorg.opnsense.list:
          #  target: 'rule_interface_group'
          register: existing_entries

        - name: Printing rules
          ansible.builtin.debug:
            var: existing_entries.data
