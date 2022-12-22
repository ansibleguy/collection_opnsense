.. _modules_unbound_forward:

.. include:: ../_include/head.rst

==========================
DNS - Unbound - Forwarding
==========================

**STATE**: stable

**TESTS**: `Playbook <https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/unbound_forward.yml>`_

**API DOCS**: `Core - Unbound <https://docs.opnsense.org/development/api/core/unbound.html>`_

**BASE DOCS**: `Unbound <https://docs.opnsense.org/manual/unbound.html>`_


Definition
**********

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "domain","string","true","\-","dom, d","Domain to forward queries of"
    "target","string","true","\-","server, srv, tgt","DNS target server"
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
        ansibleguy.opnsense.unbound_forward:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'

        ansibleguy.opnsense.list:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'
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
