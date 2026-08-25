.. _modules_dhcp:

.. include:: ../_include/head.rst

====
DHCP
====

**STATE**: stable

**TESTS**: `Reservation <https://github.com/O-X-L/ansible-opnsense/blob/latest/tests/dhcp_reservation.yml>`_ |
`ControlAgent <https://github.com/O-X-L/ansible-opnsense/blob/latest/tests/dhcp_controlagent.yml>`_ |
`Subnet <https://github.com/O-X-L/ansible-opnsense/blob/latest/tests/dhcp_subnet.yml>`_ |
`General <https://github.com/O-X-L/ansible-opnsense/blob/latest/tests/dhcp_general.yml>`_ |
`DDNS <https://github.com/O-X-L/ansible-opnsense/blob/latest/tests/kea_ddns.yml>`_

**API Docs**: `Core - KEA <https://docs.opnsense.org/development/api/core/kea.html>`_

**Service Docs**: `DHCP <https://docs.opnsense.org/manual/dhcp.html#kea-dhcp>`_

Contribution
************

Thanks to `@KalleDK <https://github.com/KalleDK>`_, `@Rath <https://github.com/superstes>`_ and `@woelfle <https://github.com/woelfle>`_ for developing these modules!

----

Definition
**********

.. include:: ../_include/param_basic.rst

oxlorg.opnsense.dhcp_general
================================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "interfaces","list","false","\-","ints","Comma separated list of network interfaces to listen on for DHCP requests"
    "socket_type","string","false","raw","dhcp_socket_type","One of: 'raw', 'udp'. Socket type used for DHCP communication."
    "fw_rules","boolean","false","true","fwrules, rules","Automatically add a basic set of firewall rules to allow DHCP traffic"
    "lifetime","int","false","4000","valid_lifetime","Defines how long the addresses (leases) given out by the server are valid (in seconds)"

oxlorg.opnsense.dhcp_reservation
====================================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "ip","string","true","","ip_address","IP address to offer to the client"
    "mac","string","false for state changes, else true","","mac_address","MAC/Ether address of the client in question"
    "subnet","string","false for state changes, else true","","\-","Subnet this reservation belongs to"
    "hostname","string","false","","\-","Offer a hostname to the client"
    "description","string","false","","\-","Optional description"
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

oxlorg.opnsense.dhcp_controlagent
=====================================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "enabled","boolean","false","true","\-","Enable or disable the control agent"
    "http_host","string","false","127.0.0.1","","Address on which the RESTful interface should be available"
    "http_port","int","false","8000","","MAC/Ether address of the client in question"
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

oxlorg.opnsense.dhcp_subnet
===============================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "subnet","string","true","\-","\-","Subnet to use. should be large enough to hold the specified pools and reservations"
    "description","string","false","\-","desc","Optional description of the subnet"
    "pools","list","false","\-","\-","List of pools, one per line in range or subnet format (e.g. 192.168.0.100 - 192.168.0.200)"
    "auto_options","boolean","false","true","option_data_autocollect","Automatically update option data for relevant attributes as routers, dns servers and ntp servers when applying settings from the gui."
    "gateway","list","false","\-","gw,routers","Default gateways to offer to the clients"
    "routes","string","false","\-","static_routes","Static routes that the client should install in its routing cache, defined as dest-ip1,router-ip1;dest-ip2,router-ip2"
    "dns","list","false","\-","dns_servers,dns_srv","DNS servers to offer to the clients"
    "domain","string","false","\-","domain_name,dom_name,dom","The domain name to offer to the client, set to this firewall's domain name when left empty"
    "domain_search","list","false","\-","dom_search","Specifies a 'search list' of Domain Names to be used by the client to locate not-fully-qualified domain names."
    "ntp_servers","list","false","\-","ntp_srv,ntp","Specifies a list of IP addresses indicating NTP (RFC 5905) servers available to the client."
    "time_servers","list","false","\-","time_srv","Specifies a list of RFC 868 time servers available to the client."
    "next_server","string","false","\-","next_srv","Next server IP address"
    "tftp_server","string","false","\-","tftp,tftp_srv,tftp_server_name","TFTP server address or fqdn"
    "tftp_file","string","false","\-","tftp_boot_file,boot_file_name","TFTP Boot filename to request"
    "ipv","int","false","4","ip_version","IP version - one of '4', '6'"
    "v6_only_preferred","boolean","false","false","v6_preferred","If clients should prefer IPv6 over IPv4"

oxlorg.opnsense.kea_ddns
============================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "enabled","boolean","false","true","\-","Enable or disable the Kea DHCP DDNS service"
    "server_ip","string","false","127.0.0.1","host","Address on which the DHCP DDNS server interface should be available"
    "server_port","int","false","53001","port","Portnumber to use for the DHCP DDNS server interface"
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

