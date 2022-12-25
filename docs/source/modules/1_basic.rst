.. _modules_basic:

.. include:: ../_include/head.rst

==========================
1 - Basic module arguments
==========================

All modules
***********

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Comment"
    :widths: 15 10 10 10 55

    firewall, string, true, \- , "IP-Address or DNS hostname of the target firewall. Must be included as 'common name' in the firewalls web-certificate to use 'ssl_verify=true'"
    api_port, int, false, 443, "Port the target firewall uses for its web-interface"
    api_key, string, "false, true if 'api_credential_file' is not used", \- , "API key used to authenticate, alternative to 'api_credential_file'"
    api_secret, string, "false, true if 'api_credential_file' is not used", \- , "API secret used to authenticate, alternative to 'api_credential_file'. Is set as 'no_log' parameter."
    api_credential_file, path, "false, true if 'api_key' and 'api_secret' are not used", \- , "Path to the api-credential file as downloaded through the web-interface. Alternative to 'api_key' and 'api_secret'."
    ssl_verify, bool, false, true, "If the certificate of the target firewall should be validated. RECOMMENDED FOR PRODUCTION USAGE!"
    ssl_ca_file, path, false, \- , "If you use an internal certificate-authority to create the certificate of the target firewall, provide the path to its public key for validation."
    debug, boolean, false, false, "Used to en-/disable the debug mode. All API requests and responses will be shown as Ansible warnings at runtime. Will be hidden if the tasks 'no_log' parameter is set to 'true'."
    timeout, float, false, \- , "Manually override the modules default timeout"

Modules managing multiple entries
*********************************

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Comment"
    :widths: 15 10 10 10 55

    "enabled","boolean","false","true","En- or disable the entry"
    "state","string","false","present","One of 'present', 'absent'. Add or remove the entry"
