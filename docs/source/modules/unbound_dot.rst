.. _modules_unbound_dot:

.. include:: ../_include/head.rst

============================
DNS - Unbound - DNS-over-TLS
============================

**STATE**: stable

**TESTS**: `Playbook <https://github.com/ansibleguy/collection_opnsense/blob/latest/tests/unbound_dot.yml>`_

**API Docs**: `Core - Unbound <https://docs.opnsense.org/development/api/core/unbound.html>`_

**Service Docs**: `Unbound <https://docs.opnsense.org/manual/unbound.html>`_


Definition
**********

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "domain","string","true","\-","dom, d","Domain of the DNS-over-TLS entry"
    "target","string","true","\-","server, srv, tgt","DNS target server"
    "port","string","false","53","p","DNS port of the target server"
    "verify","string","false","\-","common_name, cn, hostname","Verify if CN in certificate matches this value, **if not set - certificate verification will not be performed**! Must be a valid IP-Address or hostname."
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

.. include:: ../_include/param_basic.rst

Info
****

This module manages DNS-over-TLS configuration that can be found in the WEB-UI menu: 'Services - Unbound DNS - DNS over TLS'

.. include:: ../_include/unbound_mass.rst

.. warning::

    Unbound service actions like :code:`reload` can take very long (>90s). Please be aware of the **possible downtime**!

    You may also need to increase the module :code:`timeout`.

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
          target: 'unbound_dot'

      tasks:
        - name: Example
          ansibleguy.opnsense.unbound_dot:
            domain: 'dot.template.ansibleguy.net'
            target: '1.1.1.1'
            # port: 53
            # verify: 'dot.template.ansibleguy.net'
            # state: 'present'
            # enabled: true
            # debug: false

        - name: Adding
          ansibleguy.opnsense.unbound_dot:
            domain: 'dot.template.ansibleguy.net'
            target: '1.1.1.1'
            verify: 'dot.template.ansibleguy.net'

        - name: Listing dots
          ansibleguy.opnsense.list:
          #  target: 'unbound_dot'
          register: existing_entries

        - name: Printing DNS-over-TLS entries
          ansible.builtin.debug:
            var: existing_entries.data
