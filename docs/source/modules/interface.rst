.. _modules_interface:

.. include:: ../_include/head.rst

=========
Interface
=========


**STATE**: stable

**TESTS**: `vlan <https://github.com/O-X-L/ansible-opnsense/blob/latest/tests/interface_vlan.yml>`_ |
`vxlan <https://github.com/O-X-L/ansible-opnsense/blob/latest/tests/interface_vxlan.yml>`_ |
`vip <https://github.com/O-X-L/ansible-opnsense/blob/latest/tests/interface_vip.yml>`_ |
`lagg <https://github.com/O-X-L/ansible-opnsense/blob/latest/tests/interface_lagg.yml>`_ |
`loopback <https://github.com/O-X-L/ansible-opnsense/blob/latest/tests/interface_loopback.yml>`_ |
`gre <https://github.com/O-X-L/ansible-opnsense/blob/latest/tests/interface_gre.yml>`_ |
`bridge <https://github.com/O-X-L/ansible-opnsense/blob/latest/tests/interface_bridge.yml>`_ |
`gif <https://github.com/O-X-L/ansible-opnsense/blob/latest/tests/interface_gif.yml>`_

**API Docs**: `Core - Interfaces <https://docs.opnsense.org/development/api/core/interfaces.html>`_

**Service Docs**: `VLAN Docs <https://docs.opnsense.org/manual/other-interfaces.html?highlight=vlan#vlan>`_ |
`VxLAN Docs <https://docs.opnsense.org/manual/other-interfaces.html?highlight=vlan#vxlan>`_ |
`VIP Docs <https://docs.opnsense.org/manual/firewall_vip.html>`_ |
`LAGG Docs <https://docs.opnsense.org/manual/other-interfaces.html?highlight=lagg#lagg>`_ |
`GRE Docs <https://docs.opnsense.org/manual/other-interfaces.html?highlight=gre#gre>`_ |
`Bridge Docs <https://docs.opnsense.org/manual/other-interfaces.html?highlight=bridge#bridge>`_ |
`GIF Docs <https://docs.opnsense.org/manual/other-interfaces.html?highlight=gif#gif>`_


Info
****

oxlorg.opnsense.interface_assignment
==================================

This module manages interface assigned that can be found in the WEB-UI menu: 'Interfaces - Assignments'

oxlorg.opnsense.interface_vlan
==================================

This module manages VLAN configuration that can be found in the WEB-UI menu: 'Interfaces - Devices - VLAN'

oxlorg.opnsense.interface_vxlan
===================================

This module manages VXLAN configuration that can be found in the WEB-UI menu: 'Interfaces - Devices - VXLAN'

oxlorg.opnsense.interface_vip
=================================

This module manages VIP configuration that can be found in the WEB-UI menu: 'Interfaces - Virtual IPs - Settings'

oxlorg.opnsense.interface_lagg
==================================

This module manages LAGG configuration that can be found in the WEB-UI menu: 'Interfaces - Devices - LAGG'

oxlorg.opnsense.interface_loopback
======================================

This module manages Loopback configuration that can be found in the WEB-UI menu: 'Interfaces - Devices - Loopback'

oxlorg.opnsense.interface_gre
=================================

This module manages GRE Tunnel configuration that can be found in the WEB-UI menu: 'Interfaces - Devices - GRE'

oxlorg.opnsense.interface_bridge
====================================

This module manages Bridge configuration that can be found in the WEB-UI menu: 'Interfaces - Devices - Bridge'

oxlorg.opnsense.interface_gif
=================================

This module manages GIF Tunnel configuration that can be found in the WEB-UI menu: 'Interfaces - Devices - GIF'


Contribution
************

Thanks to `@jiuka <https://github.com/jiuka>`_ for developing the :code:`interface_loopback` and :code:`interface_gre` modules!

Thanks to `@Rath <https://github.com/superstes>`_ for developing the other modules!

----

Definition
**********

.. include:: ../_include/param_basic.rst

oxlorg.opnsense.interface_assignment
==================================

