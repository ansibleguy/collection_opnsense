.. _usage_troubleshoot:

.. include:: ../_include/head.rst

================
3 - Troubleshoot
================

If you get error messages - you should at first check if there are any errors listed.

Sometimes the error message can be pretty long, therefore you might want to copy its output into an editor of your choice and Strg+F/search for the terms :code:`Error:` or :code:`_content`!

Per example:

.. code-block:: bash

    # OUTPUT:
    fatal: [localhost]: FAILED! => {"changed": false, "msg": "API call failed | Error: {'rule.interface': 'option not in list'} | Response: {'status_code': 200, '_request': <Request('POST', 'https://FIREWALL/api/firewall/filter/addRule')>, '_num_bytes_downloaded': 73, '_elapsed': datetime.timedelta(microseconds=189718), '_content': b'{\"result\":\"failed\",\"validations\":{\"rule.interface\":\"option not in list\"}}', '_text': '{\"result\":\"failed\",\"validations\":{\"rule.interface\":\"option not in list\"}}'}"}

    # ERROR:
    {'rule.interface': 'option not in list'}

Verbose output
**************

You can also use the :code:`debug` argument to enable verbose output:

.. code-block:: yaml

    - name: Example
      ansibleguy.opnsense.alias:
        debug: true

When the debug-mode is enabled some useful log files are created in the directory :code:`/tmp/ansibleguy.opnsense` (*HTTP requests made, profiling of time consumption*)

If you only want the profiling logs written, you can also use the :code:`profiling` argument:

.. code-block:: yaml

    - name: Example
      ansibleguy.opnsense.alias:
        profiling: true


'Multi' modules also support these parameters on a per-item basis - so you don't get flooded.

Known errors
************

- 'option not in list' => an invalid option was provided for this parameter
- 'port only allowed for tcp/udp' => any protocol except 'TCP' or 'UDP' provided
- 'ConnectionError: Got timeout calling' => you can override the used timeout manually:

  Per example:

  .. code-block:: yaml

      - name: Example
        ansibleguy.opnsense.alias:
          timeout: 60  # seconds

Known issues
************

- **Module-call taking long**

  Many of the modules need to 'apply' its configuration after a change happened.

  Sometimes this :code:`reload` takes some time as the firewall needs to process some information.

  Per example:

  - URL-Table alias needs to be populated
  - Syslog needs to resolve its DNS-target (*if not able to resolve*)
  
  **What to do about it?**

  If you are calling a module **in a loop** for multiple items - it might be faster to use the :ref:`ansibleguy.opnsense.reload module <modules_reload>` instead.
