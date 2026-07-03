.. _modules_reload:

.. include:: ../_include/head.rst

======
Reload
======

**STATE**: stable

**TESTS**: `Playbook <https://github.com/O-X-L/ansible-opnsense/blob/latest/tests/reload.yml>`_

Contribution
************

Thanks to `@Rath <https://github.com/superstes>`_ for developing this module!

----

Info
****

This module can reload the running/loaded configuration for a specified part of the OPNsense system.

Like in the WebUI - you have to "Apply" your changes when you are done modifying.

You can also do so by setting the :code:`reload: true` module-argument of the entries that you are modifying.

But sometimes the apply/reload takes a long time (like unbound with DNS-Blocklists, IPS or GeoIP-Aliases) and thus it makes total sense to only trigger the reload once after all entries have been updated.

Alternatively you can use the :ref:`oxlorg.opnsense.service <modules_service>` module with action :code:`reload` if you like it better.

Definition
**********

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "target","string","true","\-","tgt, t","What part of the running config should be reloaded. One of: 'alias', 'rule', 'route', 'cron', 'unbound', 'syslog', 'ipsec', 'ipsec_legacy', 'shaper', 'monit', 'wireguard', 'interface_vlan', 'interface_vxlan', 'interface_vip', 'interface_lagg', 'frr', 'webproxy', 'bind', 'ids', 'dhcrelay', 'dhcp', 'kea', 'dnsmasq'"

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

      tasks:
        - name: Reloading aliases
          oxlorg.opnsense.reload:
            target: 'alias'

        - name: Reloading routes
          oxlorg.opnsense.reload:
            target: 'route'

Practical
=========

.. code-block:: yaml

    - hosts: firewalls
      connection: local
      gather_facts: false
      module_defaults:
        group/oxlorg.opnsense.all:
          firewall: 'opnsense.template.opnsense.oxl.app'
          api_credential_file: '/home/guy/.secret/opn.key'

      tasks:
        - name: Adding routes
          oxlorg.opnsense.route:
            network: "{{ item.nw }}"
            gateway: "{{ item.gw }}"
            reload: false
          loop:
            - {nw: '10.206.0.0/16', gw: 'VPN_GW'}
            - {nw: '10.67.0.0/16', gw: 'VPN2_GW'}

        - name: Adding DNS overrides
          oxlorg.opnsense.unbound_host:
            hostname: "{{ item.host }}"
            domain: 'opnsense.template.opnsense.oxl.app'
            value: "{{ item.value }}"
            reload: false
          loop:
            - {host: 'a', value: '192.168.0.1'}
            - {host: 'd', value: '192.168.0.5'}

        - name: Reloading
          oxlorg.opnsense.reload:
            target: "{{ item }}"
          loop:
            - 'route'
            - 'unbound'
