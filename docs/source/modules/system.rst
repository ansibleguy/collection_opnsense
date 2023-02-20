.. _modules_system:

.. include:: ../_include/head.rst

======
System
======

**STATE**: unstable

**TESTS**: `Playbook <https://github.com/ansibleguy/collection_opnsense/blob/latest/tests/system.yml>`_

**API Docs**: `Core - Firmware <https://docs.opnsense.org/development/api/core/firmware.html>`_


Definition
**********

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "action","string","true","\-","Action to execute. One of: 'poweroff', 'reboot', 'update', 'upgrade', 'audit'. **WARNING**: the target firewall will be temporarily unavailable if running action 'upgrade' or 'reboot', or permanently if running action 'poweroff' (;"
    "wait","boolean","false","true","If the module should wait for the action to finish. Available for 'upgrade' and 'reboot'"
    "wait_timeout","int","false","90","Seconds to wait for the action to finish - if 'wait' is enabled"
    "poll_interval","int","false","2","Interval in which to check if the firewall is online"

.. include:: ../_include/param_basic.rst


Examples
********

.. code-block:: yaml

    - hosts: localhost
      gather_facts: no
      module_defaults:
        ansibleguy.opnsense.system:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'

      tasks:
        - name: Reboot the box - will wait until finished
          ansibleguy.opnsense.system:
            action: 'reboot'

        - name: Reboot the box - don't wait
          ansibleguy.opnsense.system:
            action: 'reboot'
            wait: false

        - name: Shutdown the box
          ansibleguy.opnsense.system:
            action: 'poweroff'

        - name: Pull updates
          ansibleguy.opnsense.system:
            action: 'update'

        - name: Start upgrade - will wait until finished
          ansibleguy.opnsense.system:
            action: 'upgrade'
            timeout: 120  # depends on your download speed and firmware-version

        - name: Run audit
          ansibleguy.opnsense.system:
            action: 'audit'
