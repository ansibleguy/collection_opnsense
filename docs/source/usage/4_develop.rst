.. _usage_develop:

.. include:: ../_include/head.rst

===========
4 - Develop
===========


The basic API interaction is handled in 'ansibleguy.opnsense.plugins.module_utils.base.api'.

It is a generic abstraction layer for interacting with the api - therefore all plugins should be able to function with it!

API Definition
**************

To get to know the API - you will have to read into the API's XML-config that is linked in `the OPNSense docs <https://docs.opnsense.org/development/api.html#introduction>`_.

Per example: `Alias.xml <https://github.com/opnsense/core/blob/master/src/opnsense/mvc/app/models/OPNsense/Firewall/Alias.xml>`_

As XML isn't the most readable format - I would recommend translating it to YAML or JSON.

Here is a nice online-tool to do so: `XML-to-YAML <https://codebeautify.org/xml-to-yaml>`_ | `XML-to-JSON <https://codebeautify.org/xml-to-json>`_


Module
******

There are `module-templates <https://github.com/ansibleguy/collection_opnsense/blob/latest/plugins/modules/>`_ that can be copied - so you don't have to re-write the basic structure.

Adding new module
*****************

Testing
=======

Copy the test-template '_tmpl.yml' and rename all calls to the new module.

Run the tests like this:

.. code-block:: bash

    # set these variables:
    COL='name-of-new-collection'
    COL_PATH="$(pwd)/../collections/ansible_collections/ansibleguy/opnsense"  # path to your local collection
    TEST_FIREWALL='192.168.0.1'  # ip of your test-firewall
    TEST_API_KEY="$(pwd)/opn.txt"  # api credentials-file for your test-firewall
    export ANSIBLE_DIFF_ALWAYS=yes  # enable diff-mode for debugging

    bash "${COL_PATH}/scripts/test_single.sh" "$TEST_FIREWALL" "$TEST_API_KEY" "$COL_PATH" "$COL" 1



API
***

One can choose to either:

- create a http-session - faster if multiple calls are needed

  p.e. *check current state => create/update/delete*

  .. code-block:: python3

      from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import Session
      session = Session(module=module)
      session.get(cnf={'controller': 'alias', 'command': 'addItem', 'data': {'name': 'dummy', ...}})
      session.post(cnf={'controller': 'alias', 'command': 'delItem', 'params': [uuid]})
      session.close()

- use a single call - if only one is needed

  p.e. toggle a cronjob or restart a service

  .. code-block:: python3

      from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import single_get, single_post
      single_get(
          module=module,
          cnf={'controller': 'alias', 'command': 'addItem', 'data': {'name': 'dummy', ...}}
      )
      single_post(
          module=module,
          cnf={'controller': 'alias', 'command': 'delItem', 'params': [uuid]}
      )

For the controller/command/params/data definition - check the `OPNSense API Docs <https://docs.opnsense.org/development/api.html#core-api>`_!


Debugging
*********

Verbose output
==============

If you want to output something to ansible's runtime - use 'module.warn':

.. code-block:: python3

    module.warn(f"{before} != {after}")

You can also use the 'debug' argument to enable verbose output of the api requests. 

.. code-block:: yaml

    - name: Example
      ansibleguy.opnsense.alias:
        debug: true

'Multi' modules also support the 'debug' parameter on a per-item basis - so you don't get flooded.

When the debug-mode is enabled some useful log files are created in the directory '/tmp/ansibleguy.opnsense'

.. code-block:: bash

    guy$ ls -l /tmp/ansibleguy.opnsense/
    alias.log  # time consumption profiling for the executed module: https://docs.python.org/3/library/profile.html
    api_calls.log  # a list api calls that were executed by the debugged module

Profiling
=========

To profile a modules time-consumption - you can use the existing profiler function:

For it to work, you need to move your modules processing into a dedicated function or object!

The profiler will wrap around this function call and analyze it.

.. code-block:: python3

    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.utils import profiler
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.target_module import process

    PROFILE = True

    if PROFILE:
        profiler(
            check=process, kwargs=dict(
                m=module, p=module.params, r=result,
            ),
            log_file='target_module.log'  # in folder: /tmp/ansibleguy.opnsense/
        )

    else:
        process(m=module, p=module.params, r=result)

Note: these entries can be interpreted as waiting for the responses of HTTP requests:

- 'read' of '_ssl._SSLSocket'
- 'connect' of '_socket.socket'
- 'do_handshake' of '_ssl._SSLSocket'

One can only try to lower the needed HTTP calls.
