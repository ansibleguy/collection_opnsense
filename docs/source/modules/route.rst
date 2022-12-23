.. _modules_route:

.. include:: ../_include/head.rst

=====
Route
=====

**STATE**: unstable

**TESTS**: `Playbook <https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/route.yml>`_

**API Docs**: `Core - Routes <https://docs.opnsense.org/development/api/core/routes.html>`_

**Service Docs**: `Routes <https://docs.opnsense.org/manual/routes.html>`_

Definition
**********

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "gateway","string","true","\-","gw","An existing gateway that should be used as target for the network. The network ip protocol (*IPv4/IPv6*) must be the same! **WARNING**: You need to supply the gateways short-name as can be seen in the WEB-UI menu 'System - Gateways - Single - Name'"
    "network","string","true","\-","nw, net","Network to route. The network ip protocol (*IPv4/IPv6*) must be the same!"
    "description","string","false","\-","desc","Optional description for the route. Could be used as unique-identifier when set as only 'match_field'."
    "match_fields","list of strings","false","['network', 'gateway']","\-","Fields that are used to match configured routes with the running config - if any of those fields are changed, the module will think it's a new route"
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

.. include:: ../_include/param_basic.rst

Usage
*****

First you will have to know about **route-matching**.

The module somehow needs to link the configured and existing routes to manage them.

You can to set how this matching is done by setting the 'match_fields' parameter!

The default behaviour is that a route is matched by its 'gateway' and 'network'.

However - it is **recommended** to use/set 'description' as **unique identifier** if many routes are used.


Examples
********

.. code-block:: yaml

    - hosts: localhost
      gather_facts: no
      module_defaults:
        ansibleguy.opnsense.route:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'
          match_fields: ['description']

        ansibleguy.opnsense.list:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'
          target: 'route'

      tasks:
        - name: Example
          ansibleguy.opnsense.route:
            description: 'test1'
            network: '172.16.0.0/12'
            gateway: 'LAN_GW'
            # match_fields: ['description']
            # enabled: true
            # debug: false
            # state: 'present'

        - name: Adding route
          ansibleguy.opnsense.route:
            description: 'test2'
            network: '10.206.0.0/16'
            gateway: 'VPN_GW'
            # match_fields: ['description']

        - name: Disabling route
          ansibleguy.opnsense.route:
            description: 'test3'
            network: '10.55.0.0/16'
            gateway: 'VPN_GW'
            enabled: false
            # match_fields: ['description']

        - name: Listing routes
          ansibleguy.opnsense.list:
          #  target: 'route'
          register: existing_entries

        - name: Printing routes
          ansible.builtin.debug:
            var: existing_entries.data

        - name: Removing route 'test3'
          ansibleguy.opnsense.route:
            description: 'test3'
            network: '10.55.0.0/16'
            gateway: 'VPN_GW'
            state: 'absent'
            match_fields: ['description']
