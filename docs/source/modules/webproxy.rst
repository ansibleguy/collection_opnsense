.. _modules_webproxy:

.. include:: ../_include/head.rst

=========
Web Proxy
=========

**STATE**: unstable

**TESTS**: `webproxy_general <https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/webproxy_general.yml>`_ |
`webproxy_cache <https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/webproxy_cache.yml>`_ |
`webproxy_parent <https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/webproxy_parent.yml>`_ |
`webproxy_traffic <https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/webproxy_traffic.yml>`_ |
`webproxy_forward <https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/webproxy_forward.yml>`_ |
`webproxy_acl <https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/webproxy_acl.yml>`_ |
`webproxy_icap <https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/webproxy_icap.yml>`_ |
`webproxy_auth <https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/webproxy_auth.yml>`_ |
`webproxy_remote_acl <https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/webproxy_remote_acl.yml>`_ |
`webproxy_pac_proxy <https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/webproxy_pac_proxy.yml>`_ |
`webproxy_pac_match <https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/webproxy_pac_match.yml>`_ |
`webproxy_pac_rule <https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/webproxy_pac_rule.yml>`_

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

Forward
=======

ansibleguy.opnsense.webproxy_forward
------------------------------------

This module manages the Web-Proxy forwarding settings that can be found in the WEB-UI menu: 'Services - Web Proxy - Administration - Forward Proxy

* General Forward Settings (*DropDown*)' (*URL 'ui/proxy#subtab_proxy-forward-general'*)
* FTP Proxy Settings (*DropDown*)' (*URL 'ui/proxy#subtab_proxy-forward-ftp'*)
* SNMP Agent Settings (*DropDown*)' (*URL 'ui/proxy#subtab_proxy-forward-snmp'*)

ansibleguy.opnsense.webproxy_acl
--------------------------------

This module manages the Web-Proxy forwarding ACLs that can be found in the WEB-UI menu: 'Services - Web Proxy - Administration - General Proxy Settings - Access Control List (*DropDown*)' (*URL 'ui/proxy#subtab_proxy-forward-acl'*)

ansibleguy.opnsense.webproxy_icap
---------------------------------

This module manages the Web-Proxy ICAP settings that can be found in the WEB-UI menu: 'Services - Web Proxy - Administration - General Proxy Settings - ICAP Settings (*DropDown*)' (*URL 'ui/proxy#subtab_proxy-icap'*)

ansibleguy.opnsense.webproxy_auth
---------------------------------

This module manages the Web-Proxy authentication settings that can be found in the WEB-UI menu: 'Services - Web Proxy - Administration - General Proxy Settings - Authentication Settings (*DropDown*)' (*URL 'ui/proxy#subtab_proxy-general-authentication'*)

Remote ACL
==========

ansibleguy.opnsense.webproxy_remote_acl
---------------------------------------

This module manages the Remote ACL entries that can be found in the WEB-UI menu: 'Services - Web Proxy - Administration - Remote Access Control Lists

The configured lists are matched by its unique file-name.

Proxy Auto-Config
=================

ansibleguy.opnsense.webproxy_pac_proxy
--------------------------------------

This module manages the Proxy-Auto-Config Proxy entries that can be found in the WEB-UI menu: 'Services - Web Proxy - Administration - Proxy Auto-Config - Proxies (*DropDown*)' (*URL 'ui/proxy#subtab_pac_proxies'*)

ansibleguy.opnsense.webproxy_pac_match
--------------------------------------

This module manages the Proxy-Auto-Config Match entries that can be found in the WEB-UI menu: 'Services - Web Proxy - Administration - Proxy Auto-Config - Matches (*DropDown*)' (*URL 'ui/proxy#subtab_pac_matches'*)

You need to **provide arguments** for different **match-types**:

* 'url_matches' needs 'url' to be provided
* 'hostname_matches', 'plain_hostname', 'is_resolvable' and 'dns_domain_is' need 'hostname' to be provided
* 'my_ip_in_net' and 'destination_in_net' need 'network' to be provided
* 'date_range' needs 'month_from' and 'month_to' to be provided
* 'time_range' needs 'hour_from' and 'hour_to' to be provided
* 'weekday_range' needs 'weekday_from' and 'weekday_to' to be provided
* 'dns_domain_levels' needs 'domain_level_from' and 'domain_level_to' to be provided

ansibleguy.opnsense.webproxy_pac_rule
-------------------------------------

This module manages the Proxy-Auto-Config Rule entries that can be found in the WEB-UI menu: 'Services - Web Proxy - Administration - Proxy Auto-Config - Rules (*DropDown*)' (*URL 'ui/proxy#subtab_pac_rules'*)


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

Forward
=======

ansibleguy.opnsense.webproxy_forward
------------------------------------

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "transparent","boolean","false","false","transparent_mode","Enable transparent proxy mode. You will need a firewall rule to forward traffic from the firewall to the proxy server. You may leave the proxy interfaces empty, but remember to set a valid ACL in that case"
    "ssl_inspection","boolean","false","false","ssl_inspect, ssl","Enable SSL inspection mode, which allows to log HTTPS connections information, such as requested URL and/or make the proxy act as a man in the middle between the internet and your clients. Be aware of the security implications before enabling this option. If you plan to use transparent HTTPS mode, you need nat rules to reflect your traffic"
    "ssl_inspection_sni_only","boolean","false","false","ssl_sni_only","Do not decode and/or filter SSL content, only log requested domains and IP addresses. Some old servers may not provide SNI, so their addresses will not be indicated"
    "interfaces","list","false","['lan']","ints","Interface(s) the proxy will bind to"
    "allow_interface_subnets","boolean","false","true","allow_subnets","When enabled the subnets of the selected interfaces will be added to the allow access list"
    "port","integer","false","3128","p","\-"
    "port_ssl","integer","false","3129","p_ssl","\-"
    "ssl_ca","string","false","\-","ca","Select a Certificate Authority to use"
    "ssl_exclude","list","false","\-","\-","A list of sites which may not be inspected, for example bank sites. Prefix the domain with a . to accept all subdomains (e.g. .google.com)"
    "ssl_cache_mb","integer","false","4","ssl_cache, cache","The maximum size (in MB) to use for SSL certificates"
    "ssl_workers","integer","false","5","workers","The number of ssl certificate workers to use (sslcrtd_children)"
    "snmp","boolean","false","false","\-","Enable or disable the squid SNMP Agent"
    "port_snmp","integer","false","3401","p_snmp","\-"
    "snmp_password","string","false","public","snmp_community, snmp_pwd","The password for access to SNMP agent"
    "interfaces_ftp","list","false","\-","ints_ftp","Interface(s) the ftp proxy will bind to"
    "port_ftp","integer","false","2121","p_ftp","\-"
    "transparent_ftp","boolean","false","false","\-","Enable transparent ftp proxy mode to forward all requests or destination port 21 to the proxy server without any additional configuration"
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

