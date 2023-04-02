.. _modules_service:

.. include:: ../_include/head.rst

=======
Service
=======

**STATE**: stable

**TESTS**: `Playbook <https://github.com/ansibleguy/collection_opnsense/blob/latest/tests/service.yml>`_

Info
****

This module can interact with a specified service running on the OPNSense system.

Definition
**********

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","service, target, svc, n","Pretty name of the service to interact with. One of: 'acme_client', 'apcupsd', 'bind', 'captive_portal', 'chrony', 'cicap', 'clamav', 'collectd', 'cron', 'crowdsec', 'dns_crypt_proxy', 'dyndns', 'fetchmail', 'freeradius', 'frr', 'ftp_proxy', 'haproxy', 'hwprobe', 'ids', 'iperf', 'ipsec', 'ipsec_legacy', 'lldpd', 'maltrail', 'mdns_repeater', 'monit', 'munin_node', 'netdata', 'netsnmp', 'nginx', 'node_exporter', 'nrpe', 'ntopng', 'nut', 'openconnect', 'postfix', 'proxy', 'proxysso', 'puppet_agent', 'qemu_guest_agent', 'radsec_proxy', 'redis', 'relayd', 'rspamd', 'shadowsocks', 'shaper', 'siproxd', 'softether', 'sslh', 'stunnel', 'syslog', 'tayga', 'telegraf', 'tftp', 'tinc', 'tor', 'udp_broadcast_relay', 'unbound', 'vnstat', 'wireguard', 'zabbix_agent', 'zabbix_proxy'"
    "action","string","true","\-","do, a","What action to execute. Some services may not support all of these actions (*the module will inform you in that case*). One of: 'status', 'start', 'reload', 'restart', 'stop'"

.. include:: ../_include/param_basic.rst

Examples
********

.. code-block:: yaml

    - hosts: localhost
      gather_facts: no
      module_defaults:
        group/ansibleguy.opnsense.all:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'

      tasks:
        - name: Restarting IPSec service
          ansibleguy.opnsense.service:
            name: 'ipsec'
            action: 'restart'

        - name: Get status of FRR service
          ansibleguy.opnsense.service:
            name: 'frr'
            action: 'status'
          register: frr_svc

        - name: Printing FRR service status
          ansible.builtin.debug:
            var: frr_svc.data

        - name: Stopping Tor service
          ansibleguy.opnsense.service:
            name: 'tor'
            action: 'stop'
