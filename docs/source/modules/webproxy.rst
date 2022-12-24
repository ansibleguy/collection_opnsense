.. _modules_webproxy:

.. include:: ../_include/head.rst

=========
Web Proxy
=========

**STATE**: development

**TESTS**: `webproxy_general <https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/webproxy_general.yml>`_ |
`webproxy_cache <https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/webproxy_cache.yml>`_ |
`webproxy_parent <https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/webproxy_parent.yml>`_ |
`webproxy_traffic <https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/webproxy_traffic.yml>`_

**API Docs**: `Core - Proxy <https://docs.opnsense.org/development/api/core/proxy.html>`_

**Service Docs**: `Transparent Proxy <https://docs.opnsense.org/manual/how-tos/proxytransparent.html>`_ |
`Caching Proxy <https://docs.opnsense.org/manual/how-tos/cachingproxy.html>`_ |
`Web Proxy/Filter <https://docs.opnsense.org/manual/how-tos/proxywebfilter.html>`_

Info
****

General
=======

ansibleguy.opnsense.webproxy_general
------------------------------------

This module manages the basic Web-Proxy settings that can be found in the WEB-UI menu: 'Services - Web Proxy - Administration - General Proxy Settings' (*URL 'ui/proxy'*)

ansibleguy.opnsense.webproxy_cache
----------------------------------

This module manages the Web-Proxy caching-settings that can be found in the WEB-UI menu: 'Services - Web Proxy - Administration - General Proxy Settings - Local Cache Settings (*DropDown*)' (*URL 'ui/proxy#subtab_proxy-general-cache-local'*)

ansibleguy.opnsense.webproxy_parent
-----------------------------------

This module manages the Web-Proxy parent-proxy settings that can be found in the WEB-UI menu: 'Services - Web Proxy - Administration - General Proxy Settings - Parent Proxy Settings (*DropDown*)' (*URL 'ui/proxy#subtab_proxy-general-parentproxy'*)

ansibleguy.opnsense.webproxy_traffic
------------------------------------

This module manages the Web-Proxy traffic-management settings that can be found in the WEB-UI menu: 'Services - Web Proxy - Administration - General Proxy Settings - Traffic Management Settings (*DropDown*)' (*URL 'ui/proxy#subtab_proxy-general-traffic'*)


Definition
**********

.. include:: ../_include/param_basic.rst

General
=======

ansibleguy.opnsense.webproxy_general
------------------------------------

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "enabled","boolean","false","true","\-","En- or disable the proxy"
    "errors","string","false","opnsense","error_pages","The proxy error pages can be altered, default layout uses OPNsense content, when Squid is selected the content for the selected language will be used (standard squid layout), Custom offers the possibility to upload your own theme content"
    "icp_port","integer","false","\-","icp","\-"
    "log","boolean","false","true","\-","\-"
    "log_store","boolean","false","true","\-","\-"
    "log_target","string","false","file","\-","One of: 'file', 'file_extendend', 'file_json', 'syslog', 'syslog_json'. Send log data to the selected target. When syslog is selected, facility local 4 will be used to send messages of info level for these logs"
    "log_ignore","list","false","\-","\-","Type subnets/addresses you want to ignore for the access.log"
    "dns_servers","list","false","\-","\-","IPs of alternative DNS servers you like to use"
    "dns_prio_ipv4","boolean","false","false","dns_ipv4_first","This option reverses the order of preference to make Squid contact dual-stack websites over IPv4 first. Squid will still perform both IPv6 and IPv4 DNS lookups before connecting. This option will restrict the situations under which IPv6 connectivity is used (and tested) and will hide network problems which would otherwise be detected and warned about"
    "use_via_header","boolean","false","true","\-","If set (default), Squid will include a Via header in requests and replies as required by RFC2616"
    "pinger","boolean","false","true","\-","Toggles the Squid pinger service. This service is used in the selection of the best parent proxy"
    "handling_forwarded_for","string","false","default","forwarded_for_handling, forwarded_for, handle_ff","One of: 'default', 'on', 'off', 'transparent', 'delete', 'truncate'. Select what to do with X-Forwarded-For header. If set to: 'on', Squid will append your client's IP address in the HTTP requests it forwards. By default it looks like X-Forwarded-For: 192.1.2.3; If set to: 'off', it will appear as X-Forwarded-For: unknown; 'transparent', Squid will not alter the X-Forwarded-For header in any way; If set to: 'delete', Squid will delete the entire X-Forwarded-For header; If set to: 'truncate', Squid will remove all existing X-Forwarded-For entries, and place the client IP as the sole entry"
    "handling_uri_whitespace","string","false","strip","uri_whitespace_handling, uri_whitespace, handle_uw","One of: 'strip', 'deny', 'allow', 'encode', 'chop'. Select what to do with URI that contain whitespaces. The current Squid implementation of encode and chop violates RFC2616 by not using a 301 redirect after altering the URL"
    "hostname","string","false","\-","visible_hostname","The hostname to be displayed in proxy server error messages"
    "email","string","false","admin@localhost.local","visible_email","The email address displayed in error messages to the users"
    "suppress_version","boolean","false","false","\-","Suppress Squid version string info in HTTP headers and HTML error pages"
    "connect_timeout","integer","false","\-","","Between 1 and 120 seconds. This can help you when having connection issues with IPv6 enabled servers. "
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