.. warning::

    This feature is only available in OPNsense version >= 26.7

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "identifier","string", "false for creation,else true","\-","id","Technical identifier of the interface, used by hasync for example. "
    "description","string","false","\-","desc","You may enter a description here for your reference (not parsed)"
    "device","string","false ","\-","if","Device name to connect this interface to."
    "lock","boolean","false","\-","\-","Prevent interface removal."
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

oxlorg.opnsense.interface_vlan
==================================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "description","string","true","\-","desc, name","The unique description used to match the configured entries to the existing ones"
    "interface","string","false for state changes, else true","\-","parent, port, int, if","The parent interface to add the vlan to. Existing VLAN capable interface - you must provide the network port as shown in 'Interfaces - Assignments - Network port'"
    "vlan","integer","false for state changes, else true","\-","tag, id","802.1Q VLAN tag (between 1 and 4094)"
    "priority","integer","false","0","prio","802.1Q VLAN PCP (between 0 and 7)"
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst


oxlorg.opnsense.interface_vxlan
===================================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "id","integer","true","\-","vxlanid, vni","The unique ID of the VxLAN"
    "interface","string","false for state changes, else true","\-","vxlandev, device, int","Optionally set an interface to bind the VxLAN to. You must provide the network port as shown in 'Interface - Assignments - Interface ID (in brackets)'"
    "local","string","false for state changes, else true","\-","source_address, source_ip, vxlanlocal, source, src","Source IP for the VxLAN tunnel. The source address used in the encapsulating IPv4/IPv6 header. The address should already be assigned to an existing interface. When the interface is configured in unicast mode, the listening socket is bound to this address."
    "local_port","integer","false","\-","source_port, vxlanlocalport, srcport","Define the port to be used"
    "remote","string","false","\-","remote_address, remote_ip, destination, vxlanremote, dest","Remote IP for the VxLAN tunnel - if unicast is used. The interface can be configured in a unicast, or point-to-point, mode to create a tunnel between two hosts. This is the IP address of the remote end of the tunnel."
    "remote_port","integer","false","\-","destination_port, vxlanremoteport, destport","Define the port to be used"
    "group","string","false","\-","multicast_group, multicast_address, multicast_ip, vxlangroup","Remote IP for the VxLAN tunnel - if multicast is used. The interface can be configured in a multicast mode to create a virtual network of hosts. This is the IP multicast group address the interface will join."
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst


oxlorg.opnsense.interface_vip
=================================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "match_fields","list","false","['address', 'interface']","\-","Fields that are used to match configured VIPs with the running config - if any of those fields are changed, the module will think it's a new entry. At least one of: 'address', 'interface', 'cidr', 'description'"
    "address", "string", "true", "\-", "addr, ip, network, net", "Provide an address and subnet to use. (e.g 192.168.0.1/24)"
    "interface", "string", "true", "\-", "port, int, if", "Existing interface - you must provide the network port as shown in 'Interfaces - Assignments - Network port'"
    "mode", "string", "false", "ipalias", "m", "One of: 'ipalias', 'carp', 'proxyarp', 'other'"
    "expand", "boolean", "false", "true", "\-", "\-"
    "bind", "boolean", "false", "true", "\-", "Assigning services to the virtual IP's interface will automatically include this address. Uncheck to prevent binding to this address instead"
    "gateway", "string", "false", "\-", "gw", "For some interface types a gateway is required to configure an IP Alias (ppp/pppoe/tun), leave this field empty for all other interface types"
    "password", "string", "false", "\-", "pwd", "VHID group password"
    "vhid", "integer", "false", "\-", "group, grp, id", "VHID group that the machines will share"
    "advertising_base", "integer", "false", "1", "adv_base, base", "The frequency that this machine will advertise. 0 usually means master. Otherwise the lowest combination of both values in the cluster determines the master"
    "advertising_skew", "integer", "false", "0", "adv_skew, skew", "\-"
    "description","string","false","\-","desc, name","Optional description"
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst


oxlorg.opnsense.interface_lagg
==================================

