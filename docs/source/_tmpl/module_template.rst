.. _modules_<module>:

.. include:: ../_include/head.rst

============
MODULE TITLE
============

**STATE**: unstable

**TESTS**: `Playbook <https://github.com/ansibleguy/collection_opnsense/blob/latest/tests/<module>.yml>`_

**API Docs**: `<module> <https://docs.opnsense.org/development/api/core/<module>.html>`_

**Service Docs**: `<module> <https://docs.opnsense.org/manual/<module>.html>`_


Definition
**********

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "parameter name","parameter type","if is required","default value","aliases","description"
    "placeholder","string","false","\-","\-","Some description"
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

.. include:: ../_include/param_basic.rst

Usage
*****

Basic description of the module.

Place for additional information the user should know of.

Examples
********

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
        # add optional parameters commented-out
        # required ones normally
        # add their default values to get a brief overview of how the module works
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
