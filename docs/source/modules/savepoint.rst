.. _modules_savepoint:

.. include:: ../_include/head.rst

.. |rollback_process| image:: https://docs.opnsense.org/_images/blockdiag-43422f611798118832d099ed58decb1437fb76a0.png

==================
Firewall Savepoint
==================

**STATE**: unstable

**TESTS**: `Playbook <https://github.com/ansibleguy/collection_opnsense/blob/latest/tests/savepoint.yml>`_

**API Docs**: `Core - Firewall <https://docs.opnsense.org/development/api/core/firewall.html>`_


Info
****

You can use those savepoints to prevent lockout-situations when managing rulesets remotely.

Here is the basic process:

|rollback_process|

It currently just works with the 'Firewall' plugin:

- :ref:`ansibleguy.opnsense.rule <modules_rule>`
- :ref:`ansibleguy.opnsense.source_nat <modules_source_nat>`

Definition
**********

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","false","'create'","Action to execute. One of: 'create', 'revert', 'apply', 'cancel_rollback', 'cancel'"
    "revision","string","false, true if action is one of 'apply', 'revert' or 'cancel_rollback'","\-","Savepoint revision to apply, revert or cancel_rollback"
    "controller","string","false","'filter'","Controller to manage the savepoint of. One of: 'source_nat', 'filter'"
    "api_module","string","false","'firewall'","Module to manage the savepoint of. Currently only supports 'firewall'"

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
        - name: Create a savepoint for firewall filters
          ansibleguy.opnsense.savepoint:
            action: 'create'
            controller: 'filter'  # default
          register: filter_savepoint

        - name: Apply savepoint
          ansibleguy.opnsense.savepoint:
            action: 'apply'
            revision: "{{ filter_savepoint.revision }}"

        - name: Revert savepoint
          ansibleguy.opnsense.savepoint:
            action: 'revert'
            revision: "{{ filter_savepoint.revision }}"

        - name: Create a savepoint for firewall source-nat
          ansibleguy.opnsense.savepoint:
            action: 'create'
            controller: 'source_nat'
          register: snat_savepoint

        - name: Remove source-nat savepoint (else it will be reverted automatically)
          ansibleguy.opnsense.savepoint:
            action: 'cancel_rollback'
            controller: 'source_nat'
            revision: "{{ snat_savepoint.revision }}"
