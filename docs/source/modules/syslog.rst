.. _modules_syslog:

.. include:: ../_include/head.rst

======
Syslog
======

**STATE**: stable

**TESTS**: `Playbook <https://github.com/ansibleguy/collection_opnsense/blob/latest/tests/syslog.yml>`_

**API Docs**: `Core - Syslog <https://docs.opnsense.org/development/api/core/syslog.html>`_


Definition
**********

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "target","string","true","\-","hostname, tgt, server, srv","Server to forward the logs to"
    "port","int","false","514","p","Port to forward the logs to"
    "transport","string","false","udp4","trans, t","Transport protocol to use. One of: 'udp4', 'tcp4', 'udp6', 'tcp6', 'tls4', 'tls6'"
    "level","list","false","['info', 'notice', 'warn', 'err', 'crit', 'alert', 'emerg']","lvl, lv","Log levels to forward. One or multiple of: 'debug', 'info', 'notice', 'warn', 'err', 'crit', 'alert', 'emerg'"
    "program","list","false","\-","prog","Limit applications to send logs from. For options see WEB-UI (*value in brackets needed*)."
    "facility","list","false","\-","fac","Facility to use. One of multiple of: 'kern', 'user', 'mail', 'daemon', 'auth', 'syslog', 'lpr', 'news', 'uucp', 'cron', 'authpriv', 'ftp', 'ntp', 'security', 'console', 'local0', 'local1', 'local2', 'local3', 'local4', 'local5', 'local6', 'local7'"
    "certificate","string","false, true if transport is TLS","\-","cert","Certificate to use for encrypted transport. Provide the certificates ID - not display name."
    "description","string","false","\-","desc","Optional description for the syslog-destination. Could be used as unique-identifier when set as only 'match_field'."
    "match_fields","list","false","['target', 'facility', 'program']","\-","Fields that are used to match configured syslog-destinations with the running config - if any of those fields are changed, the module will think it's a new entry. At least one of: 'target', 'transport', 'facility', 'program', 'level', 'port', 'description'"

.. include:: ../_include/param_basic.rst

Examples
********

.. code-block:: yaml

    - hosts: localhost
      gather_facts: no
      module_defaults:
        ansibleguy.opnsense.syslog:
          firewall: "{{ lookup('ansible.builtin.env', 'TEST_FIREWALL') }}"
          api_credential_file: "{{ lookup('ansible.builtin.env', 'TEST_API_KEY') }}"
          ssl_verify: false
          match_fields: ['description']

        ansibleguy.opnsense.list:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'
          target: 'syslog'

      tasks:
        - name: Example
          ansibleguy.opnsense.syslog:
            target: '192.168.0.1'
            # port: 514
            # transport: 'udp4'
            # level: ['info', 'notice', 'warn', 'err', 'crit', 'alert', 'emerg']
            # program: ['firewall', 'openvpn']
            # facility: ['security']
            # certificate: 'certificate-id'
            # rfc5424: false
            # description: 'example'
            # match_fields: ['target', 'facility', 'program']

        - name: Adding 1
          ansibleguy.opnsense.syslog:
            description: 'test1'
            target: '192.168.0.1'
            # match_fields: ['description']

        - name: Listing
          ansibleguy.opnsense.list:
          #  target: 'syslog'
          register: existing_entries

        - name: Printing entries
          ansible.builtin.debug:
            var: existing_entries.data

Cleanup
=======

Removing all unwanted (*not configured*) entries.

In this example the description is used as unique identifier!

.. code-block:: yaml

    - hosts: localhost
      gather_facts: no
      module_defaults:
        ansibleguy.opnsense.syslog:
          firewall: "{{ lookup('ansible.builtin.env', 'TEST_FIREWALL') }}"
          api_credential_file: "{{ lookup('ansible.builtin.env', 'TEST_API_KEY') }}"
          ssl_verify: false
          match_fields: ['description']

        ansibleguy.opnsense.list:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'
          target: 'syslog'

      vars:
        syslog: {...}

      tasks:
        - name: Listing
          ansibleguy.opnsense.list:
          #  target: 'syslog'
          register: existing_entries

        - name: Purge
          ansibleguy.opnsense.syslog:
            description: "{{ destination.description }}"
            target: "{{ destination.target }}"
            state: 'absent'

          when: destination.description not in syslog | json_query('[*].description')

          loop_control:
            loop_var: destination
          loop: "{{ existing_entries.data }}"