ansibleguy.opnsense.webproxy_cache
----------------------------------

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "memory_mb","integer","false","256","memory, mem","The cache memory size to use or zero to disable completely"
    "size_mb","integer","false","100","size","The storage size for the local cache"
    "directory","string","false","/var/squid/cache","dir","The location for the local cache"
    "layer_1","integer","false","16","layer1, l1","The number of first-level subdirectories for the local cache"
    "layer_2","integer","false","256","layer2, l2","The number of second-level subdirectories for the local cache"
    "size_mb_max","integer","false","4","maximum_object_size, max_size","The maximum object size"
    "memory_kb_max","integer","false","512","maximum_object_size_in_memory, max_memory, max_mem","The maximum object size"
    "memory_cache_mode","string","false","default","cache_mode, mode","One of: 'always', 'disk', 'network', 'default'. Controls which objects to keep in the memory cache (cache_mem) always: Keep most recently fetched objects in memory (default) disk: Only disk cache hits are kept in memory, which means an object must first be cached on disk and then hit a second time before cached in memory. network: Only objects fetched from network is kept in memory"
    "cache_linux_packages","boolean","false","false","\-","Enable or disable the caching of packages for linux distributions. This makes sense if you have multiple servers in your network and do not host your own package mirror. This will reduce internet traffic usage but increase disk access"
    "cache_windows_updates","boolean","false","false","\-","Enable or disable the caching of Windows updates. This makes sense if you don't have a WSUS server. If you can setup a WSUS server, this solution should be preferred"
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

ansibleguy.opnsense.webproxy_parent
-----------------------------------

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "enabled","boolean","false","true","\-","En- or disable the parent-proxy"
    "host","string","false","\-","ip","Parent proxy IP address or hostname"
    "auth","boolean","false","false","\-","Enable authentication against the parent proxy"
    "user","string","false","\-","\-","Set a username if parent proxy requires authentication"
    "password","string","false","\-","\-","Set a username if parent proxy requires authentication"
    "port","integer","false","\-","p","\-"
    "local_domains","list","false","\-","domains","Domains not to be sent via parent proxy"
    "local_ips","list","false","\-","ips","IP addresses not to be sent via parent proxy"
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

ansibleguy.opnsense.webproxy_traffic
------------------------------------

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "enabled","boolean","false","true","\-","En- or disable the traffic management"
    "download_kb_max","integer","false","2048","download_max, download, dl_max, dl","The maximum size for downloads in kilobytes (leave empty to disable)"
    "upload_kb_max","integer","false","1024","upload_max, upload, ul_max, ul","The maximum size for uploads in kilobytes (leave empty to disable)"
    "throttle_kb_bandwidth","integer","false","1024","throttle_bandwidth, throttle_bw, bandwidth, bw","The allowed overall bandwidth in kilobits per second (leave empty to disable)"
    "throttle_kb_host_bandwidth","integer","false","256","throttle_host_bandwidth, throttle_host_bw, host_bandwidth, host_bw","The allowed per host bandwidth in kilobits per second (leave empty to disable)"
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst


Examples
********

General
=======

ansibleguy.opnsense.webproxy_general
------------------------------------

