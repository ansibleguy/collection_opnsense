.. _modules_unbound_acl:

.. include:: ../_include/head.rst

===================
DNS - Unbound - ACL
===================

**STATE**: stable

**TESTS**: `Playbook <https://github.com/ansibleguy/collection_opnsense/blob/latest/tests/unbound_acl.yml>`_

**API Docs**: `Core - Unbound <https://docs.opnsense.org/development/api/core/unbound.html>`_

**Service Docs**: `Unbound <https://docs.opnsense.org/manual/unbound.html>`_


Info
****

This module manages the ACL settings that can be found in the WEB-UI menu: 'Services - Unbound DNS - Access Lists' (*URL 'ui/unbound/acl'*)

The configured lists are matched by its unique file-name.

Definition
**********

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "enabled","boolean","false","true","\-","En- or disable the ACL"
    "name","string","true","\-","n","Unique name of the ACL"
    "action","string","false","allow","\-","What to to with DNS request that match the criteria. One of: 'allow', 'deny', 'refuse', 'allow_snoop', 'deny_non_local', 'refuse_non_local'"
    "networks","list","false for state changes, else true","\-","nets","The list of networks in CIDR notation to apply this ACL to"
    "description","string","false","\-","desc","The description for the ACL"
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

.. include:: ../_include/param_basic.rst

Examples
********

.. code-block:: yaml

    - hosts: localhost
      gather_facts: no
      module_defaults:
        group/ansibleguy.opnsense.all:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'

        ansibleguy.opnsense.list:
          target: 'unbound_acl'

      tasks:
        - name: Example
          ansibleguy.opnsense.unbound_acl:
            # enabled: true
            # name: ''
            # action: ''
            # networks: ['']
            # description: ''
            # reload: true

        - name: Adding
          ansibleguy.opnsense.unbound_acl:
            name: 'test1'
            action: 'allow'
            networks: ['192.168.0.0/24']

        - name: Changing
          ansibleguy.opnsense.unbound_acl:
            name: 'test1'
            action: 'deny'
            networks: ['192.168.1.0/25']

        - name: Disabling
          ansibleguy.opnsense.unbound_acl:
            name: 'test1'
            action: 'deny'
            networks: ['192.168.1.0/25']
            enabled: false

        - name: Listing
          ansibleguy.opnsense.list:
            # target: 'unbound_acl'
          register: existing_entries

        - name: Printing tests
          ansible.builtin.debug:
            var: existing_entries.data

        - name: Removing
          ansibleguy.opnsense.unbound_acl:
            name: 'test1'
            state: 'absent'
