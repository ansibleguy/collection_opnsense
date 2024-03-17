.. _modules_unbound_host_alias:

.. include:: ../_include/head.rst

==========================
DNS - Unbound - Host Alias
==========================

**STATE**: stable

**TESTS**: `Playbook <https://github.com/ansibleguy/collection_opnsense/blob/latest/tests/unbound_host_alias.yml>`_

**API Docs**: `Core - Unbound <https://docs.opnsense.org/development/api/core/unbound.html>`_

**Service Docs**: `Unbound <https://docs.opnsense.org/manual/unbound.html>`_

Definition
**********

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "match_fields","string","false","['alias', 'domain']","\-","Fields that are used to match configured domain-overrides with the running config - if any of those fields are changed, the module will think it's a new entry. At least one of: 'hostname', 'domain', 'alias',  'description'"
    "alias","string","true","\-","hostname","Host-alias to create"
    "domain","string","true","\-","dom, d","Domain to override"
    "target","string","false for state changes, else true","\-","tgt, host","Existing host override record"
    "description","string","false","\-","desc","Optional description for the host-alias. Could be used as unique-identifier when set as only 'match_field'."
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

.. include:: ../_include/param_basic.rst

Info
****

This module manages DNS host-alias override configuration that can be found in the WEB-UI menu: 'Services - Unbound DNS - Overrides - Host overrides - Aliases'

Entries like these override individual results from the forwarders.

Use these for changing DNS results or for adding custom DNS records.

Keep in mind that all resource record types (i.e. A, AAAA, MX, etc. records) of a specified host below are being overwritten.

.. warning::

    Unbound service actions like :code:`reload` can take long. Please be aware of the **possible downtime**!

    You may also need to increase the module :code:`timeout`.

Usage
*****

First you will have to know about **alias-matching**.

The module somehow needs to link the configured and existing host-aliases to manage them.

You can to set how this matching is done by setting the 'match_fields' parameter!

The default behaviour is that a host-alias is matched by its 'alias' and 'domain' fields.

However - it is **recommended** to use/set 'description' as **unique identifier** if many aliases are used.

.. include:: ../_include/unbound_mass.rst

Examples
********

.. code-block:: yaml

    - hosts: localhost
      gather_facts: no
      module_defaults:
        group/ansibleguy.opnsense.all:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'

        ansibleguy.opnsense.unbound_host_alias:
          match_fields: ['description']

        ansibleguy.opnsense.list:
          target: 'unbound_host_alias'

      tasks:
        - name: Example
          ansibleguy.opnsense.unbound_host_alias:
            alias: 'test'
            domain: 'opnsense.template.ansibleguy.net'
            target: 'host.opnsense.template.ansibleguy.net'
            # match_fields: ['description']
            # description: 'example'
            # state: 'present'
            # reload: true
            # enabled: true
            # debug: false

        - name: Adding alias 'test1.local' for record 'test.local'
          ansibleguy.opnsense.unbound_host_alias:
            alias: 'test1'
            domain: 'local'
            target: 'test.local'
            description: 'test1'
            # match_fields: ['description']

        - name: Disabling
          ansibleguy.opnsense.unbound_host_alias:
            alias: 'test1'
            domain: 'local'
            target: 'test.local'
            description: 'test1'
            enabled: false
            # match_fields: ['description']

        - name: Removing
          ansibleguy.opnsense.unbound_host_alias:
            alias: 'test1'
            domain: 'local'
            target: 'test.local'
            state: 'absent'
            description: 'test1'
            # match_fields: ['description']

        - name: Listing
          ansibleguy.opnsense.list:
          #  target: 'unbound_host_alias'
          register: existing_entries

        - name: Printing aliases
          ansible.builtin.debug:
            var: existing_entries.data