ansibleguy.opnsense.webproxy_acl
--------------------------------

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "allow","list","false","\-","allow_subnets, subnets","IPs and Subnets you want to allow access to the proxy server"
    "exclude","list","false","\-","unrestricted, ignore","IPs and Subnets you want to bypass the proxy server"
    "banned","list","false","\-","blocked, block, ban","IPs and Subnets you want to deny access to the  proxy server"
    "exclude_domains","list","false","\-","safe_list, whitelist","You may use a regular expression, use a comma or press Enter for new item. Examples: 'mydomain.com' matches on '*.mydomain.com'; '^https?:\\/\\/([a-zA-Z]+)\\.mydomain\\.' matches on 'http(s)://textONLY.mydomain.*'; '\\.gif$' matches on '\\*.gif' but not on '\\*.gif\\test'; '\\[0-9]+\\.gif$' matches on '\\123.gif' but not on '\\test.gif'"
    "block_domains","list","false","\-","block, block_list, blacklist","You may use a regular expression, use a comma or press Enter for new item. Examples: 'mydomain.com' matches on '*.mydomain.com'; '^https?:\\/\\/([a-zA-Z]+)\\.mydomain\\.' matches on 'http(s)://textONLY.mydomain.*'; '\\.gif$' matches on '\\*.gif' but not on '\\*.gif\\test'; '\\[0-9]+\\.gif$' matches on '\\123.gif' but not on '\\test.gif'"
    "block_user_agents","list","false","\-","block_ua, block_list_ua","Block user-agents. You may use a regular expression, use a comma or press Enter for new item. Examples: '^(.)+Macintosh(.)+Firefox/37\\.0' matches on 'Macintosh version of Firefox revision 37.0'; '^Mozilla' matches on 'all Mozilla based browsers'"
    "block_mime_types","list","false","\-","block_mime, block_list_mime","Block specific MIME type reply. You may use a regular expression, use a comma or press Enter for new item. Examples: 'video/flv' matches on 'Flash Video'; 'application/x-javascript' matches on 'javascripts'"
    "exclude_google","list","false","\-","safe_list_google","The domain that will be allowed to use Google GSuite. All accounts that are not in this domain will be blocked to use it"
    "youtube_filter","string","false","\-","youtube","One of: 'strict', 'moderate'. Youtube filter level"
    "ports_tcp","list","false","['80:http', '21:ftp', '443:https', '70:gopher', '210:wais', '1025-65535:unregistered ports', '280:http-mgmt', '488:gss-http', '591:filemaker', '777:multiling http']","p_tcp","Allowed destination TCP ports, you may use ranges (ex. 222-226) and add comments with colon (ex. 22:ssh)"
    "ports_ssl","list","false","['443:https']","p_ssl","Allowed destination SSL ports, you may use ranges (ex. 222-226) and add comments with colon (ex. 22:ssh)"
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

ansibleguy.opnsense.webproxy_icap
---------------------------------

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "enabled","boolean","false","true","\-","If this checkbox is checked, you can use an ICAP server to filter or replace content"
    "request_url","string","false","icap://[::1]:1344/avscan","request, request_target","The url where the REQMOD requests should be sent to"
    "response_url","string","false","icap://[::1]:1344/avscan","response, response_target","The url where the RESPMOD requests should be sent to"
    "ttl","integer","false","60","default_ttl","\-"
    "send_client_ip","boolean","false","true","send_client","If you enable this option, the client IP address will be sent to the ICAP server. This can be useful if you want to filter traffic based on IP addresses"
    "send_username","boolean","false","false","send_user","If you enable this option, the username of the client will be sent to the ICAP server. This can be useful if you want to filter traffic based on usernames. Authentication is required to use usernames"
    "encode_username","boolean","false","false","user_encode, encode_user, enc_user","Use this option if your usernames need to be encoded"
    "header_username","string","false","X-Username","header_user, user_header","The header which should be used to send the username to the ICAP server"
    "preview","boolean","false","true","\-","If you use previews, only a part of the data is sent to the ICAP server. Setting this option can improve the performance"
    "preview_size","integer","false","1024","\-","Size of the preview which is sent to the ICAP server"
    "exclude","list","false","\-","\-","Exclusion list destination domains.You may use a regular expression, use a comma or press Enter for new item. Examples: 'mydomain.com' matches on '*.mydomain.com'; 'https://([a-zA-Z]+)\\.mydomain\\.' matches on 'http(s)://textONLY.mydomain.*'; '\\.gif$' matches on '\\*.gif' but not on '\\*.gif\\test'; '\\[0-9]+\\.gif$' matches on '\\123.gif' but not on '\\test.gif'"
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

ansibleguy.opnsense.webproxy_auth
---------------------------------

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "method","string","false","\-","type, target","The authentication backend to use - as shown in the WEB-UI at 'System - Access - Servers'. Per example: 'Local Database'"
    "group","string","false","\-","local_group","Restrict access to users in the selected (local)group. **NOTE**: please be aware that users (or vouchers) which aren't administered locally will be denied when using this option"
    "prompt","string","false","OPNsense proxy authentication","realm","The prompt will be displayed in the authentication request window"
    "group","string","false","\-","local_group",""
    "ttl_h","integer","false","2","ttl, ttl_hours, credential_ttl","This specifies for how long (in hours) the proxy server assumes an externally validated username and password combination is valid (Time To Live). When the TTL expires, the user will be prompted for credentials again"
    "processes","integer","false","5","proc","The total number of authenticator processes to spawn"
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