----

Examples
********

oxlorg.opnsense.dhcp_general
================================

.. code-block:: yaml

      - hosts: firewalls
      connection: local
        gather_facts: no
        module_defaults:
          group/oxlorg.opnsense.all:
            firewall: 'opnsense.template.opnsense.oxl.app'
            api_credentials_file: '/home/guy/.secret/opn.key'

        tasks:
          - name: Listen to network interfaces
            oxlorg.opnsense.dhcp_general:
              enabled: true
              interfaces: 'lan,opt1,opt2,vlan0.10'
              # socket_type: 'raw'
              # fw_rules: true
              # lifetime: 4000

----

oxlorg.opnsense.dhcp_reservation
====================================

.. code-block:: yaml

    - hosts: firewalls
      connection: local
      gather_facts: no
      module_defaults:
        group/oxlorg.opnsense.all:
          firewall: 'opnsense.template.opnsense.oxl.app'
          api_credential_file: '/home/guy/.secret/opn.key'

        oxlorg.opnsense.list:
          target: 'dhcp_reservation'

      tasks:
        - name: Example
          oxlorg.opnsense.dhcp_reservation:
            ip: '192.168.0.1'
            subnet: '192.168.0.0/24'
            mac: 'aa:aa:aa:bb:bb:bb'
            # hostname: 'test'
            # description: ''
            # state: 'present'
            # reload: true
            # debug: false

        - name: Adding
          oxlorg.opnsense.dhcp_reservation:
            subnet: '192.168.0.0/24'
            ip: '192.168.0.1'
            mac: 'aa:aa:aa:bb:bb:bb'

        - name: Removing
          oxlorg.opnsense.dhcp_reservation:
            ip: '192.168.0.1'
            state: 'absent'

        - name: Listing
          oxlorg.opnsense.list:
          #  target: 'dhcp_reservation'
          register: existing_entries

        - name: Show existing reservations
          ansible.builtin.debug:
            var: existing_entries.data

----

oxlorg.opnsense.dhcp_controlagent
=====================================

.. code-block:: yaml

    - hosts: firewalls
      connection: local
      gather_facts: no
      module_defaults:
        group/oxlorg.opnsense.all:
          firewall: 'opnsense.template.opnsense.oxl.app'
          api_credential_file: '/home/guy/.secret/opn.key'

      tasks:
        - name: Example
          oxlorg.opnsense.dhcp_controlagent:
            enabled: true
            http_host: 127.0.0.1
            http_port: 8000
            # reload: true
            # debug: false

        - name: Stopping
          oxlorg.opnsense.dhcp_controlagent:
            enabled: false
            reload: true

----

oxlorg.opnsense.dhcp_subnet
===============================

.. code-block:: yaml

    - host: firewalls
      connection: local
      gather_facts: false
      module_defaults:
        group/oxlorg.opnsense.all:
          firewall: 'opnsense.template.opnsense.oxl.app'
          api_credential_file: '/home/guy/.secret/opn.key'

        oxlorg.opnsense.list:
          target: 'dhcp_reservation'

      tasks:
        - name: Example
          oxlorg.opnsense.dhcp_subnet:
            subnet: '192.168.89.0/24'
            # description: ''
            # pools: []
            # auto_options: true
            # gateway: ''
            # routes: ''
            # dns: []
            # domain: ''
            # domain_search: []
            # ntp_servers: []
            # time_servers: []
            # next_server: ''
            # tftp_server: ''
            # tftp_file: ''
            # ipv: 4
            # v6_only_preferred: false
            # match_fields: ['subnet']

        - name: Add subnet
          oxlorg.opnsense.dhcp_subnet:
            subnet: '10.0.100.0/24'
            pools:
              - '10.0.100.1-10.0.100.99'
              - '10.0.100.150-10.0.100.199'
            auto_options: false
            gateway: '192.168.89.254'
            dns: ['1.1.1.2', '1.0.0.2']
            domain: 'test.lan'

        - name: Remove subnet
          oxlorg.opnsense.dhcp_subnet:
            subnet: '10.0.100.0/24'
            state: absent

----

oxlorg.opnsense.kea_ddns
============================

.. code-block:: yaml

    - hosts: firewalls
      connection: local
      gather_facts: false
      module_defaults:
        group/oxlorg.opnsense.all:
          firewall: 'opnsense.template.opnsense.oxl.app'
          api_credential_file: '/home/guy/.secret/opn.key'

      tasks:
        - name: Example
          oxlorg.opnsense.kea_ddns:
            enabled: true
            server_ip: '127.0.0.1'
            server_port: 53001
            # reload: true
            # debug: false

        - name: Stopping
          oxlorg.opnsense.kea_ddns:
            enabled: false
            reload: true