.. code-block:: yaml

    - hosts: localhost
      gather_facts: no
      module_defaults:
        ansibleguy.opnsense.webproxy_general:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'

        ansibleguy.opnsense.list:
          target: 'webproxy_general'
          firewall: "{{ lookup('ansible.builtin.env', 'TEST_FIREWALL') }}"
          api_credential_file: "{{ lookup('ansible.builtin.env', 'TEST_API_KEY') }}"

      tasks:
        - name: Example
          ansibleguy.opnsense.webproxy_general:
            # errors: 'opnsense'
            # icp_port: ''
            # log: true
            # log_store: true
            # log_target: 'file'
            # log_ignore: []
            # dns_servers: []
            # dns_prio_ipv4: false
            # use_via_header: true
            # suppress_version: false
            # pinger: true
            # hostname: ''
            # connect_timeout: ''
            # email: 'admin@localhost.local'
            # handling_forwarded_for: 'default'
            # handling_uri_whitespace: 'strip'
            # errors: 'opnsense'
            # enabled: true
            # reload: true
            # debug: false

        - name: Pulling settings
          ansibleguy.opnsense.list:
          #  target: 'webproxy_general'
          register: existing_entries

        - name: Printing settings
          ansible.builtin.debug:
            var: existing_entries.data

ansibleguy.opnsense.webproxy_cache
----------------------------------

.. code-block:: yaml

    - hosts: localhost
      gather_facts: no
      module_defaults:
        ansibleguy.opnsense.webproxy_cache:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'

        ansibleguy.opnsense.list:
          target: 'webproxy_cache'
          firewall: "{{ lookup('ansible.builtin.env', 'TEST_FIREWALL') }}"
          api_credential_file: "{{ lookup('ansible.builtin.env', 'TEST_API_KEY') }}"

      tasks:
        - name: Example
          ansibleguy.opnsense.webproxy_cache:
            # memory_mb: 256
            # size_mb: 100
            # directory: '/var/squid/cache'
            # layer_1: 16
            # layer_2: 256
            # size_mb_max: 4
            # memory_kb_max: 512
            # memory_cache_mode: 'default'
            # cache_linux_packages: false
            # cache_windows_updates: false
            # reload: true
            # debug: false

        - name: Pulling settings
          ansibleguy.opnsense.list:
          #  target: 'webproxy_cache'
          register: existing_entries

        - name: Printing settings
          ansible.builtin.debug:
            var: existing_entries.data

ansibleguy.opnsense.webproxy_parent
-----------------------------------

.. code-block:: yaml

    - hosts: localhost
      gather_facts: no
      module_defaults:
        ansibleguy.opnsense.webproxy_parent:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'

        ansibleguy.opnsense.list:
          target: 'webproxy_parent'
          firewall: "{{ lookup('ansible.builtin.env', 'TEST_FIREWALL') }}"
          api_credential_file: "{{ lookup('ansible.builtin.env', 'TEST_API_KEY') }}"

      tasks:
        - name: Example
          ansibleguy.opnsense.webproxy_parent:
            # host: ''
            # auth: false
            # user: ''
            # password: ''
            # port: ''
            # local_domains: []
            # local_ips: []
            # enabled: true
            # reload: true
            # debug: false

        - name: Pulling settings
          ansibleguy.opnsense.list:
          #  target: 'webproxy_parent'
          register: existing_entries

        - name: Printing settings
          ansible.builtin.debug:
            var: existing_entries.data

ansibleguy.opnsense.webproxy_traffic
------------------------------------

.. code-block:: yaml

    - hosts: localhost
      gather_facts: no
      module_defaults:
        ansibleguy.opnsense.webproxy_traffic:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'

        ansibleguy.opnsense.list:
          target: 'webproxy_traffic'
          firewall: "{{ lookup('ansible.builtin.env', 'TEST_FIREWALL') }}"
          api_credential_file: "{{ lookup('ansible.builtin.env', 'TEST_API_KEY') }}"

      tasks:
        - name: Example
          ansibleguy.opnsense.webproxy_traffic:
            # download_kb_max: 2048
            # upload_kb_max: 1024
            # throttle_kb_bandwidth: 1024
            # throttle_kb_host_bandwidth: 256
            # enabled: true
            # reload: true
            # debug: false

        - name: Pulling settings
          ansibleguy.opnsense.list:
          #  target: 'webproxy_traffic'
          register: existing_entries

        - name: Printing settings
          ansible.builtin.debug:
            var: existing_entries.data