Remote ACL
==========

ansibleguy.opnsense.webproxy_remote_acl
---------------------------------------

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "file","string","true","\-","filename","Unique file-name to store the remote acl in. Used to match existing entries with configured ones"
    "url","string","false for state changes, else true","\-","\-","Url to fetch the acl from"
    "description","string","false for state changes, else true","\-","desc","A description to explain what this blacklist is intended for"
    "username","string","false","\-","user","Optional user for authentication"
    "password","string","false","\-","pwd","Optional password for authentication"
    "categories","list","false","\-","cat, filter","Select categories to use, leave empty for all. Categories are visible in the WEB-UI after initial download"
    "verify_ssl","boolean","false","true","verify","If certificate validation should be done - relevant if self-signed certificates are used on the target server!"
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

Proxy Auto-Config
=================

ansibleguy.opnsense.webproxy_pac_proxy
--------------------------------------

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","\-","Unique name for the proxy"
    "url","string","false for state changes, else true","\-","\-","A proxy URL in the form proxy.example.com:3128"
    "type","string","false","proxy","\-","One of: 'proxy', 'direct', 'http', 'https', 'socks', 'socks4', 'socks5'. Usually you should use 'direct' for a direct connection or 'proxy' for a Proxy"
    "description","string","false","\-","desc","\-"
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

ansibleguy.opnsense.webproxy_pac_match
--------------------------------------

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","\-","Unique name for the match"
    "description","string","false","\-","desc","\-"
    "negate","boolean","false","false","\-","Negate this match. For example you can match if a host is not inside a network"
    "type","string","false","url_matches","\-","One of: 'url_matches', 'hostname_matches', 'dns_domain_is', 'destination_in_net', 'my_ip_in_net', 'plain_hostname', 'is_resolvable', 'dns_domain_levels', 'weekday_range', 'date_range', 'time_range'. The type of the match. Depending on the match, you will need different arguments"
    "hostname","string","false","\-","\-","A hostname pattern like *.opnsense.org"
    "url","string","false","\-","\-","A URL pattern like forum.opnsense.org/index*"
    "network","string","false","\-","\-","The network address to match in CIDR notation for example like 127.0.0.1/8 or ::1/128"
    "domain_level_from","integer","false","0","domain_from","The minimum amount of dots in the domain name"
    "domain_level_to","integer","false","0","domain_to","The maximum amount of dots in the domain name"
    "hour_from","integer","false","0","time_from","Start hour for match-period"
    "hour_to","integer","false","0","time_to","End hour for match-period"
    "month_from","integer","false","1","date_from","Start month for match-period"
    "month_to","integer","false","1","date_to","End hour month match-period"
    "weekday_from","integer","false","1","day_from","Start weekday for match-period. 1 = monday, 7 = sunday"
    "weekday_to","integer","false","1","day_to","End hour weekday match-period. 1 = monday, 7 = sunday"
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

ansibleguy.opnsense.webproxy_pac_rule
-------------------------------------

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "description","string","true","\-","desc, name","Unique description used to identify existing rules"
    "matches","list","false for state changes, else true","\-","\-","Matches you want to use in this rule. This matches are joined using the selected separator"
    "proxies","list","false for state changes, else true","\-","\-","Proxies you want to use address using this rule"
    "join_type","string","false","and","join","One of: 'and', 'or'. A separator to join the matches. 'or' means any match can be true which can be used to configure the same proxy for multiple networks while 'and' means all matches must be true which can be used to assign the proxy in a more detailed way"
    "match_type","string","false","if","operator","One of: 'if', 'unless'. Choose 'if' in case any case you want to ensure a match to evaluate as is, else choose 'unless' if you want the negated version. Unless is used if you want to use the proxy for every host but not for some special ones"
    "enabled","boolean","false","true","\-","En- or disable the rule"
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
          register: current_config

        - name: Printing settings
          ansible.builtin.debug:
            var: current_config.data

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
          register: current_config

        - name: Printing settings
          ansible.builtin.debug:
            var: current_config.data

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
          register: current_config

        - name: Printing settings
          ansible.builtin.debug:
            var: current_config.data

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
          register: current_config

        - name: Printing settings
          ansible.builtin.debug:
            var: current_config.data

