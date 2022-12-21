.. _usage_troubleshoot:

.. include:: ../_include/head.rst

================
3 - Troubleshoot
================

If you get error messages - you should at first check if there are any errors listed.

Sometimes the error message can be pretty long, therefore you might want to copy its output into an editor of your choice and Strg+F/search for the terms 'Error:' or '_content'!

Per example:

.. code-block:: bash

    # OUTPUT:
    fatal: [localhost]: FAILED! => {"changed": false, "msg": "API call failed | Error: {'rule.interface': 'option not in list'} | Response: {'status_code': 200, 'headers': Headers({'content-type': 'application/json; charset=UTF-8', 'content-length': '73', 'date': 'Tue, 30 Aug 2022 15:17:57 GMT', 'server': 'OPNsense'}), '_request': <Request('POST', 'https://FIREWALL/api/firewall/filter/addRule')>, 'next_request': None, 'extensions': {'http_version': b'HTTP/1.1', 'reason_phrase': b'OK', 'network_stream': <httpcore.backends.sync.SyncStream object at 0x7f7efa1975b0>}, 'history': [], 'is_closed': True, 'is_stream_consumed': True, 'default_encoding': 'utf-8', 'stream': <httpx._client.BoundSyncStream object at 0x7f7efa1b28e0>, '_num_bytes_downloaded': 73, '_decoder': <httpx._decoders.IdentityDecoder object at 0x7f7efa139190>, '_elapsed': datetime.timedelta(microseconds=189718), '_content': b'{\"result\":\"failed\",\"validations\":{\"rule.interface\":\"option not in list\"}}', '_encoding': 'UTF-8', '_text': '{\"result\":\"failed\",\"validations\":{\"rule.interface\":\"option not in list\"}}'}"}

    # ERROR:
    {'rule.interface': 'option not in list'}

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

  Sometimes this 'reload' takes some time as the firewall needs to process some information.

  Per example:

  - URL-Table alias needs to be populated
  - Syslog needs to resolve its DNS-target (*if not able to resolve*)
  
  **What to do about it?**

  If you are calling a module **in a loop** for multiple items - it might be faster to use the :ref:`ansibleguy.opnsense.reload module <modules_reload>` instead.
