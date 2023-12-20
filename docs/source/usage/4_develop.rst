.. _usage_develop:

.. include:: ../_include/head.rst

===========
4 - Develop
===========


The basic API interaction is handled in 'ansibleguy.opnsense.plugins.module_utils.base.api'.

It is a generic abstraction layer for interacting with the api - therefore all plugins should be able to function with it!

Install
*******

You can install the collection to a specific directory for easier testing.

.. code-block:: bash

    cd $PLAYBOOK_DIR
    ansible-galaxy collection install git+https://github.com/ansibleguy/collection_opnsense.git,<COMMIT/BRANCH> -p ./collections

Of course you can always place the repository at :code:`${PLAYBOOK_DIR}/ansible_collections/ansibleguy/opnsense` so it gets picked-up by Ansible.

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

**Checklist**:

- Create the module-file at:

  '<COLLECTION>/plugins/modules/<MODULE>.py'

  You can copy the template from '<COLLECTION>/plugins/modules/_tmpl_obj.py'

  Note: When adding module-parameters - you can copy/paste the field-description from the OPNSense web-ui! We don't have to reinvent the wheel. (*'full help' toggle*)

- For most modules you should create a sub-file to handle the actual logic so the main module-file is kept clean:

  '<COLLECTION>/plugins/module_utils/main/<MODULE>.py'

  You can copy the template from '<COLLECTION>/plugins/module_utils/main/_tmpl.py'


- Add **ansible-based tests**:

  I personally like to write tests before adding new modules and testing the modules functionality from the start (test-driven-development)

  - You can copy the template from '<COLLECTION>/tests/_tmpl.yml'

    Rename all calls to the new module.

  - Add a cleanup-task in '<COLLECTION>/tests/cleanup.yml' (set state we will expect when re-running the tests)

  - Enable the test once it runs successfully - add it to '<COLLECTION>/scripts/test.sh'


- Add **documentation**:

  - You can copy the template from '<COLLECTION>/docs/source/_tmpl/module_template.rst' and replace '<module>' and links

    `reStructuredText <https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html>`_ is preferred, but markdown is also supported

    Also add important module-specific information.

  - Optional: We should also add **inline module-documentation** `as standardized for Ansible <https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_documenting.html#documentation-block>`_

    To keep the main module file clean - the documentation should be placed in '<COLLECTION>/plugins/module_utils/inline_docs/'

    You can copy the template from '<COLLECTION>/plugins/module_utils/inline_docs/_tmpl.py'

    You can then import the documentation inside the main module file.


- Add the module to '<COLLECTION>/meta/runtime.yml'


- Add the module as option to the 'ansibleguy.opnsense.list' module:

  '<COLLECTION>/plugins/modules/list.py'


- Add the module as option to the 'ansibleguy.opnsense.reload' module:

  '<COLLECTION>/plugins/modules/reload.py'


- If you are implementing a new service:

  Add the service as option to the 'ansibleguy.opnsense.service' module:

  '<COLLECTION>/plugins/modules/service.py'


Testing
=======


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

You can also use the :code:`debug` argument to enable verbose output of the api requests.

.. code-block:: yaml

    - name: Example
      ansibleguy.opnsense.alias:
        debug: true

'Multi' modules also support the :code:`debug` parameter on a per-item basis - so you don't get flooded.

When the debug-mode is enabled some useful log files are created in the directory :code:`/tmp/ansibleguy.opnsense`

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

    if module.params['profiling']:
        profiler(
            check=process, kwargs=dict(
                m=module, p=module.params, r=result,
            ),
        )

    else:
        process(m=module, p=module.params, r=result)

Note: these entries can be interpreted as waiting for the responses of HTTP requests:

- 'read' of '_ssl._SSLSocket'
- 'connect' of '_socket.socket'
- 'do_handshake' of '_ssl._SSLSocket'

One can only try to lower the needed HTTP calls.