.. warning::

    This feature is only available in OPNsense version >= 23.7

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "match_fields","list","false","['members']","\-","Fields that are used to match configured LAGG with the running config - if any of those fields are changed, the module will think it's a new entry. At least one of: 'device', 'members', 'primary_member', 'proto', 'description'"
    "device", "string", "false", "\-", "laggif", "Optional 'device' of the entry. Needs to start with 'lagg'"
    "members", "list", "false", "\-", "port, int, if", "Existing LAGG capable interface - you must provide the network port as shown in 'Interfaces - Assignments - Network port'"
    "primary_member", "string", "false", "\-", "\-", "This interface will be added first in the lagg making it the primary one - you must provide the network port as shown in 'Interfaces - Assignments - Network port'"
    "proto", "string", "false", "lacp", "p", "The protocol to use. One of: 'none', 'lacp', 'failover', 'fec', 'loadbalance', 'roundrobin'"
    "lacp_fast_timeout", "boolean", "false", "false", "\-", "Enable lacp fast-timeout on the interface."
    "use_flowid", "string", "false", "\-", "\-", "Use the RSS hash from the network card if available, otherwise a hash is locally calculated. The default depends on the system tunable in net.link.lagg.default_use_flowid. One of: 'default', 'yes', 'no'"
    "lagghash", "list", "false", "['l2']", "\-", "Set the packet layers to hash for aggregation protocols which load balance. At least one of: 'l2', 'l3', 'l4'"
    "lacp_strict", "string", "false", "\-", "\-", "Enable lacp strict compliance on the interface. The default depends on the system tunable in net.link.lagg.lacp.default_strict_mode. One of: 'default', 'yes', 'no'"
    "mtu", "integer", "false", "false", "\-", "If you leave this field blank, the smallest mtu of this laggs children will be used."
    "description","string","true","\-","desc, name","The description used to match the configured entries to the existing ones"
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

oxlorg.opnsense.interface_loopback
======================================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "description","string","true","\-","desc, name","The unique description used to match the configured entries to the existing ones"
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

oxlorg.opnsense.interface_gre
=================================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "description","string","true","\-","desc, name","The unique description used to match the configured entries to the existing ones"
    "local","string","true","\-","l, local_addr","The local address or interface to use."
    "remote","string","true","\-","r, remote_addr","Peer address where encapsulated gre packets will be sent."
    "tunnel_local","string","true","\-","tl, tunnel_local_addr","Local gre tunnel endpoint."
    "tunnel_remote","string","true","\-","tr, tunnel_remote_addr","Remote gre tunnel endpoint."
    "tunnel_remote_net","integer","false","32","\-","Netmask `ipv4` or prefix `ipv6` to use for this tunnel "
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

oxlorg.opnsense.interface_bridge
====================================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "description","string","true","\-","desc, name","The unique description used to match the configured entries to the existing ones"
    "members","list","false","\-","ports, ints","Interfaces participating in the bridge. - you must provide the network port as shown in 'Interfaces - Assignments - Network port"
    "link_local","boolean","false","false","\-","Enable link-local addresses on the interface"
    "stp","boolean","false","false","\-","Enable spanning tree options for this bridge"
    "stp_proto","string","false","rstp","\-","Protocol used for spanning tree. One of: 'rstp' or 'stp'"
    "stp_interfaces","list","false","\-","stp_ports, stp_ints","Interfaces to enable Spanning Tree Protocol on"
    "stp_max_age","integer","false","\-","\-","Time that a Spanning Tree Protocol configuration is valid"
    "stp_fwdelay","integer","false","\-","\-","Time that must pass before an interface begins forwarding packets"
    "stp_hold","integer","false","\-","\-","Tansmit hold count for Spanning Tree"
    "cache_size","integer","false","\-","\-","Size of the bridge address cache"
    "cache_timeout","integer","false","\-","\-","Timeout of address cache entries"
    "span_interfaces","list","false","\-","span_ports, span_ints","Interfaces to add as span ports"
    "edge_interfaces","list","false","\-","edge_ports, edge_ints","Interfaces to set as edge ports"
    "auto_edge_interfaces","list","false","\-","auto_edge_ports, auto_edge_ints","Allow selected interfaces to automatically detect edge status"
    "ptp_interfaces","list","false","\-","ptp_ports, ptp_ints","Interfaces to set as point-to-point link"
    "auto_ptp_interfaces","list","false","\-","auto_ptp_ports, auto_ptp_ints","Automatically detect the point-to-point status on selected interfaces"
    "static_interfaces","list","false","\-","static_ports, static_ints, sticky_interfaces, sticky_ports, sticky_ints","Mark interfaces as a 'sticky' interface."
    "private_interfaces","list","false","\-","private_ports, private_ints","Mark interfaces as a 'private' interface"
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

