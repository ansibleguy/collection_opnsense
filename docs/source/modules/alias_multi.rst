.. _modules_alias_multi:

.. include:: ../_include/head.rst

=======================
Alias - Mass Management
=======================


**STATE**: stable

**TESTS**: `Playbook <https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/alias_multi.yml>`_

**API Docs**: `Core - Firewall <https://docs.opnsense.org/development/api/core/firewall.html>`_

**Service Docs**: `Aliases <https://docs.opnsense.org/manual/aliases.html>`_

This module allows you to manage multiple aliases.

It is faster than the 'alias' module as it reduces the needed api/http calls.

Info
****

For more detailed information on what alias types are supported - see the `OPNSense documentation <https://docs.opnsense.org/manual/aliases.html>`_.

Multi
*****

- Each alias has the attributes as defined in the :ref:`ansibleguy.opnsense.alias <modules_alias>` module

- To ensure valid configuration - the attributes of each alias get verified using ansible's built-in verifier

Definition
**********

.. include:: ../_include/param_basic.rst

ansibleguy.opnsense.alias_multi
===============================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "aliases","dictionary","true","\-","\-","Dictionary of aliases to manage/configure"
    "fail_verification","boolean","false","false","fail_verify","Fail module if single alias fails the verification"
    "fail_processing","boolean","false","true","fail_proc","Fail module if single alias fails to be processed"
    "state","string","false","'present'","\-","Options: 'present', 'absent'"
    "enabled","boolean","false","true","\-","If all aliases should be en- or disabled"
    "output_info","boolean","false","false","info","Enable to show some information on processing at runtime. Will be hidden if the tasks 'no_log' parameter is set to 'true'."
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

ansibleguy.opnsense.alias_purge
===============================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "aliases","dictionary","true","\-","\-","Configured aliases - to exclude from purging"
    "output_info","boolean","false","false","info","Enable to show some information on processing at runtime. Will be hidden if the tasks 'no_log' parameter is set to 'true'."
    "action","string","false","'delete'","\-","What to do with the matched aliases. One of: 'disable', 'delete'"
    "filters","dictionary","false","\-","\-","Field-value pairs to filter on - per example: {type: port} - to only purge aliases of type 'port'"
    "filter_invert","boolean","false","false","\-","If true - it will purge all but the filtered ones"
    "filter_partial","boolean","false","false","\-","If true - the filter will also match if it is just a partial value-match"
    "force_all","boolean","false","false","\-","If set to true and neither aliases, nor filters are provided - all non-builtin aliases will be purged"
    "fail_all","boolean","false","false","fail","Fail module if single alias fails to be purged"
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

Examples
********

.. code-block:: yaml

    - hosts: localhost
      gather_facts: no
      module_defaults:
        ansibleguy.opnsense.alias_multi:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'

        ansibleguy.opnsense.list:
          firewall: "{{ lookup('ansible.builtin.env', 'TEST_FIREWALL') }}"
          api_credential_file: "{{ lookup('ansible.builtin.env', 'TEST_API_KEY') }}"
          target: 'alias'

        ansibleguy.opnsense.alias_purge:
          firewall: "{{ lookup('ansible.builtin.env', 'TEST_FIREWALL') }}"
          api_credential_file: "{{ lookup('ansible.builtin.env', 'TEST_API_KEY') }}"

      tasks:
        - name: Creation
          ansibleguy.opnsense.alias_multi:
            fail_verification: true  # default = false; Fail module if single alias fails the verification
            aliases:
              test1:
                content: '1.1.1.1'
              test2:
                content: ['1.1.1.1', '1.1.1.2']
                description: 'to be deleted'
              test3:
                type: 'network'
                content: '10.0.0.0/24'
                description: 'to be disabled'
            # fail_processing: false
            # output_info: false

        - name: Changes
          ansibleguy.opnsense.alias_multi:
            aliases:
              test1:
                content: ['1.1.1.3']
              test2:
                state: 'absent'
              test3:
                enabled: false

        - name: Change state of all
          ansibleguy.opnsense.alias_multi:
            aliases:
              test1:
              test3:
            state: 'absent'
            # enabled: true

        - name: Listing
          ansibleguy.opnsense.list:
          #  target: 'alias'
          register: existing_entries

        - name: Printing aliases
          ansible.builtin.debug:
            var: existing_entries.data

        - name: Purging all non-configured aliases
          ansibleguy.opnsense.alias_purge:
            aliases: {...}
            # action: 'disable'  # default = remove

        - name: Purging all port aliases
          ansibleguy.opnsense.alias_purge:
            filters:  # filtering aliases to purge by alias-parameters
              type: 'port'
            # filter_invert: true  # purge all non-port aliases
