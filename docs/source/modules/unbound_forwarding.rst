.. _modules_unbound_forward:

.. include:: ../_include/head.rst

==========================
DNS - Unbound - Forwarding
==========================

**STATE**: stable

**TESTS**: `Playbook <https://github.com/ansibleguy/collection_opnsense/blob/latest/tests/unbound_forward.yml>`_

**API Docs**: `Core - Unbound <https://docs.opnsense.org/development/api/core/unbound.html>`_

**Service Docs**: `Unbound <https://docs.opnsense.org/manual/unbound.html>`_


Definition
**********

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "domain","string","false","\-","dom, d","Domain of the host. All queries for this domain will be forwarded to the nameserver specified. Leave empty to catch all queries and forward them to the nameserver"
    "target","string","true","\-","server, srv, tgt","Server to forward the dns queries to"
    "port","string","false","53","p","DNS port of the target server"
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

.. include:: ../_include/param_basic.rst

Info
****

This module manages DNS-Forwardings that can be found in the WEB-UI menu: 'Services - Unbound DNS - Query Forwardings'

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

        ansibleguy.opnsense.list:
          target: 'unbound_forward'

      tasks:
        - name: Example
          ansibleguy.opnsense.unbound_forward:
            domain: 'dot.template.ansibleguy.net'
            target: '1.1.1.1'
            # port: 53
            # verify: 'dot.template.ansibleguy.net'
            # state: 'present'
            # enabled: true
            # debug: false

        - name: Adding
          ansibleguy.opnsense.unbound_forward:
            domain: 'dot.template.ansibleguy.net'
            target: '1.1.1.1'

        - name: Listing forwardings
          ansibleguy.opnsense.list:
          #  target: 'unbound_forward'
          register: existing_entries

        - name: Printing DNS-Forwardings
          ansible.builtin.debug:
            var: existing_entries.data