oxlorg.opnsense.interface_gif
=================================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "description","string","true","\-","desc, name","The unique description used to match the configured entries to the existing ones"
    "local","string","true","\-","l, local_addr","The local address or interface to use."
    "remote","string","true","\-","r, remote_addr","Peer address where encapsulated gre packets will be sent."
    "tunnel_local","string","true","\-","tl, tunnel_local_addr","Local gre tunnel endpoint."
    "tunnel_remote","string","true","\-","tr, tunnel_remote_addr","Remote gre tunnel endpoint."
    "tunnel_remote_net","integer","false","32","\-","Netmask `ipv4` or prefix `ipv6` to use for this tunnel "
    "ingress_filtering","boolean","false","true","filtering","Enable ingress filtering on outer tunnel"
    "ecn_friendly","boolean","false","false","ecn","Enable ECN friendly behavior this violates RFC2893"
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

----

Examples
********

oxlorg.opnsense.interface_vlan
==================================

.. code-block:: yaml
    
    - hosts: firewalls
      connection: local
      gather_facts: false
      module_defaults:
        group/oxlorg.opnsense.all:
          firewall: 'opnsense.template.opnsense.oxl.app'
          api_credential_file: '/home/guy/.secret/opn.key'
    
        oxlorg.opnsense.list:
          target: 'interface_vlan'

oxlorg.opnsense.interface_vlan
==================================

.. code-block:: yaml

    - hosts: firewalls
      connection: local
      gather_facts: false
      module_defaults:
        group/oxlorg.opnsense.all:
          firewall: 'opnsense.template.opnsense.oxl.app'
          api_credential_file: '/home/guy/.secret/opn.key'
    
        oxlorg.opnsense.list:
          target: 'interface_assignment'
    
      tasks:
        - name: Assign a physical device
          oxlorg.opnsense.interface_assignment:
            description: 'example'
            interface: 'vtnet2'
               
        - name: Assign a VLAN
          oxlorg.opnsense.interface_assignment:
            description: 'test1'
            interface: '"vlan0.20"'
    
        - name: Listing
          oxlorg.opnsense.list:
          register: existing_entries
    
        - name: Printing Assignments
          ansible.builtin.debug:
            var: existing_entries.data
    
        - name: Removing VLAN
          oxlorg.opnsense.interface_vlan:
            identifier: 'opt2'
            state: 'absent'

oxlorg.opnsense.interface_vxlan
===================================

.. code-block:: yaml

    - hosts: firewalls
      connection: local
      gather_facts: false
      module_defaults:
        group/oxlorg.opnsense.all:
          firewall: 'opnsense.template.opnsense.oxl.app'
          api_credential_file: '/home/guy/.secret/opn.key'
    
        oxlorg.opnsense.list:
          target: 'interface_vxlan'
    
      tasks:
        - name: Example
          oxlorg.opnsense.interface_vxlan:
            id: 100
            local: '192.168.0.1'
            # remote: ''
            # group: ''
            # interface: 'lan'
            # debug: false
            # state: 'present'
            # reload: true
    
        - name: Adding VxLAN
          oxlorg.opnsense.interface_vxlan:
            id: 100
            local: '192.168.0.1'
            interface: 'lan'
    
        - name: Listing
          oxlorg.opnsense.list:
          #  target: 'interface_vxlan'
          register: existing_entries
    
        - name: Printing VxLANs
          ansible.builtin.debug:
            var: existing_entries.data
    
        - name: Removing VxLAN
          oxlorg.opnsense.interface_vxlan:
            id: 100
            state: 'absent'

