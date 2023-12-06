.. _modules_ids:

.. include:: ../_include/head.rst

===========================
Intrusion Prevention System
===========================

**STATE**: unstable

**TESTS**: `ansibleguy.opnsense.ids_general <https://github.com/ansibleguy/collection_opnsense/blob/latest/tests/ids_general.yml>`_,
`ansibleguy.opnsense.ids_action <https://github.com/ansibleguy/collection_opnsense/blob/latest/tests/ids_action.yml>`_,
`ansibleguy.opnsense.ids_policy <https://github.com/ansibleguy/collection_opnsense/blob/latest/tests/ids_policy.yml>`_,
`ansibleguy.opnsense.ids_policy_rule <https://github.com/ansibleguy/collection_opnsense/blob/latest/tests/ids_policy_rule.yml>`_,
`ansibleguy.opnsense.ids_rule <https://github.com/ansibleguy/collection_opnsense/blob/latest/tests/ids_rule.yml>`_,
`ansibleguy.opnsense.ids_ruleset <https://github.com/ansibleguy/collection_opnsense/blob/latest/tests/ids_ruleset.yml>`_,
`ansibleguy.opnsense.ids_ruleset_properties <https://github.com/ansibleguy/collection_opnsense/blob/latest/tests/ids_ruleset_properties.yml>`_,
`ansibleguy.opnsense.ids_user_rule <https://github.com/ansibleguy/collection_opnsense/blob/latest/tests/ids_user_rule.yml>`_,

**API Docs**: `IDS <https://docs.opnsense.org/development/api/core/ids.html>`_

**Service Docs**: `Intrusion Prevention System <https://docs.opnsense.org/manual/ips.html>`_


Definition
**********

.. include:: ../_include/param_basic.rst

ansibleguy.opnsense.ids_action
==============================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "action","string","true","\-","do, a","Action to execute. One of: 'get_alert_info', 'get_alert_logs', 'query_alerts', 'status', 'reconfigure', 'restart', 'start', 'stop', 'drop_alert_log', 'reload_rules', 'update_rules'. These ones return information: 'get_alert_info', 'get_alert_logs', 'query_alerts', 'status'"



Usage
*****

TBD

Examples
********

ansibleguy.opnsense.ids_action
==============================

.. code-block:: yaml

    - hosts: localhost
      gather_facts: false
      module_defaults:
        group/ansibleguy.opnsense.all:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'

      tasks:
        - name: Example
          ansibleguy.opnsense.ids_action:
            action: 'status'
            # debug: false

        - name: Pull Alert Logs
          ansibleguy.opnsense.ids_action:
            action: 'get_alert_logs'
          register: ids_logs

        - name: Printing
          ansible.builtin.debug:
            var: ids_logs.data

        - name: Reload Rules
          ansibleguy.opnsense.ids_action:
            action: 'reload_rules'

        - name: Update Rules
          ansibleguy.opnsense.ids_action:
            action: 'update_rules'


ansibleguy.opnsense.ids_xxx
===========================

.. code-block:: yaml

    - hosts: localhost
      gather_facts: false
      module_defaults:
        group/ansibleguy.opnsense.all:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'

        ansibleguy.opnsense.list:
          target: '<module>'

      tasks:
        - name: Example
          ansibleguy.opnsense.<module>:
            description: 'test1'
            command: 'system remote backup'
            # state: 'absent'
            # debug: false

        - name: Adding something
          ansibleguy.opnsense.<module>:

        - name: Changing something
          ansibleguy.opnsense.<module>:

        - name: Listing jobs
          ansibleguy.opnsense.list:
          #  target: '<module>'
          register: existing_jobs

        - name: Printing
          ansible.builtin.debug:
            var: existing_jobs.data
