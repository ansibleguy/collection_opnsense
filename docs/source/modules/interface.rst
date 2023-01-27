.. _modules_interface:

.. include:: ../_include/head.rst

=========
Interface
=========


**STATE**: unstable

**TESTS**: `vlan <https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/interface_vlan.yml>`_ |
`vxlan <https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/interface_vxlan.yml>`_ |
`vip <https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/interface_vip.yml>`_

**API Docs**: `Core - Interfaces <https://docs.opnsense.org/development/api/core/interfaces.html>`_

**Service Docs**: `VLAN Docs <https://docs.opnsense.org/manual/other-interfaces.html?highlight=vlan#vlan>`_ |
`VxLAN Docs <https://docs.opnsense.org/manual/other-interfaces.html?highlight=vlan#vxlan>`_ |
`VIP Docs <https://docs.opnsense.org/manual/firewall_vip.html>`_


Info
****

ansibleguy.opnsense.interface_vlan
==================================

This module manages VLAN configuration that can be found in the WEB-UI menu: 'Interfaces - Other Types - VLAN'

ansibleguy.opnsense.interface_vxlan
===================================

This module manages VXLAN configuration that can be found in the WEB-UI menu: 'Interfaces - Other Types - VXLAN'

ansibleguy.opnsense.interface_vip
===================================

This module manages VIP configuration that can be found in the WEB-UI menu: 'Interfaces - Virtual IPs - Settings'


Definition
**********

.. include:: ../_include/param_basic.rst

ansibleguy.opnsense.interface_vlan
==================================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "description","string","true","\-","desc, name","The unique description used to match the configured entries to the existing ones"
    "interface","string","false for state changes, else true","\-","parent, port, int, if","The parent interface to add the vlan to. Existing VLAN capable interface - you must provide the network port as shown in 'Interfaces - Assignments - Network port'"
    "vlan","integer","false for state changes, else true","\-","tag, id","802.1Q VLAN tag (between 1 and 4094)"
    "priority","integer","false","0","prio","802.1Q VLAN PCP (between 0 and 7)"
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst


ansibleguy.opnsense.interface_vxlan
===================================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "id","integer","true","\-","vxlanid, vni","The unique ID of the VxLAN"
    "interface","string","false for state changes, else true","\-","vxlandev, device, int","Optionally set an interface to bind the VxLAN to. You must provide the network port as shown in 'Interface - Assignments - Interface ID (in brackets)'"
    "local","string","false for state changes, else true","\-","source_address, source_ip, vxlanlocal, source, src","Source IP for the VxLAN tunnel. The source address used in the encapsulating IPv4/IPv6 header. The address should already be assigned to an existing interface. When the interface is configured in unicast mode, the listening socket is bound to this address."
    "remote","string","false","\-","remote_address, remote_ip, destination, vxlanremote, dest","Remote IP for the VxLAN tunnel - if unicast is used. The interface can be configured in a unicast, or point-to-point, mode to create a tunnel between two hosts. This is the IP address of the remote end of the tunnel."
    "group","string","false","\-","multicast_group, multicast_address, multicast_ip, vxlangroup","Remote IP for the VxLAN tunnel - if multicast is used. The interface can be configured in a multicast mode to create a virtual network of hosts. This is the IP multicast group address the interface will join."
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst


ansibleguy.opnsense.interface_vip
=================================

.. warning::

    This feature is only available in OPNSense version >= 23.1

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "match_fields","list","false","['address', 'interface']","\-","Fields that are used to match configured VIPs with the running config - if any of those fields are changed, the module will think it's a new entry. At least one of: 'address', 'interface', 'cidr', 'description'"
    "address", "string", "true", "\-", "addr, ip", "\-"
    "interface", "string", "true", "\-", "port, int, if", "Existing interface - you must provide the network port as shown in 'Interfaces - Assignments - Network port'"
    "mode", "string", "false", "ipalias", "m", "One of: 'ipalias', 'carp', 'proxyarp', 'other'"
    "cidr", "integer", "false", "32", "subnet_bits, subnet", "CIDR of the VIP network"
    "expand", "boolean", "false", "true", "\-", "\-"
    "bind", "boolean", "false", "true", "\-", "Assigning services to the virtual IP's interface will automatically include this address. Uncheck to prevent binding to this address instead"
    "gateway", "string", "false", "\-", "gw", "For some interface types a gateway is required to configure an IP Alias (ppp/pppoe/tun), leave this field empty for all other interface types"
    "password", "string", "false", "\-", "pwd", "VHID group password"
    "vhid", "integer", "false", "\-", "group, grp, id", "VHID group that the machines will share"
    "advertising_base", "integer", "false", "1", "adv_base, base", "The frequency that this machine will advertise. 0 usually means master. Otherwise the lowest combination of both values in the cluster determines the master"
    "advertising_skew", "integer", "false", "0", "adv_skew, skew", "\-"
    "description","string","false","\-","desc, name","Optional description"
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst


