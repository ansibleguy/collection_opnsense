.. _modules_package:

.. include:: ../_include/head.rst

=======
Package
=======

**STATE**: stable

**TESTS**: `Playbook <https://github.com/ansibleguy/collection_opnsense/blob/latest/tests/package.yml>`_

**API Docs**: `Core - Firmware <https://docs.opnsense.org/development/api/core/firmware.html>`_

**Service Docs**: `Plugins <https://docs.opnsense.org/manual/firmware.html#plugins>`_


Info
****

If:

- the package cache is too old, it will take some time - as OPNSense automatically checks for updates beforehand
- the target firewall runs an outdated version, the actions 'install' and 'reinstall' will fail as OPNSense prevents it

  - in that case - you should run :ref:`ansibleguy.opnsense.system <modules_system>` with action 'upgrade'


Be aware that the list-module with target 'package' will return installed plugins AND base-packages.

Definition
**********

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","list of strings","true","\-","Package or list of packages to process"
    "action","string","true","\-","Action to execute. One of: 'install', 'reinstall', 'remove', 'lock', 'unlock'"
    "post_sleep","int","false","3","Seconds to sleep after executing the action. The firewall needs some time to update package info."
    "timeout","float","false","30.0","Seconds until the action request times-out"

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

        ansibleguy.opnsense.list:
          target: 'package'

      tasks:
        - name: Installing
          ansibleguy.opnsense.package:
            name: 'os-api-backup'
            action: 'install'

        - name: Installing - multiple packages at once
          ansibleguy.opnsense.package:
            name: ['os-api-backup', 'os-dmidecode']
            action: 'install'

        - name: Removing
          ansibleguy.opnsense.package:
            name: 'os-api-backup'
            action: 'remove'

        - name: Re-installing
          ansibleguy.opnsense.package:
            name: 'os-api-backup'
            action: 'reinstall'

        - name: Locking
          ansibleguy.opnsense.package:
            name: 'os-api-backup'
            action: 'lock'

        - name: Unlocking
          ansibleguy.opnsense.package:
            name: 'os-api-backup'
            action: 'unlock'

        - name: Listing
          ansibleguy.opnsense.list:
          #  target: 'package'
          register: existing_entries

        - name: Printing installed packages
          ansible.builtin.debug:
            var: existing_entries.data