oxlorg.opnsense.interface_vip
=================================

.. code-block:: yaml

    - hosts: firewalls
      connection: local
      gather_facts: false
      module_defaults:
        group/oxlorg.opnsense.all:
          firewall: 'opnsense.template.opnsense.oxl.app'
          api_credential_file: '/home/guy/.secret/opn.key'
    
        oxlorg.opnsense.list:
          target: 'interface_vip'
    
      tasks:
        - name: Example
          oxlorg.opnsense.interface_vip:
            interface: 'opt1'
            address: '192.168.0.100/24'
            # match_fields: ['address', 'interface]
            # mode: 'ipalias'
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
          oxlorg.opnsense.interface_vip:
            interface: 'opt1'
            address: '192.168.0.100/24'
            mode: 'carp'
            vhid: 10
            password: 'secret'
    
        - name: Listing
          oxlorg.opnsense.list:
          #  target: 'interface_vip'
          register: existing_entries
    
        - name: Printing VIPs
          ansible.builtin.debug:
            var: existing_entries.data
    
        - name: Removing VIP
          oxlorg.opnsense.interface_vip:
            interface: 'opt1'
            address: '192.168.0.100/24'
            state: 'absent'

oxlorg.opnsense.interface_lagg
==================================

.. code-block:: yaml

    - hosts: firewalls
      connection: local
      gather_facts: false
      module_defaults:
        group/oxlorg.opnsense.all:
          firewall: 'opnsense.template.opnsense.oxl.app'
          api_credential_file: '/home/guy/.secret/opn.key'
    
        oxlorg.opnsense.list:
          target: 'interface_lagg'
    
      tasks:
        - name: Example
          oxlorg.opnsense.interface_lagg:
            # device: lagg0
            # description: LACP ax0/1
            members:
              - ax0
              - ax1
            # primary_member: ax0
            # proto: lacp
            # lacp_fast_timeout: 'default'
            # use_flowid: 'default'
            # lagghash: ['l2']
            # lacp_strict: 'default'
            # mtu: 9000
            # match_fields: ['members']
    
        - name: Adding LAGG
          oxlorg.opnsense.interface_lagg:
            members:
              - ax0
              - ax1
    
        - name: Listing
          oxlorg.opnsense.list:
          #  target: 'interface_lagg'
          register: existing_entries
    
        - name: Printing LAGGs
          ansible.builtin.debug:
            var: existing_entries.data
    
        - name: Removing LAGG
          oxlorg.opnsense.interface_lagg:
            device: lagg0
            match_fields: ['device']
            state: 'absent'

oxlorg.opnsense.interface_loopback
======================================

.. code-block:: yaml

    - hosts: firewalls
      connection: local
      gather_facts: false
      module_defaults:
        group/oxlorg.opnsense.all:
          firewall: 'opnsense.template.opnsense.oxl.app'
          api_credential_file: '/home/guy/.secret/opn.key'
    
        oxlorg.opnsense.list:
          target: 'interface_loopback'
    
      tasks:
        - name: Example
          oxlorg.opnsense.interface_loopback:
            description: 'MyLoopback'
            # debug: false
            # state: 'present'
            # reload: true
    
        - name: Adding Loopback
          oxlorg.opnsense.interface_loopback:
            description: 'MyLoopback'
    
        - name: Listing
          oxlorg.opnsense.list:
          #  target: 'interface_loopback'
          register: existing_entries
    
        - name: Printing Loopbacks
          ansible.builtin.debug:
            var: existing_entries.data
    
        - name: Removing Loopback
          oxlorg.opnsense.interface_loopback:
            description: 'MyLoopback'
            state: 'absent'

oxlorg.opnsense.interface_gre
=================================

