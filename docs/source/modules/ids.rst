.. _modules_ids:

.. include:: ../_include/head.rst

===========================
Intrusion Prevention System
===========================

**STATE**: unstable

**TESTS**: `ansibleguy.opnsense.ids_general <https://github.com/ansibleguy/collection_opnsense/blob/latest/tests/ids_general.yml>`_,
`ansibleguy.opnsense.ids_action <https://github.com/ansibleguy/collection_opnsense/blob/latest/tests/ids_action.yml>`_,
`ansibleguy.opnsense.ids_policy <https://github.com/ansibleguy/collection_opnsense/blob/latest/tests/ids_policy.yml>`_,
`ansibleguy.opnsense.ids_policy_rule <https://github.com/ansibleguy/collection_opnsense/blob/latest/tests/ids_policy_rule.yml>`_,
`ansibleguy.opnsense.ids_rule <https://github.com/ansibleguy/collection_opnsense/blob/latest/tests/ids_rule.yml>`_,
`ansibleguy.opnsense.ids_ruleset <https://github.com/ansibleguy/collection_opnsense/blob/latest/tests/ids_ruleset.yml>`_,
`ansibleguy.opnsense.ids_ruleset_properties <https://github.com/ansibleguy/collection_opnsense/blob/latest/tests/ids_ruleset_properties.yml>`_,
`ansibleguy.opnsense.ids_user_rule <https://github.com/ansibleguy/collection_opnsense/blob/latest/tests/ids_user_rule.yml>`_,

**API Docs**: `IDS <https://docs.opnsense.org/development/api/core/ids.html>`_

**Service Docs**: `Intrusion Prevention System <https://docs.opnsense.org/manual/ips.html>`_


Definition
**********

.. include:: ../_include/param_basic.rst

ansibleguy.opnsense.ids_action
==============================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "action","string","true","\-","do, a","Action to execute. One of: 'get_alert_info', 'get_alert_logs', 'query_alerts', 'status', 'reconfigure', 'restart', 'start', 'stop', 'drop_alert_log', 'reload_rules', 'update_rules'. These ones return information: 'get_alert_info', 'get_alert_logs', 'query_alerts', 'status'"
    "parameter","string","false","\-","param","Parameter Alert-ID needed for 'get_alert_info'"

ansibleguy.opnsense.ids_general
===============================

Interfaces for 'ids_general' must be provided as used in the network config (_p.e. 'opt1' instead of 'DMZ'_)

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "interfaces","list","true","\-","ints","Select interface(s) to use. When enabling IPS, only use physical interfaces here (no vlans etc)"
    "enabled","boolean","false","true","\-","Enable intrusion detection system"
    "block","boolean","false","false","protection, ips","Enable protection mode (block traffic). Before enabling, please disable all hardware offloading first in advanced network!"
    "promiscuous","boolean","false","\-","physical, vlan","For certain setups (like IPS with vlans), this is required to actually capture data on the physical interface"
    "default_packet_size","int","false","\- (system default)","packet_size","With this option, you can set the size of the packets on your network. It is possible that bigger packets have to be processed sometimes. The engine can still process these bigger packets, but processing it will lower the performance. Unset = system default"
    "local_networks","list","false","['192.168.0.0/16', '10.0.0.0/8', '172.16.0.0/12']","home_networks","Networks to interpret as local"
    "pattern_matcher","string","false","\- (system default)","algorithm, matcher, algo","One of: 'ac', 'ac-bs', 'ac-ks', 'hs'. Select the multi-pattern matcher algorithm to use. Options: unset = system default, 'ac' = 'Aho-Corasick', 'ac-bs' = 'Aho-Corasick, reduced memory implementation', 'ac-ks' = 'Aho-Corasick, Ken Steele variant', 'hs' = 'Hyperscan'"
    "profile","string","false","\- (system default)","detect_profile","One of: 'low', 'medium', 'high', 'custom'. The detection engine builds internal groups of signatures. The engine allow us to specify the profile to use for them, to manage memory on an efficient way keeping a good performance. Unset = system default"
    "profile_toclient_groups","integer","true if profile = 'custom'","\-","toclient_groups","Between 0 and 65535. If Custom is specified. The detection engine tries to split out separate signatures into groups so that a packet is only inspected against signatures that can actually match. As in large rule set this would result in way too many groups and memory usage similar groups are merged together"
    "profile_toserver_groups","integer","true if profile = 'custom'","\-","toserver_groups","Between 0 and 65535. If Custom is specified. The detection engine tries to split out separate signatures into groups so that a packet is only inspected against signatures that can actually match. As in large rule set this would result in way too many groups and memory usage similar groups are merged together"
    "schedule","string","false","'ids rule updates'","update_cron","Name/Description of an existing cron-job that should be used to update IDS"
    "syslog_alerts","boolean","false","\-","syslog, log","Send alerts to system log in fast log format. This will not change the alert logging used by the product itself"
    "syslog_output","boolean","false","\-","log_stdout","Send alerts in eve format to syslog, using log level info. This will not change the alert logging used by the product itself. Drop logs will only be send to the internal logger, due to restrictions in suricata"
    "log_level","string","false","\- (system default)","\-","One of: 'info', 'perf', 'config', 'debug'. Increase the verbosity of the Suricata application logging by increasing the log level from the default. Unset = system default"
    "log_retention","integer","false","4","log_count","Number of logs to keep"
    "log_payload","boolean","false","\-","log_packet","Send packet payload to the log for further analyses"
    "log_rotate","string","false","weekly","\-","One of: 'weekly', 'daily'. Rotate alert logs at provided interval"
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst



Usage
*****

TBD

Examples
********

ansibleguy.opnsense.ids_action
==============================

.. code-block:: yaml

    - hosts: localhost
      gather_facts: false
      module_defaults:
        group/ansibleguy.opnsense.all:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'

      tasks:
        - name: Example
          ansibleguy.opnsense.ids_action:
            action: 'status'
            # debug: false

        - name: Pull Alert Logs
          ansibleguy.opnsense.ids_action:
            action: 'get_alert_logs'
          register: ids_logs

        - name: Printing
          ansible.builtin.debug:
            var: ids_logs.data

        - name: Reload Rules
          ansibleguy.opnsense.ids_action:
            action: 'reload_rules'

        - name: Update Rules
          ansibleguy.opnsense.ids_action:
            action: 'update_rules'


ansibleguy.opnsense.ids_general
===========================

.. code-block:: yaml

    - hosts: localhost
      gather_facts: false
      module_defaults:
        group/ansibleguy.opnsense.all:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'

        ansibleguy.opnsense.list:
          target: 'ids_general'

      tasks:
        - name: Example
          ansibleguy.opnsense.ids_general:
            interfaces: ['opt1']
            # enabled: true
            # block: true
            # promiscuous: false
            # default_packet_size: ''
            # local_networks: ['192.168.0.0/16', '10.0.0.0/8', '172.16.0.0/12']
            # pattern_matcher: ''
            # profile: ''
            # profile_toclient_groups: ''
            # profile_toserver_groups: ''
            # schedule: 'ids rule updates'
            # syslog_alerts: false
            # syslog_output: false
            # log_level: ''
            # log_retention: 4
            # log_payload: false
            # log_rotate: 'weekly'
            # reload: true
            # debug: false

        - name: Enabling IDS (learning mode)
          ansibleguy.opnsense.ids_general:
            interfaces: ['opt1']
            enabled: true
            pattern_matcher: 'ac'
            profile: 'low'
            local_networks: ['10.0.0.0/16']
            log_rotate: 'daily'
            log_retention: 14
            syslog: true
            log_level: 'info'

        - name: Enabling IPS (blocking)
          ansibleguy.opnsense.ids_general:
            interfaces: ['opt1']
            enabled: true
            block: true
            pattern_matcher: 'ac'
            profile: 'low'
            local_networks: ['10.0.0.0/16']
            log_rotate: 'daily'
            log_retention: 14
            syslog: true
            log_level: 'info'

        - name: Listing Settings
          ansibleguy.opnsense.list:
          #  target: 'ids_general'
          register: existing_settings

        - name: Printing Settings
          ansible.builtin.debug:
            var: existing_settings.data
