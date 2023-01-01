.. _usage_basic:

.. include:: ../_include/head.rst

=========
2 - Basic
=========

Prerequisites
*************

You need to create API credentials as described in the `OPNSense documentation <https://docs.opnsense.org/development/how-tos/api.html#creating-keys>`_.

**Menu**: System - Access - Users - Edit {admin user} - Add api key

SSL Certificate
===============

If you use your firewall for non-testing purposes - you should **ALWAYS USE SSL VERIFICATION** for your connections!

.. code-block:: yaml

    ssl_verify: true

To make a connection trusted you need either:

- a valid public certificate for the DNS-Name your firewall has (*LetsEncrypt/ACME*)
- an internal certificate authority that is used to create signed certificates

  - you could create such internal certificates using OPNSense. See the `OPNSense documentation for self-signed certificates <https://docs.opnsense.org/manual/how-tos/self-signed-chain.html>`_.
  - if you do so - it is important that the IP-address and/or DNS-Name of your firewall is included in the 'Subject Alternative Name' (*SAN*) for it to be valid

After you got a valid certificate - you need to import and activate it:

- Import: 'System - Trust - Certificates - Import'
- Make sure your DNS-Names are allowed: 'System - Settings - Administration - Alternate Hostnames'
- Activate: 'System - Settings - Administration - SSL Certificate'

If you are using an internal CA for your certificates - you have to provide its public key to the modules:

.. code-block:: yaml

    ssl_ca_file: '/path/to/ca.pem'

----

Basics
******

Defaults
========

If some parameters will be the same every time - use 'module_defaults':

.. code-block:: yaml

    - hosts: localhost
      gather_facts: no
      module_defaults:
        ansibleguy.opnsense.alias:
            firewall: 'opnsense.template.ansibleguy.net'
            api_credential_file: '/home/guy/.secret/opn.key'
            # if you use an internal certificate:
            #   ssl_ca_file: '/etc/ssl/certs/custom/ca.crt'
            # else you COULD (but SHOULD NOT) use:
            #   ssl_verify: false

      tasks:
        - name: Example
          ansibleguy.opnsense.alias:
            name: 'ANSIBLE_TEST1'
            content: ['1.1.1.1']

Inventory
=========

If you are running the modules over hosts in your inventory - you would do it like that:

.. code-block:: yaml

    - hosts: firewalls
      connection: local  # execute modules on controller
      gather_facts: no
      tasks:
        - name: Example
          ansibleguy.opnsense.alias:
            firewall: "{{ ansible_host }}"  # or use a per-host variable to store the FQDN..

Vault
=====

You may want to use '**ansible-vault**' to **encrypt** your 'api_secret'.

Vault-Encryption of the 'api_credential_file' is not yet supported.


.. code-block:: bash

    ansible-vault encrypt_string 'YOUR_API_SECRET'

Then add it as variable to your inventory/config:

.. code-block:: yaml

    firewall:
      key: 'test'
      secret: !vault |
        $ANSIBLE_VAULT;1.1;AES256
        38303736393135366562396233353930366631396531613062366365363234363063626365656263
        6637646636323437333437353336316332663133316435650a366439336665383763376432653736
        32313332363032646436626230646461376532666366663265373663316331316664336134366338
        6531363362613039330a316436386533393636623837653163333564383232313363666361643730
        3132

And refer to it in the module calls or module-defaults:

.. code-block:: yaml

    - hosts: localhost
      gather_facts: no
      module_defaults:
        ansibleguy.opnsense.route:
          firewall: '...'
          api_key: "{{ firewall.key }}"
          api_secret: "{{ firewall.secret }}"

To decrypt those secrets at runtime, you need to supply the 'ask-vault-pass' argument:

.. code-block:: bash

    ansible-playbook -D opnsense.yml --ask-vault-pass


Running
=======

These modules support check-mode and can show you the difference between existing and configured items:

.. code-block:: bash

    # show difference
    ansible-playbook opnsense.yml -D

    # run in check-mode (no changes are made)
    ansible-playbook opnsense.yml --check
