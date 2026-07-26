.. _modules_alias:

.. include:: ../_include/head.rst

=====
Alias
=====

**STATE**: stable

**TESTS**: `Playbook <https://github.com/O-X-L/ansible-opnsense/blob/latest/tests/alias.yml>`_

**API Docs**: `Core - Firewall <https://docs.opnsense.org/development/api/core/firewall.html>`_

**Service Docs**: `Aliases <https://docs.opnsense.org/manual/aliases.html>`_

This module allows you to manage single aliases.

Contribution
************

Thanks to `@Rath <https://github.com/superstes>`_ for developing this module!

----

Info
****

For more detailed information on what alias types are supported - see `the documentation <https://docs.opnsense.org/manual/aliases.html>`_.

To use GeoIP alias types - you need to configure a source for it first. See: `documentation <https://docs.opnsense.org/manual/how-tos/maxmind_geo_ip.html>`_

Mass-Manage
===========

If you want to mass-manage aliases - take a look at the :ref:`oxlorg.opnsense.alias_multi <modules_alias_multi>` module. It is scales better for that use-case!

Definition
**********

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","n","Unique name of the alias"
    "description","string","false","\-","desc","Description for the alias"
    "content","list","false for state changes, else true","\-","cont, c","Values the alias should hold"
    "type","string","false","'host'","t","Type of value the alias should hold. One of: 'host', 'network', 'port', 'url', 'urltable', 'urljson', 'geoip', 'networkgroup', 'mac', 'dynipv6host', 'internal', 'external'"
    "statistics","boolean","false","false","\-", "Maintain a set of counters for this alias"
    "updatefreq_days","float","false","7.0 if type=urltable","\-","Needed only for the alias-type 'urltable' or 'urljson'. Interval to update its content. Per example: 0.5 for every 12 hours"
    "interface","string","false","\-","int, if","Needed only for the alias-type 'dynipv6host'. Select the interface for the V6 dynamic IP"
    "path_expression","string","false","\-","pr, jq","Needed only for the alias-type 'urljson'. Simplified expression to select a field inside a container, a dot is used as field separator (e.g. container.fieldname). Expressions using the jq language are also supported."
    "reload","boolean","false","false","\-", .. include:: ../_include/param_reload.rst

.. include:: ../_include/param_basic.rst

----

Examples
********

.. code-block:: yaml

    - hosts: firewalls
      connection: local
      gather_facts: no
      module_defaults:
        group/oxlorg.opnsense.all:
          firewall: 'opnsense.template.opnsense.oxl.app'
          api_credential_file: '/home/guy/.secret/opn.key'

        oxlorg.opnsense.list:
          target: 'alias'

        oxlorg.opnsense.reload:
          target: 'alias'

      tasks:
        - name: Example
          oxlorg.opnsense.alias:
            name: 'ANSIBLE_TEST1'
            description: 'just a test'
            content: '1.1.1.1'
            state: 'present'
            # type: 'host'  # default
            # updatefreq_days: 3  # used only for type 'urltable' and 'urljson'
            # interface: lan # used only for the type 'dynipv6host'
            # path_expression: '' # used only for type 'urljson'
            # ssl_ca_file: '/etc/ssl/certs/custom/ca.crt'
            # ssl_verify: False
            # api_key: !vault ...  # alternative to 'api_credential_file'
            # api_secret: !vault ...
            # debug: false

        - name: Adding
          oxlorg.opnsense.alias:
            name: 'ANSIBLE_TEST2'
            content: '192.168.1.1'

        - name: Listing
          oxlorg.opnsense.list:
          #  target: 'alias'
          register: existing_entries

        - name: Printing aliases
          ansible.builtin.debug:
            var: existing_entries.data  # type = list of dicts

        - name: Changing
          oxlorg.opnsense.alias:
            name: 'ANSIBLE_TEST2'
            content: ['192.168.1.5', '192.168.10.4']

        - name: Removing
          oxlorg.opnsense.alias:
            name: 'ANSIBLE_TEST3'
            state: 'absent'

        - name: Disabling
          oxlorg.opnsense.alias:
            name: 'ANSIBLE_TEST2'
            enabled: false

        - name: Adding ports
          oxlorg.opnsense.alias:
            name: 'ANSIBLE_TEST3'
            type: 'port'
            content: [80, 443, '9000:9002']

        - name: Adding url-table
          oxlorg.opnsense.alias:
            name: 'ANSIBLE_TEST4'
            type: 'urltable'
            updatefreq_days: 2.6
            content: 'https://www.spamhaus.org/drop/drop.txt'

        - name: Adding url-json
          oxlorg.opnsense.alias:
            name: 'ANSIBLE_TEST5'
            type: 'urltable'
            updatefreq_days: 2.6
            content: 'https://www.spamhaus.org/drop/drop.txt'

        - name: Adding dns-names
          oxlorg.opnsense.alias:
            name: 'ANSIBLE_TEST6'
            content:
              - 'https://api.github.com/meta'
            path_expression: '.web + .api + .git | .[]'

        - name: Adding network
          oxlorg.opnsense.alias:
            name: 'ANSIBLE_TEST6'
            type: 'network'
            content: '192.168.0.0/24'

        - name: Adding geoips regions
          oxlorg.opnsense.alias:
            name: 'ANSIBLE_TEST_1_2_GEOIP2'
            type: 'geoip'
            content: ['AT', 'DE', 'CH']

        - name: Reloading running config
          oxlorg.opnsense.reload:
          #  target: 'alias'
