# BIND DNS

**STATE**: unstable

**TESTS**: [bind_general](https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/bind_general.yml) | 
[bind_blocklist](https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/bind_blocklist.yml) | 
[bind_acl](https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/bind_acl.yml) | 
[bind_domain](https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/bind_domain.yml) | 
[bind_record](https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/bind_record.yml)

**API DOCS**: [Plugins - Bind](https://docs.opnsense.org/development/api/plugins/bind.html)

## Sponsoring

Thanks to [@telmich](https://github.com/telmich) for sponsoring the development of these modules!

## Prerequisites

You need to install the BIND plugin:
```
os-bind
```

You can also install it using the [package module](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_package.md).

## Definition

For basic parameters see: [Basics](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_basic.md#definition)

### ansibleguy.opnsense.bind_general

| Parameter   | Type    | Required | Default value        | Aliases                                                | Comment                                                                                                          |
|:------------|:--------|:---------|:---------------------|:-------------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------|
| enabled     | bool    | false     | true                 | -                                                      | En- or disable the BIND service                                                                                  |
| ipv6     | bool    | false     | false                | -                                                      | En- or disable IPv6                                                                                              |
| response_policy_zones     | bool    | false     | false                | rpz                                                    | En- or disable response policy zones                                                                             |
| port     | integer | false     | 53530                | p                                                      | Port the BIND service should listen on. Integer between 1 and 65535                                              |
| listen_ipv4     | list    | false     | ['127.0.0.1']        | listen_v4, listen                                      | IPv4 addresses the service should listen on                                                                      |
| listen_ipv6     | list    | false     | ['::1']              | listen_v6                                              | IPv6 addresses the service should listen on                                                                      |
| query_source_ipv4     | string  | false     | -                    | query_ipv4, query_v4                                   | Specify the IPv4 address used as a source for outbound queries                                                   |
| query_source_ipv6     | string  | false     | -                    | query_ipv6, query_v6                                   | Specify the IPv6 address used as a source for outbound queries                                                   |
| transfer_source_ipv4     | string  | false     | -                    | transfer_ipv4, transfer_v4                             | Specify the IPv4 address used as a source for zone transfers                                                     |
| transfer_source_ipv6     | string  | false     | -                    | transfer_ipv6, transfer_v6                             | Specify the IPv6 address used as a source for zone transfers                                                     |
| forwarders     | list    | false     | -                    | fwd                                                    | Set one or more hosts to send your DNS queries if the request is unknown                                         |
| filter_aaaa_v4     | bool    | false     | false                | -                                                      | En- or disable to filter AAAA records on IPv4 Clients                                                            |
| filter_aaaa_v6     | bool    | false     | false                | -                                                      | En- or disable to filter AAAA records on IPv6 Clients                                                            |
| log_size     | integer | false     | 5                    | max_log_size                                           | Maximum log file size in MB                                                                                      |
| cache_size     | integer | false     | 50                   | max_cache_percentage, cache_percentage, max_cache_size | How much memory in percent the cache can use from the system                                                     |
| recursion_acl     | string  | false     | -                    | recursion                                              | Name of an existing ACL - where you allow which clients can resolve via this service. Usually use your local LAN |
| transfer_acl     | string  | false     | -                    | allow_transfer, transfer                                       | Name of an existing ACL - where you allow which server can retrieve zones                                        |
| dnssec_validation     | string  | false     | -                    | dnssec                                       | One of: 'auto', 'no'. Set to "Auto" to use the static trust anchor configuration by the system                   |
| hide_hostname     | bool    | false     | false                | -                                                      | If the system hostname should be hidden for DNS queries                                                          |
| hide_version     | bool    | false     | true                 | -                                                      | If the local BIND version should be hidden in DNS queries                                                        |
| prefetch     | bool    | false     | true                 | -                                                      | If it should prefetch domains                                                                                    |
| ratelimit     | bool    | false     | false                | -                                                      | If DNS replies should be rate limited                                                                            |
| ratelimit_count     | integer | false     | -                    | -                                                      | Set how many replies per second are allowed                                                                            |
| ratelimit_except     | list    | false     | ['127.0.0.1', '::1'] | -                                                      | Except a list of IPs from rate-limiting                                                                            |
| reload       | boolean | false    | true                 | -         | If the running config should be reloaded on change - this will take some time. For mass-managing items you might want to reload it 'manually' after all changes are done => using the [reload module](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_reload.md). |


### ansibleguy.opnsense.bind_blocklist

| Parameter    | Type    | Required | Default value         | Aliases                          | Comment                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
|:-------------|:--------|:---------|:----------------------|:---------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| enabled     | bool    | false    | true                 | -                                                      | En- or disable Blocklists                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| block           | list    | false    | -                     | lists | Blocklist's you want to enable. At least one of: 'AdAway List', 'AdGuard List', 'Blocklist.site Ads', 'Blocklist.site Fraud', 'Blocklist.site Phishing', 'Cameleon List', 'Easy List', 'EMD Malicious Domains List', 'Easyprivacy List', 'hpHosts Ads', 'hpHosts FSA', 'hpHosts PSH', 'hpHosts PUP', 'Malwaredomain List', 'NoCoin List', 'PornTop1M List', 'Ransomware Tracker List', 'Simple Ad List', 'Simple Tracker List', 'Steven Black List', 'WindowsSpyBlocker (spy)', 'WindowsSpyBlocker (update)', 'WindowsSpyBlocker (extra)', 'YoYo List' |
| exclude  | list    | false    | -                     | safe_list                             | Domains to exclude from the filter                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |                                                                                                                                                  |
| safe_google  | boolean | false    | -                     | safe_search_google                             |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |                                                                                                                                                  |
| safe_duckduckgo  | boolean | false    | -                     | safe_search_duckduckgo                             |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |                                                                                                                                                  |
| safe_youtube  | boolean | false    | -                     | safe_search_youtube                             |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |                                                                                                                                                  |
| safe_bing  | boolean | false    | -                     | safe_search_bing                             |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |                                                                                                                                                  |
| reload       | boolean | false    | true                 | -         | If the running config should be reloaded on change - this will take some time. For mass-managing items you might want to reload it 'manually' after all changes are done => using the [reload module](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_reload.md). |

### ansibleguy.opnsense.bind_acl

| Parameter | Type   | Required | Default value | Aliases | Comment                                                                                                              |
|:----------|:-------|:---------|:--------------|:--------|:---------------------------------------------------------------------------------------------------------------------|
| name      | string | true     | -             | -       | Unique name of the ACL. Some restrictions apply! Length < 32 and neither of: 'any', 'localhost', 'localnets', 'none' |
| networks  | list   | false for state changes, else true     | -             | nets   | List of networks to add to the ACL                                                                                   |
| reload       | boolean | false    | true                 | -         | If the running config should be reloaded on change - this will take some time. For mass-managing items you might want to reload it 'manually' after all changes are done => using the [reload module](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_reload.md). |

### ansibleguy.opnsense.bind_domain

| Parameter | Type    | Required | Default value | Aliases             | Comment                                                                                                                                                                                                                                      |
|:----------|:--------|:---------|:--------------|:--------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| name      | string  | true     | -             | domain_name, domain | Domain name of the zone. Both forward and reverse zones may be specified, i.e. example.com or 0.168.192.in-addr.arpa.                                                                                                                        |
| mode  | string  | false    | 'master'      | -                   | Zone operation mode. One of: 'master', 'slave'                                                                                                                                                                                               |
| master  | list    | false    | -             | master_ip           | Set the IP address of master server when using slave mode                                                                                                                                                                                    |
| transfer_key_algo  | string  | false    | -             | -                   | Set the authentication algorithm for the TSIG key used to transfer domain data from the master server. One of: 'hmac-sha512', 'hmac-sha384', 'hmac-sha256', 'hmac-sha224', 'hmac-sha1', 'hmac-md5'                                           |
| transfer_key_name  | string  | false    | -             | -                   | The name of the TSIG key, which must match the value on the master server                                                                                                                                                                    |
| transfer_key  | string  | false    | -             | -                   | The base64-encoded TSIG key                                                                                                                                                                                                                  |
| allow_notify  | list    | false    | -             | allow_notify_slave  | A list of allowed IP addresses to receive notifies from                                                                                                                                                                                      |
| transfer_acl  | string  | false    | -             | allow_transfer      | Name of an existing ACL - where you allow which server can retrieve zones                                                                                                                                                                    |
| query_acl  | string  | false    | -             | allow_query         | Name of an existing ACL - where you allow which client are allowed to query this zone                                                                                                                                                        |
| ttl  | integer | false    | 86400             | -                   | The general Time To Live for this zone. Between 60 and 86400                                                                                                                                                                                 |
| refresh  | integer | false    | 21600             | -                   | The time in seconds after which name servers should refresh the zone information. Between 60 and 86400                                                                                                                                       |
| retry  | integer | false    | 3600             | -                   | The time in seconds after which name servers should retry requests if the master does not respond. Between 60 and 86400                                                                                                                                       |
| expire  | integer | false    | 3542400             | -                   | The time in seconds after which name servers should stop answering requests if the master does not respond. Between 60 and 10000000                                                                                                                                       |
| negative  | integer | false    | 3600             | -                   | The time in seconds after which an entry for a non-existent record should expire from cache. Between 60 and 86400                                                                                                                                       |
| admin_mail  | string | false    | 'mail.opnsense.localdomain             | -                   | The mail address of zone admin. A @-sign will automatically be replaced with a dot in the zone data |
| server  | string | false    | 'opnsense.localdomain             | dns_server          | The DNS server hosting this file. This should usually be the FQDN of your firewall where the BIND plugin is installed |
| reload       | boolean | false    | true                 | -         | If the running config should be reloaded on change - this will take some time. For mass-managing items you might want to reload it 'manually' after all changes are done => using the [reload module](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_reload.md). |

**Note:**

A domain can only be removed if no records linked to it exist.

Else it will leave the configuration in a state where you'll have to edit the backup-xml and restore it to remove those records as they will not show in the Web-UI and cannot be addressed using the module.

It seems the plugin lacks validation in that case.


### ansibleguy.opnsense.bind_record

| Parameter | Type    | Required | Default value | Aliases     | Comment                                                                                                                                                                                                                                            |
|:----------|:--------|:---------|:--------------|:------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| match_fields     | list  | false     | ['domain', 'name', 'type']             | -           | Fields that are used to match configured records with the running config - if any of those fields are changed, the module will think it's a new record. At least one of: 'domain', 'name', 'type', 'value'                                         |
| name      | string  | true     | -             | record      | Name of the record                                                                                                                                                                                                                                 |
| domain      | string  | true     | -             | domain_name | Existing domain/zone for the record                                                                                                                                                                                                                |
| type      | string  | false    | 'A'           | -           | Type of the record. One of: 'A', 'AAAA', 'CAA', 'CNAME', 'DNSKEY', 'DS', 'MX', 'NS', 'PTR', 'RRSIG', 'SRV', 'TLSA', 'TXT'                                                                                                                          |
| value      | false for state changes, else true  | false    | ''            | -           | Value the record should hold                                                                                                                                                                                                                       |
| round_robin      | boolean | false    | false         | -           | If multiple records with the same domain/name/type combination exist - the module will only execute 'state=absent' if set to 'false'. To create multiple ones set this to 'true'. Records will only be created, NOT UPDATED! (no matching is done) |
| reload       | boolean | false    | true                 | -         | If the running config should be reloaded on change - this will take some time. For mass-managing items you might want to reload it 'manually' after all changes are done => using the [reload module](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_reload.md). |


### ansibleguy.opnsense.bind_record_multi

| Parameter | Type                               | Required | Default value              | Aliases | Comment                                                                                                                                                                                                                                                                                  |
|:----------|:-----------------------------------|:---------|:---------------------------|:--------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| records      | dictionary                         | true     | -                          | record  | Records to process. Format of the dictionary: {'domain1': [{'name': 'record1', 'value': '192.168.0.1'}, {'name': 'record2', 'type': 'TXT', 'value': 'random'}]} (_dictionary of domains with a list of record-dictionaries_)                                                             |
| match_fields     | list  | false     | ['domain', 'name', 'type'] | -       | Fields that are used to match configured records with the running config - if any of those fields are changed, the module will think it's a new record. At least one of: 'domain', 'name', 'type', 'value'                                                                               |
| fail_verification | boolean    | false    | false                      | fail_verify | Fail module if single record fails the verification                                                                                                                                                                                                                                      |
| fail_processing   | boolean    | false    | true                       | fail_proc   | Fail module if single record fails to be processed                                                                                                                                                                                                                                       |
| state | string     | false   | 'present'                  | -       | Options: 'present', 'absent'                                                                                                                                                                                                                                                             |
| enabled | boolean    | false | true                       | -       | If all records should be en- or disabled                                                                                                                                                                                                                                                 |
| output_info | boolean    | false | false                      | info    | Enable to show some information on processing at runtime. Will be hidden if the tasks 'no_log' parameter is set to 'true'.                                                                                                                                                               |
| reload       | boolean | false    | true                       | -         | If the running config should be reloaded on change - this will take some time. For mass-managing items you might want to reload it 'manually' after all changes are done => using the [reload module](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_reload.md). |


## Info

### Mass manage

If you want to mass-manage DNS records - use the [bind_record_multi](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_bind.md#ansibleguyopnsensebind_record_multi-1) module. It scales better for that use-case!

For other modules:

* If you are mass-managing DNS records or using DNS-Blocklists - you might want to disable ```reload: false``` on single module-calls!

* This takes a long time, as the service gets reloaded every time!

* You might want to reload it 'manually' after all changes are done => using the [reload module](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_reload.md)

### Round-Robin

The management of [round-robin](https://en.wikipedia.org/wiki/Round-robin_DNS) records is a harder to manage by the module as a single record cannot be identified!

Therefor the 'bind_record' module has an 'round_robin' argument.

#### Default mode

With it set to 'false' (_default_) only one record with the exact combination of domain/type/name will be accepted.

Else the module will throw an error!

In this mode the management (_create/update/delete_) of those single records is completely logical.

#### round-robin mode

If you need to set it to 'true' - its usage changes a little.

Updating the value of a single record within a round-robin is not possible!

**Deletion**

You could delete a single one of the records by setting the 'match_fields' argument to ['domain', 'name', 'type', 'value'] and therefor matching its value.

But the default behaviour is that you can only delete all of them at once.

If a change is needed, you will have to run the module using 'state=absent' first and then re-create all the records.


## Examples

### ansibleguy.opnsense.bind_general

```yaml
- hosts: localhost
  gather_facts: no
  module_defaults:
    ansibleguy.opnsense.bind_general:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'

    ansibleguy.opnsense.list:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'
      target: 'bind_general'

  tasks:
    - name: Example
      ansibleguy.opnsense.bind_general:
        # enabled: true
        # ipv6: true
        # response_policy_zones: true
        # port: 53530
        # listen_ipv4: ['127.0.0.1']
        # listen_ipv6: ['::1']
        # query_source_ipv4: ''
        # transfer_source_ipv4: ''
        # query_source_ipv6: ''
        # transfer_source_ipv6: ''
        # forwarders: []
        # filter_aaaa_v4: false
        # filter_aaaa_v6: false
        # filter_aaaa_acl: []
        # log_size: 5
        # cache_size: 50
        # recursion_acl: ''
        # transfer_acl: ''
        # dnssec_validation: 'no'
        # hide_hostname: false
        # hide_version: true
        # prefetch: true
        # ratelimit: true
        # ratelimit_count: 
        # ratelimit_except: ['127.0.0.1', '::1']
        # reload: true

    - name: Configuring BIND
      ansibleguy.opnsense.bind_general:
        enabled: true
        listen_ipv4: ['127.0.0.1', '192.168.0.1']
        query_source_ipv4: '192.168.0.1'
        transfer_source_ipv4: '192.168.0.1'
        filter_aaaa_v4: false
        filter_aaaa_acl: ['192.168.0.2', '192.168.0.4']
        dnssec_validation: 'no'
        hide_hostname: true
        hide_version: true
        ratelimit: true
        prefetch: false
        ratelimit_count: 50
        log_size: 10
        response_policy_zones: false
        ipv6: false

    - name: Pulling settings
      ansibleguy.opnsense.list:
      #  target: 'bind_general'
      register: existing_entries

    - name: Printing settings
      ansible.builtin.debug:
        var: existing_entries.data
```

### ansibleguy.opnsense.bind_blocklist

```yaml
- hosts: localhost
  gather_facts: no
  module_defaults:
    ansibleguy.opnsense.bind_blocklist:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'

    ansibleguy.opnsense.list:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'
      target: 'bind_blocklist'

  tasks:
    - name: Example
      ansibleguy.opnsense.bind_blocklist:
        # enabled: true
        # block: []
        # exclude: []
        # safe_google: false
        # safe_duckduckgo: false
        # safe_youtube: false
        # safe_bing: false
        # reload: true

    - name: Configuring blocklists
      ansibleguy.opnsense.bind_blocklist:
        block: ['Steven Black List', 'NoCoin List', 'Blocklist.site Phishing', 'AdGuard List']
        exclude: ['test.ansibleguy.net', 'ansibleguy.net']
        safe_google: true
        safe_youtube: true

    - name: Disabling blocklists
      ansibleguy.opnsense.bind_blocklist:
        enabled: false
        block: ['Steven Black List', 'NoCoin List', 'Blocklist.site Phishing', 'AdGuard List']
        exclude: ['test.ansibleguy.net', 'ansibleguy.net']
        safe_google: true
        safe_youtube: true

    - name: Listing blocklists
      ansibleguy.opnsense.list:
      #  target: 'bind_blocklist'
      register: existing_entries

    - name: Printing blocklists
      ansible.builtin.debug:
        var: existing_entries.data
```

### ansibleguy.opnsense.bind_acl

```yaml
- hosts: localhost
  gather_facts: no
  module_defaults:
    ansibleguy.opnsense.bind_acl:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'

    ansibleguy.opnsense.list:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'
      target: 'bind_acl'

  tasks:
    - name: Example
      ansibleguy.opnsense.bind_acl:
        name: 'example'
        # enabled: true
        # networks: []
        # reload: true

    - name: Adding
      ansibleguy.opnsense.bind_acl:
        name: 'test1'
        networks: ['192.168.0.0/24']

    - name: Changing
      ansibleguy.opnsense.bind_acl:
        name: 'test1'
        networks: ['192.168.1.0/25']

    - name: Disabling
      ansibleguy.opnsense.bind_acl:
        name: 'test1'
        networks: ['192.168.1.0/25']
        enabled: false

    - name: Listing
      ansibleguy.opnsense.list:
        # target: 'bind_acl'
      register: existing_entries

    - name: Printing tests
      ansible.builtin.debug:
        var: existing_entries.data

    - name: Removing
      ansibleguy.opnsense.bind_acl:
        name: 'test1'
        state: 'absent'
```

### ansibleguy.opnsense.bind_domain

```yaml
- hosts: localhost
  gather_facts: no
  module_defaults:
    ansibleguy.opnsense.bind_domain:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'

    ansibleguy.opnsense.list:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'
      target: 'bind_domain'

  tasks:
    - name: Example
      ansibleguy.opnsense.bind_domain:
        name: 'example.ansibleguy'
        # enabled: true
        # mode: 'master'
        # transfer_key_algo: ''
        # transfer_key_name: ''
        # transfer_key: ''
        # allow_notify: []
        # transfer_acl: ''
        # query_acl: ''
        # ttl: 86400
        # refresh: 21600
        # retry: 3600
        # expire: 3542400
        # negative: 3600
        # admin_mail: 'mail.opnsense.localdomain'
        # server: 'opnsense.localdomain'
        # reload: true

    - name: Adding
      ansibleguy.opnsense.bind_domain:
        name: 'test1.ansibleguy'
        transfer_key_algo: 'hmac-sha512'
        transfer_key_name: 'test'
        transfer_key: "{{ 'randomsecret' | b64encode }}"
        ttl: 14400
        retry: 1800

    - name: Changing
      ansibleguy.opnsense.bind_domain:
        name: 'test1.ansibleguy'
        transfer_key_algo: 'hmac-sha512'
        transfer_key_name: 'test'
        transfer_key: "{{ 'randomsecretNEW' | b64encode }}"
        ttl: 14400
        retry: 1800
        transfer_acl: 'test1_acl'

    - name: Disabling
      ansibleguy.opnsense.bind_domain:
        name: 'test1.ansibleguy'
        enabled: false

    - name: Listing
      ansibleguy.opnsense.list:
        # target: 'bind_domain'
      register: existing_entries

    - name: Printing tests
      ansible.builtin.debug:
        var: existing_entries.data

    - name: Removing
      ansibleguy.opnsense.bind_domain:
        name: 'test1.ansibleguy'
        state: 'absent'
```

### ansibleguy.opnsense.bind_record

```yaml
- hosts: localhost
  gather_facts: no
  module_defaults:
    ansibleguy.opnsense.bind_record:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'

    ansibleguy.opnsense.list:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'
      target: 'bind_record'

  tasks:
    - name: Example
      ansibleguy.opnsense.bind_record:
        domain: 'template.ansibleguy'
        name: 'example'
        # value: ''
        # type: 'A'
        # round_robin: false
        # enabled: true
        # match_fields: ['domain', 'name', 'type']
        # reload: true

    - name: Adding
      ansibleguy.opnsense.bind_record:
        domain: 'template.ansibleguy'
        name: 'test1'
        value: '192.168.0.1'

    - name: Changing
      ansibleguy.opnsense.bind_record:
        domain: 'template.ansibleguy'
        name: 'test1'
        value: '192.168.1.1'

    - name: Disabling
      ansibleguy.opnsense.bind_record:
        domain: 'template.ansibleguy'
        name: 'test1'
        value: '192.168.1.1'
        enabled: false

    - name: Listing
      ansibleguy.opnsense.list:
        # target: 'bind_record'
      register: existing_entries

    - name: Printing tests
      ansible.builtin.debug:
        var: existing_entries.data

    - name: Removing
      ansibleguy.opnsense.bind_record:
        domain: 'template.ansibleguy'
        name: 'test1'
        state: 'absent'
```

### ansibleguy.opnsense.bind_record_multi

```yaml
- hosts: localhost
  gather_facts: no
  module_defaults:
    ansibleguy.opnsense.bind_record_multi:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'

  tasks:
    - name: Example
      ansibleguy.opnsense.bind_record_multi:
        records:
          'template.ansibleguy':  # domain
            - name: 'example'
              value: '192.168.1.1'
        # fail_verification: false
        # fail_processing: false
        # enabled: true
        # match_fields: ['domain', 'name', 'type']
        # reload: true
        # output_info: false

    - name: Adding
      ansibleguy.opnsense.bind_record_multi:
        records:
          'template.ansibleguy':
            - name: 'test1'
              value: '192.168.1.1'
            - name: 'test1'
              type: 'TXT'
              value: 'random'
            - name: 'test2'
              value: '192.168.2.1'
            - name: 'test3'
              value: '192.168.3.1'
            - name: 'test4'
              type: 'CNAME'
              value: 'test1.test3.ansibleguy'

    - name: Changing
      ansibleguy.opnsense.bind_record_multi:
        records:
          'template.ansibleguy':
            - name: 'test1'
              value: '192.168.1.2'
            - name: 'test1'
              type: 'TXT'
              value: 'random_new'
            - name: 'test2'
              value: '192.168.2.1'
              enabled: false
            - name: 'test3'
              state: 'absent'
            - name: 'test4'
              type: 'CNAME'
              value: 'test2.test3.ansibleguy'

    - name: Disabling all
      ansibleguy.opnsense.bind_record_multi:
        records:
          'template.ansibleguy':
            - name: 'test1'
              value: '192.168.1.2'
            - name: 'test1'
              type: 'TXT'
              value: 'random_new'
            - name: 'test2'
              value: '192.168.2.1'
            - name: 'test3'
              state: 'absent'
            - name: 'test4'
              type: 'CNAME'
              value: 'test2.test3.ansibleguy'
        enabled: false

    - name: Removing all
      ansibleguy.opnsense.bind_record_multi:
        records:
          'template.ansibleguy':
            - 'test1'
            - name: 'test1'
              type: 'TXT'
            - 'test2'
            - 'test3'
            - name: 'test4'
              type: 'CNAME'
        state: 'absent'
```
