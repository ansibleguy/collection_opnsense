.. _modules_radvd:

.. include:: ../_include/head.rst

=====================
Router Advertisements
=====================

**State:** Unstable

**Tests:** `radvd.yml <https://github.com/O-X-L/ansible-opnsense/blob/latest/tests/radvd.yml>`_

**API Docs**: `Core - Router Advertisements <https://docs.opnsense.org/development/api/core/radvd.html>`_

**Service Docs**: `Router Advertisements <https://docs.opnsense.org/manual/radvd.html>`_

Functions
*********

This module manages Router Advertisement Daemon entries on an OPNsense firewall.

Parameters
##########

.. csv-table:: Definition
   :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
   :widths: 15 10 10 10 10 45

   "interface","string","true","\-","\-","Interface that should send router advertisements."
   "enabled","boolean","false","true","\-","Enable or disable this router advertisement entry."
   "base6_interface","string","false","\-","\-","Optional constructor interface for the advertised prefix."
   "mode","choice","false","stateless","\-","Router advertisement mode. One of: 'router', 'unmanaged', 'managed', 'assist', 'stateless'."
   "deprecate_prefix","choice","false","\-","\-","Deprecate the prefix on the interface. One of: '', 'on', 'off'."
   "remove_adv_on_exit","choice","false","\-","\-","Send a final advertisement with zero lifetimes when radvd exits. One of: '', 'on', 'off'."
   "remove_route","choice","false","\-","\-","Remove routes after they expire. One of: '', 'on', 'off'."
   "routes","list","false","[]","\-","Additional IPv6 routes to advertise."
   "rdnss","list","false","[]","\-","Recursive DNS server IPv6 addresses to advertise."
   "dnssl","list","false","[]","\-","DNS search domains to advertise."
   "dns","boolean","false","true","\-","Advertise DNS information."
   "min_rtr_adv_interval","integer","false","200","\-","Minimum time between sending unsolicited multicast router advertisements."
   "max_rtr_adv_interval","integer","false","600","\-","Maximum time between sending unsolicited multicast router advertisements."
   "adv_dnssl_lifetime","integer","false","\-","\-","Lifetime in seconds for advertised DNS search list entries."
   "adv_default_lifetime","integer","false","\-","\-","Lifetime in seconds associated with the default router."
   "adv_link_mtu","integer","false","\-","\-","MTU value to advertise on the link."
   "adv_preferred_lifetime","integer","false","\-","\-","Preferred lifetime in seconds for the advertised prefix."
   "adv_ra_src_address","string","false","\-","\-","Source address to use for router advertisements."
   "adv_rdnss_lifetime","integer","false","\-","\-","Lifetime in seconds for advertised recursive DNS servers."
   "adv_route_lifetime","integer","false","\-","\-","Lifetime in seconds for advertised routes."
   "adv_valid_lifetime","integer","false","\-","\-","Valid lifetime in seconds for the advertised prefix."
   "adv_default_preference","choice","false","medium","\-","Default router preference. One of: 'low', 'medium', 'high'."
   "nat64prefix","string","false","\-","\-","NAT64 IPv6 prefix to advertise."

.. include:: ../_include/param_basic.rst

.. include:: ../_include/param_reload.rst

Usage
*****

Create, update, disable, and remove Router Advertisement Daemon entries.

Examples
********

.. code-block:: yaml

   - hosts: firewalls
     connection: local
     gather_facts: false
     module_defaults:
       group/oxlorg.opnsense.all:
         firewall: 'opnsense.template.oxlorg.net'
         api_credential_file: '/home/guy/.secret/opn.key'

     tasks:
       - name: Create router advertisements for LAN
         oxlorg.opnsense.radvd:
           interface: lan
           mode: stateless
           rdnss:
             - 2001:db8::53
           dnssl:
             - example.net

       - name: Disable router advertisements for LAN
         oxlorg.opnsense.radvd:
           interface: lan
           enabled: false

       - name: Remove router advertisements for LAN
         oxlorg.opnsense.radvd:
           interface: lan
           state: absent