Forward
=======

ansibleguy.opnsense.webproxy_forward
------------------------------------

.. code-block:: yaml

    - hosts: localhost
      gather_facts: no
      module_defaults:
        ansibleguy.opnsense.webproxy_forward:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'

        ansibleguy.opnsense.list:
          target: 'webproxy_forward'
          firewall: "{{ lookup('ansible.builtin.env', 'TEST_FIREWALL') }}"
          api_credential_file: "{{ lookup('ansible.builtin.env', 'TEST_API_KEY') }}"

      tasks:
        - name: Example
          ansibleguy.opnsense.webproxy_forward:
            # interfaces: ['lan']
            # port: 3238
            # port_ssl: 3239
            # transparent: false
            # ssl_inspection: false
            # ssl_inspection_sni_only: false
            # ssl_ca: ''
            # ssl_exclude: []
            # ssl_cache_mb: 4
            # ssl_workers: 5
            # allow_interface_subnets: true
            # snmp: true
            # port_snmp: 3401
            # snmp_password: 'public'
            # interfaces_ftp: []
            # port_ftp: 2121
            # transparent_ftp: false
            # reload: true
            # debug: false

ansibleguy.opnsense.webproxy_acl
--------------------------------

.. code-block:: yaml

    - hosts: localhost
      gather_facts: no
      module_defaults:
        ansibleguy.opnsense.webproxy_acl:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'

        ansibleguy.opnsense.list:
          target: 'webproxy_acl'
          firewall: "{{ lookup('ansible.builtin.env', 'TEST_FIREWALL') }}"
          api_credential_file: "{{ lookup('ansible.builtin.env', 'TEST_API_KEY') }}"

      tasks:
        - name: Example
          ansibleguy.opnsense.webproxy_acl:
            # allow: []
            # exclude: []
            # banned: []
            # exclude_domains: []
            # block_domains: []
            # block_user_agents: []
            # block_mime_types: []
            # exclude_google: []
            # youtube_filter: ''
            # ports_tcp: ['80:http', '21:ftp', '443:https', '70:gopher', '210:wais', '1025-65535:unregistered ports', '280:http-mgmt', '488:gss-http', '591:filemaker', '777:multiling http']
            # ports_ssl: ['443:https']
            # reload: true
            # debug: false

        - name: Configuring
          ansibleguy.opnsense.webproxy_acl:
            allow: ['192.168.0.0/24', '172.16.1.0/29', '172.16.0.5']
            exclude: ['192.168.2.0/28', '172.16.1.5']
            banned: ['172.16.3.0/24', '172.16.2.5']
            exclude_domains: ['ansibleguy.net']
            block_domains: ['ansibleguy.com']
            block_user_agents: ['test1', 'test2']
            block_mime_types: ['video/flv', 'test']
            ports_tcp: ['80:http', '21:ftp']
            ports_ssl: ['443:https', '8443:random']
            youtube_filter: 'moderate'

        - name: Pulling settings
          ansibleguy.opnsense.list:
          #  target: 'webproxy_acl'
          register: current_config

        - name: Printing settings
          ansible.builtin.debug:
            var: current_config.data

ansibleguy.opnsense.webproxy_icap
---------------------------------

