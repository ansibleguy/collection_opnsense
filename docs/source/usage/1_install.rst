.. _usage_install:

.. include:: ../_include/head.rst

================
1 - Installation
================


Ansible
*******

See `the documentation <https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#pip-install>`_ on how to install Ansible.

Dependencies
************

The `httpx python module <https://www.python-httpx.org/>`_ is used for API communications!

.. code-block:: bash

    python3 -m pip install httpx


Collection
**********

.. code-block:: bash

    # stable version:
    ansible-galaxy collection install ansibleguy.opnsense

    # latest version:
    ansible-galaxy collection install git+https://github.com/ansibleguy/collection_opnsense.git

    # install to specific director for easier development
    cd $PLAYBOOK_DIR
    ansible-galaxy collection install git+https://github.com/ansibleguy/collection_opnsense.git -p ./collections
