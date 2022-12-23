.. _modules_unbound_domain:

.. include:: ../_include/head.rst

===============================
DNS - Unbound - Domain Override
===============================


**STATE**: unstable

**TESTS**: `Playbook <https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/unbound_domain.yml>`_

**API Docs**: `Core - Unbound <https://docs.opnsense.org/development/api/core/unbound.html>`_

**Service Docs**: `Unbound <https://docs.opnsense.org/manual/unbound.html>`_

Definition
**********

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "match_fields","string","false","['domain', 'server']","\-","Fields that are used to match configured domain-overrides with the running config - if any of those fields are changed, the module will think it's a new entry. At least one of: 'domain', 'server', 'description'"
    "domain","string","true","\-","dom, d","Domain to override"
    "server","string","true","\-","value, srv","Target server"
    "description","string","false","\-","desc","Optional description for the domain-override. Could be used as unique-identifier when set as only 'match_field'."
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

.. include:: ../_include/param_basic.rst

Info
****

This module manages DNS domain-overrides configuration that can be found in the WEB-UI menu: 'Services - Unbound DNS - Overrides - Domain overrides'

Entries like these override an entire domain by specifying an authoritative DNS server to be queried for that domain.

Usage
*****

First you will have to know about **domain-matching**.

The module somehow needs to link the configured and existing domain-overrides to manage them.

You can to set how this matching is done by setting the 'match_fields' parameter!

The default behaviour is that a domain-override is matched by its 'domain' and 'server' fields.

However - it is **recommended** to use/set 'description' as **unique identifier** if many overrides are used.

.. include:: ../_include/unbound_mass.rst

Examples
********

.. code-block:: yaml

    - hosts: localhost
      gather_facts: no
      module_defaults:
        ansibleguy.opnsense.unbound_domain:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'
          match_fields: ['description']

        ansibleguy.opnsense.list:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'
          target: 'unbound_domain'

      tasks:
        - name: Example
          ansibleguy.opnsense.unbound_domain:
            domain: 'opnsense.template.ansibleguy.net'
            server: '192.168.0.1'
            # match_fields: ['description']
            # description: 'example'
            # state: 'present'
            # enabled: true
            # debug: false

        - name: Adding
          ansibleguy.opnsense.unbound_domain:
            domain: 'opnsense.template.ansibleguy.net'
            server: '192.168.0.1'
            match_fields: ['description']
            description: 'test1'
            # match_fields: ['description']

        - name: Disabling
          ansibleguy.opnsense.unbound_domain:
            domain: 'opnsense.template.ansibleguy.net'
            server: '192.168.0.1'
            match_fields: ['description']
            description: 'test1'
            enabled: false
            # match_fields: ['description']

        - name: Removing
          ansibleguy.opnsense.unbound_domain:
            domain: 'opnsense.template.ansibleguy.net'
            server: '192.168.0.1'
            state: 'absent'
            description: 'test1'
            # match_fields: ['description']

        - name: Listing domains
          ansibleguy.opnsense.list:
          #  target: 'unbound_domain'
          register: existing_entries

        - name: Printing entries
          ansible.builtin.debug:
            var: existing_entries.data