.. code-block:: yaml

    - hosts: localhost
      gather_facts: no
      module_defaults:
        ansibleguy.opnsense.webproxy_icap:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'

        ansibleguy.opnsense.list:
          target: 'webproxy_icap'
          firewall: "{{ lookup('ansible.builtin.env', 'TEST_FIREWALL') }}"
          api_credential_file: "{{ lookup('ansible.builtin.env', 'TEST_API_KEY') }}"

      tasks:
        - name: Example
          ansibleguy.opnsense.webproxy_icap:
            # request_url: 'icap://[::1]:1344/avscan'
            # response_url: 'icap://[::1]:1344/avscan'
            # ttl: 60
            # send_client_ip: true
            # send_username: false
            # encode_username: false
            # header_username: 'X-Username'
            # preview: true
            # preview_size: 1024
            # exclude: []
            # enabled: true
            # reload: true
            # debug: false

        - name: Pulling settings
          ansibleguy.opnsense.list:
          #  target: 'webproxy_icap'
          register: current_config

        - name: Printing settings
          ansible.builtin.debug:
            var: current_config.data

ansibleguy.opnsense.webproxy_auth
---------------------------------

.. code-block:: yaml

    - hosts: localhost
      gather_facts: no
      module_defaults:
        ansibleguy.opnsense.webproxy_auth:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'

        ansibleguy.opnsense.list:
          target: 'webproxy_auth'
          firewall: "{{ lookup('ansible.builtin.env', 'TEST_FIREWALL') }}"
          api_credential_file: "{{ lookup('ansible.builtin.env', 'TEST_API_KEY') }}"

      tasks:
        - name: Example
          ansibleguy.opnsense.webproxy_auth:
            # method: ''
            # group: ''
            # prompt: 'OPNsense proxy authentication'
            # ttl_h: 2
            # processes: 5
            # reload: true
            # debug: false

        - name: Pulling settings
          ansibleguy.opnsense.list:
          #  target: 'webproxy_auth'
          register: current_config

        - name: Printing settings
          ansible.builtin.debug:
            var: current_config.data

Remote ACL
==========

ansibleguy.opnsense.webproxy_remote_acl
---------------------------------------

.. code-block:: yaml

    - hosts: localhost
      gather_facts: no
      module_defaults:
        ansibleguy.opnsense.webproxy_remote_acl:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'

        ansibleguy.opnsense.list:
          target: 'webproxy_remote_acl'
          firewall: "{{ lookup('ansible.builtin.env', 'TEST_FIREWALL') }}"
          api_credential_file: "{{ lookup('ansible.builtin.env', 'TEST_API_KEY') }}"

      tasks:
        - name: Example
          ansibleguy.opnsense.webproxy_remote_acl:
            file: 'example'
            url: 'https://example.ansibleguy.net/rac1'
            description: 'example ACL'
            # categories: []
            # username: ''
            # password: ''
            # verify_ssl: true
            # enabled: true
            # reload: true
            # debug: false

        - name: Adding
          ansibleguy.opnsense.webproxy_remote_acl:
            file: 'test1'
            url: 'https://test.lan/rac1'
            username: 'random'
            password: 'random'
            verify_ssl: true
            description: 'test'

        - name: Disabling
          ansibleguy.opnsense.webproxy_remote_acl:
            file: 'test1'
            url: 'https://test.lan/rac2'
            username: 'random'
            password: 'random2'
            description: 'Custom ACL'
            enabled: false

        - name: Pulling settings
          ansibleguy.opnsense.list:
          #  target: 'webproxy_remote_acl'
          register: existing_entries

        - name: Printing settings
          ansible.builtin.debug:
            var: existing_entries.data

        - name: Removing
          ansibleguy.opnsense.webproxy_remote_acl:
            file: 'test1'
            state: 'absent'

Proxy Auto-Config
=================

ansibleguy.opnsense.webproxy_pac_proxy
--------------------------------------

