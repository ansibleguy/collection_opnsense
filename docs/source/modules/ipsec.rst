.. _modules_ipsec:

.. include:: ../_include/head.rst

=====
IPSec
=====

**STATE**: unstable

**TESTS**: `ipsec_cert <https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/ipsec_cert.yml>`_

**API Docs**: `Core - IPSec <https://docs.opnsense.org/development/api/core/ipsec.html>`_

**Service Docs**: `Routes <https://docs.opnsense.org/manual/vpnet.html#ipsec>`_


Limitations
***********

We are still `waiting for the API implementation <https://github.com/opnsense/core/pull/6187#issuecomment-1356263118>`_ to manage IPSec tunnels.

Therefor this projects 

Definition
**********

ansibleguy.opnsense.ipsec_cert
==============================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","\-","Name of the key-pair - used to identify the entry."
    "public_key","string","false for state changes, else true","\-","pub_key, pub","\-"
    "private_key","string","false for state changes, else true","\-","priv_key, priv","\-"
    "type","string","false","rsa","\-","Type of the key. Currently the only option is 'rsa'"
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

.. include:: ../_include/param_basic.rst

Usage
*****

To apply changes to the keys, you need to set 'reload: true' on each call or use the :ref:`ansibleguy.opnsense.reload <modules_reload>` module to apply it once you finished modifying all entries!

As far as I can tell - the IPSec service gets restarted one you do so - be aware of that.

Vault
=====

You may want to use '**ansible-vault**' to **encrypt** your 'private_key' content!

.. code-block:: bash

    ansible-vault encrypt_string '-----BEGIN RSA PRIVATE KEY-----\n...-----END RSA PRIVATE KEY-----\n'

    # or encrypt the private_key file beforehand (might be easier)
    ansible-vault encrypt /path/to/private/key/file.pem


Examples
********

.. code-block:: yaml

    - hosts: localhost
      gather_facts: no
      module_defaults:
        ansibleguy.opnsense.ipsec_cert:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'

        ansibleguy.opnsense.list:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'
          target: 'ipsec_cert'

      tasks:
        - name: Example
          ansibleguy.opnsense.ipsec_cert:
            name: 'example'
            public_key: |
              -----BEGIN PUBLIC KEY-----
              ...
              -----END PUBLIC KEY-----
            private_key: |
              -----BEGIN RSA PRIVATE KEY-----
              ...
              -----END RSA PRIVATE KEY-----

            # reload: false

        - name: Adding key-pair and applying it
          ansibleguy.opnsense.ipsec_cert:
            name: 'test1'
            public_key: |
              -----BEGIN PUBLIC KEY-----
              ...
              -----END PUBLIC KEY-----
            private_key: !vault ...
            reload: true

        - name: Listing
          ansibleguy.opnsense.list:
          #  target: 'ipsec_cert'
          no_log: true  # could log private keys
          register: existing_entries

        - name: Printing
          ansible.builtin.debug:
            var: existing_entries.data

        - name: Manually reloading/applying config
          ansibleguy.opnsense.reload:
            target: 'ipsec'