.. code-block:: yaml

    - hosts: firewalls
      connection: local
      gather_facts: false
      module_defaults:
        group/oxlorg.opnsense.all:
          firewall: 'opnsense.template.opnsense.oxl.app'
          api_credential_file: '/home/guy/.secret/opn.key'
    
        oxlorg.opnsense.list:
          target: 'interface_gre'
    
      tasks:
        - name: Example
          oxlorg.opnsense.interface_gre:
            description: 'MyGRETunnel'
            local: 'lan'
            remote: '192.168.100.1'
            tunnel_local: '10.0.0.1'
            tunnel_remote: '10.0.0.2'
            # tunnel_remote_net: 32
            # debug: false
            # state: 'present'
            # reload: true
    
        - name: Adding GRE Tunnel
          oxlorg.opnsense.interface_gre:
            description: 'MyGRETunnel'
            local: 'lan'
            remote: '192.168.100.1'
            tunnel_local: '10.0.0.1'
            tunnel_remote: '10.0.0.2'
    
        - name: Listing
          oxlorg.opnsense.list:
          #  target: 'interface_gre'
          register: existing_entries
    
        - name: Printing GRE Tunnels
          ansible.builtin.debug:
            var: existing_entries.data
    
        - name: Removing GRE Tunnel 
          oxlorg.opnsense.interface_gre:
            description: 'MyGRETunnel'
            state: 'absent'

oxlorg.opnsense.interface_bridge
====================================

.. code-block:: yaml

    - hosts: firewalls
      connection: local
      gather_facts: false
      module_defaults:
        group/oxlorg.opnsense.all:
          firewall: 'opnsense.template.opnsense.oxl.app'
          api_credential_file: '/home/guy/.secret/opn.key'
    
        oxlorg.opnsense.list:
          target: 'interface_bridge'
    
      tasks:
        - name: Example
          oxlorg.opnsense.interface_bridge:
            description: 'MyBridge'
            members: 'lan'
            # link_local: false
            # stp: false
            # stp_proto: rstp
            # stp_interfaces:
            # stp_max_age:
            # stp_fwdelay:
            # stp_hold:
            # cache_size:
            # cache_timeout:
            # span_interfaces:
            # edge_interfaces:
            # auto_edge_interfaces:
            # ptp_interfaces:
            # auto_ptp_interfaces:
            # static_interfaces:
            # private_interfaces:
            # debug: false
            # state: 'present'
            # reload: true
    
        - name: Adding Bridge
          oxlorg.opnsense.interface_bridge:
            description: 'MyBridge'
            members: 'lan'
    
        - name: Listing
          oxlorg.opnsense.list:
          #  target: 'interface_bridge'
          register: existing_entries
    
        - name: Printing Bridges
          ansible.builtin.debug:
            var: existing_entries.data
    
        - name: Removing Bridge
          oxlorg.opnsense.interface_bridge:
            description: 'MyBridge'
            state: 'absent'

oxlorg.opnsense.interface_gif
=================================

.. code-block:: yaml

    - hosts: firewalls
      connection: local
      gather_facts: false
      module_defaults:
        group/oxlorg.opnsense.all:
          firewall: 'opnsense.template.opnsense.oxl.app'
          api_credential_file: '/home/guy/.secret/opn.key'
    
        oxlorg.opnsense.list:
          target: 'interface_gif'
    
      tasks:
        - name: Example
          oxlorg.opnsense.interface_gif:
            description: 'MyGIFTunnel'
            local: 'lan'
            remote: '192.168.100.1'
            tunnel_local: '10.0.0.1'
            tunnel_remote: '10.0.0.2'
            # tunnel_remote_net: 32
            # ingres_filtering: true
            # ecn_friendly: false
            # debug: false
            # state: 'present'
            # reload: true
    
        - name: Adding GIF Tunnel
          oxlorg.opnsense.interface_gif:
            description: 'MyGIFTunnel'
            local: 'lan'
            remote: '192.168.100.1'
            tunnel_local: '10.0.0.1'
            tunnel_remote: '10.0.0.2'
    
        - name: Listing
          oxlorg.opnsense.list:
          #  target: 'interface_gif'
          register: existing_entries
    
        - name: Printing GIF Tunnels
          ansible.builtin.debug:
            var: existing_entries.data
    
        - name: Removing GIF Tunnel 
          oxlorg.opnsense.interface_gif:
            description: 'MyGIFTunnel'
            state: 'absent'