.. code-block:: yaml

    - hosts: localhost
      gather_facts: no
      module_defaults:
        ansibleguy.opnsense.webproxy_pac_proxy:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'

        ansibleguy.opnsense.list:
          target: 'webproxy_pac_proxy'
          firewall: "{{ lookup('ansible.builtin.env', 'TEST_FIREWALL') }}"
          api_credential_file: "{{ lookup('ansible.builtin.env', 'TEST_API_KEY') }}"

      tasks:
        - name: Example
          ansibleguy.opnsense.webproxy_pac_proxy:
            name: 'example'
            url: 'example.ansibleguy.net:3128'
            # type: 'proxy'
            # description: ''
            # reload: true
            # debug: false

        - name: Adding
          ansibleguy.opnsense.webproxy_pac_proxy:
            name: 'test1'
            url: 'test.lan:3128'
            description: 'test'

        - name: Pulling settings
          ansibleguy.opnsense.list:
          #  target: 'webproxy_pac_proxy'
          register: existing_entries

        - name: Printing settings
          ansible.builtin.debug:
            var: existing_entries.data

        - name: Removing
          ansibleguy.opnsense.webproxy_pac_proxy:
            file: 'test1'
            state: 'absent'

ansibleguy.opnsense.webproxy_pac_match
--------------------------------------

.. code-block:: yaml

    - hosts: localhost
      gather_facts: no
      module_defaults:
        ansibleguy.opnsense.webproxy_pac_match:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'

        ansibleguy.opnsense.list:
          target: 'webproxy_pac_match'
          firewall: "{{ lookup('ansible.builtin.env', 'TEST_FIREWALL') }}"
          api_credential_file: "{{ lookup('ansible.builtin.env', 'TEST_API_KEY') }}"

      tasks:
        - name: Example
          ansibleguy.opnsense.webproxy_pac_match:
            name: 'example'
            # type: 'url_matches'
            # description: ''
            # negate: false
            # hostname: ''
            # url: ''
            # network: ''
            # domain_level_from: 0
            # domain_level_to: 0
            # hour_from: 0
            # hour_to: 0
            # month_from: 1
            # month_to: 1
            # weekday_from: 1
            # weekday_to: 1
            # reload: true
            # debug: false

        - name: Adding hostname match
          ansibleguy.opnsense.webproxy_pac_match:
            hostname: 'test.ansibleguy.net'
            type: 'hostname_matches'
            description: 'test'

        - name: Adding time match
          ansibleguy.opnsense.webproxy_pac_match:
            hostname: 'test.ansibleguy.net'
            description: 'working hours'
            type: 'time_range'
            hour_from: 6
            hour_to: 18

        - name: Pulling settings
          ansibleguy.opnsense.list:
          #  target: 'webproxy_pac_match'
          register: existing_entries

        - name: Printing settings
          ansible.builtin.debug:
            var: existing_entries.data

        - name: Removing
          ansibleguy.opnsense.webproxy_pac_match:
            file: 'test1'
            state: 'absent'

ansibleguy.opnsense.webproxy_pac_rule
-------------------------------------

.. code-block:: yaml

    - hosts: localhost
      gather_facts: no
      module_defaults:
        ansibleguy.opnsense.webproxy_pac_rule:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'

        ansibleguy.opnsense.list:
          target: 'webproxy_pac_rule'
          firewall: "{{ lookup('ansible.builtin.env', 'TEST_FIREWALL') }}"
          api_credential_file: "{{ lookup('ansible.builtin.env', 'TEST_API_KEY') }}"

      tasks:
        - name: Example
          ansibleguy.opnsense.webproxy_pac_rule:
            description: 'example'
            matches: []
            proxies: []
            # join_type: 'and'
            # match_type: 'if'
            # reload: true
            # debug: false

        - name: Adding - linking to existing match & proxy
          ansibleguy.opnsense.webproxy_pac_rule:
            description: 'test_rule'
            matches: ['test_match']
            proxies: ['test_proxy']
            join_type: 'and'
            match_type: 'unless'

        - name: Pulling settings
          ansibleguy.opnsense.list:
          #  target: 'webproxy_pac_rule'
          register: existing_entries

        - name: Printing settings
          ansible.builtin.debug:
            var: existing_entries.data

        - name: Removing
          ansibleguy.opnsense.webproxy_pac_rule:
            file: 'test_rule'
            state: 'absent'