Examples
********

ansibleguy.opnsense.interface_vlan
==================================

.. code-block:: yaml

    - hosts: localhost
      gather_facts: no
      module_defaults:
        ansibleguy.opnsense.interface_vlan:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'
    
        ansibleguy.opnsense.list:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'
          target: 'interface_vlan'
    
      tasks:
        - name: Example
          ansibleguy.opnsense.interface_vlan:
            description: 'example'
            interface: 'vtnet0'
            vlan: 100
            # priority: 0
            # debug: false
            # state: 'present'
            # reload: true
    
        - name: Adding VLAN
          ansibleguy.opnsense.interface_vlan:
            description: 'test1'
            interface: 'vtnet0'
            vlan: 100
    
        - name: Listing VLANs
          ansibleguy.opnsense.list:
          #  target: 'interface_vlan'
          register: existing_entries
    
        - name: Printing
          ansible.builtin.debug:
            var: existing_entries.data
    
        - name: Removing VLAN
          ansibleguy.opnsense.interface_vlan:
            description: 'test1'
            state: 'absent'

ansibleguy.opnsense.interface_vxlan
===================================

.. code-block:: yaml

    - hosts: localhost
      gather_facts: no
      module_defaults:
        ansibleguy.opnsense.interface_vxlan:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'
    
        ansibleguy.opnsense.list:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'
          target: 'interface_vxlan'
    
      tasks:
        - name: Example
          ansibleguy.opnsense.interface_vxlan:
            id: 100
            local: '192.168.0.1'
            # remote: ''
            # group: ''
            # interface: 'lan'
            # debug: false
            # state: 'present'
            # reload: true
    
        - name: Adding VxLAN
          ansibleguy.opnsense.interface_vxlan:
            id: 100
            local: '192.168.0.1'
            interface: 'lan'
    
        - name: Listing VxLANs
          ansibleguy.opnsense.list:
          #  target: 'interface_vxlan'
          register: existing_entries
    
        - name: Printing
          ansible.builtin.debug:
            var: existing_entries.data
    
        - name: Removing VxLAN
          ansibleguy.opnsense.interface_vxlan:
            id: 100
            state: 'absent'

ansibleguy.opnsense.interface_vip
=================================

.. code-block:: yaml

    - hosts: localhost
      gather_facts: no
      module_defaults:
        ansibleguy.opnsense.interface_vip:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'
    
        ansibleguy.opnsense.list:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'
          target: 'interface_vip'
    
      tasks:
        - name: Example
          ansibleguy.opnsense.interface_vip:
            interface: 'opt1'
            address: '192.168.0.100'
            # match_fields: ['address', 'interface]
            # mode: 'ipalias'
            # cidr: 32
            # expand: true
            # bind: true
            # gateway: ''
            # password: ''
            # vhid: ''
            # advertising_base: 1
            # advertising_skew: 0
            # description: ''
            # debug: false
            # state: 'present'
            # reload: true
    
        - name: Adding VIP
          ansibleguy.opnsense.interface_vip:
            interface: 'opt1'
            address: '192.168.0.100'
            cidr: 24
            mode: 'carp'
            vhid: 10
            password: 'secret'
    
        - name: Listing VIPs
          ansibleguy.opnsense.list:
          #  target: 'interface_vip'
          register: existing_entries
    
        - name: Printing
          ansible.builtin.debug:
            var: existing_entries.data
    
        - name: Removing VIP
          ansibleguy.opnsense.interface_vip:
            interface: 'opt1'
            address: '192.168.0.100'
            state: 'absent'
