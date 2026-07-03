.. _modules_basic:

.. include:: ../_include/head.rst

======================
Basic module arguments
======================

All modules
***********

..  csv-table:: Definition
    :header: "Parameter","Type","Required","Default","Aliases","Comment"
    :widths: 15 10 10 10 10 45

    "firewall","string","true","\-","\-","IP-Address or DNS hostname of the target firewall. Must be included as 'common name' or 'subject alternative name' in the firewalls web-certificate to use 'ssl_verify=true'"
    "api_port","integer","false","443","\-","Port the target firewall uses for its web-interface"
    "api_key","string","false, true if 'api_credential_file' is not used","\-","\-","API key used to authenticate, alternative to 'api_credential_file'"
    "api_secret","string","false, true if 'api_credential_file' is not used","\-","\-","API secret used to authenticate, alternative to 'api_credential_file'. Is set as 'no_log' parameter"
    "api_credential_file","path","false, true if 'api_key' and 'api_secret' are not used","\-","\-","Path to the api-credential file as downloaded through the web-interface. Alternative to 'api_key' and 'api_secret'"
    "ssl_verify","boolean","false","true","\-","If the certificate of the target firewall should be validated. RECOMMENDED FOR PRODUCTION USAGE!"
    "ssl_ca_file","path","false","\-","\-","If you use an internal certificate-authority to create the certificate of the target firewall, provide the path to its public key for validation"
    "debug","boolean","false","false","\-","Used to en-/disable the debug mode. All API requests and responses will be shown as Ansible warnings at runtime. Will be hidden if the tasks 'no_log' parameter is set to 'true'"
    "profiling","boolean","false","false","\-","Used to en-/disable the profiling mode. Time consumption of the module will be logged to '/tmp/oxlorg.opnsense'"
    "api_timeout","float","false","\-","timeout","Manually override the modules default API-request timeout"
    "api_retries","integer","false","0","connect_retries","Number of retries on API requests, in case there is an error when ESTABLISHING the connection. This does not handle errors returned by the OPNsense system"

Modules managing multiple entries
*********************************

..  csv-table:: Definition
    :header: "Parameter","Type","Required","Default","Aliases","Comment"
    :widths: 15 10 10 10 10 45

    "enabled","boolean","false","true","\-","En- or disable the entry"
    "state","string","false","present","\-","One of 'present', 'absent'. Add or remove the entry"
    "match_fields","list","false","depends on the module","\-","Some modules allow you to define the fields that are used to match configured entries with existing ones (Ansible vars/inventory <=> OPNsense). The Ansible-Module will only consider an entry to be the same when all fields in this list match."

Reload / Apply
**************

Like in the WebUI - you have to "Apply" your changes when you are done modifying.

For more info see: :ref:`oxlorg.opnsense.reload <modules_reload>`
