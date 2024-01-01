.. _modules_reload:

.. include:: ../_include/head.rst

==========
2 - Reload
==========

**STATE**: stable

**TESTS**: `Playbook <https://github.com/ansibleguy/collection_opnsense/blob/latest/tests/reload.yml>`_

Info
****

This module can reload the running/loaded configuration for a specified part of the OPNSense system.

Most modules of this collection will automatically reload its relevant running config on change - but you can speed up mass-management of items when disabling reload on single module-calls (*reload: false*), and do it afterward using THIS module.

Alternatively you can use the :ref:`ansibleguy.opnsense.service <modules_service>` module with action :code:`reload` if you like it better.

Definition
**********

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "target","string","true","\-","tgt, t","What part of the running config should be reloaded. One of: 'alias', 'rule', 'route', 'cron', 'unbound', 'syslog', 'ipsec', 'ipsec_legacy', 'shaper', 'monit', 'wireguard', 'interface_vlan', 'interface_vxlan', 'interface_vip', 'frr', 'webproxy', 'bind', 'ids'"

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

      tasks:
        - name: Reloading aliases
          ansibleguy.opnsense.reload:
            target: 'alias'

        - name: Reloading routes
          ansibleguy.opnsense.reload:
            target: 'route'

Practical
=========

.. code-block:: yaml

    - hosts: localhost
      gather_facts: no
      module_defaults:
        group/ansibleguy.opnsense.all:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'

      tasks:
        - name: Adding routes
          ansibleguy.opnsense.route:
            network: "{{ item.nw }}"
            gateway: "{{ item.gw }}"
            reload: false
          loop:
            - {nw: '10.206.0.0/16', gw: 'VPN_GW'}
            - {nw: '10.67.0.0/16', gw: 'VPN2_GW'}

        - name: Adding DNS overrides
          ansibleguy.opnsense.unbound_host:
            hostname: "{{ item.host }}"
            domain: 'opnsense.template.ansibleguy.net'
            value: "{{ item.value }}"
            reload: false
          loop:
            - {host: 'a', value: '192.168.0.1'}
            - {host: 'd', value: '192.168.0.5'}

        - name: Reloading
          ansibleguy.opnsense.reload:
            target: "{{ item }}"
          loop:
            - 'route'
            - 'unbound'
