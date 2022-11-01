# OPNSense - Alias module

**STATE**: stable

**TESTS**: [Playbook](https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/alias.yml)

**API DOCS**: [Core - Firewall](https://docs.opnsense.org/development/api/core/firewall.html)

**BASE DOCS**: [Aliases](https://docs.opnsense.org/manual/aliases.html)

This module allows you to manage single aliases.


## Info

For more detailed information on what alias types are supported - see [the documentation](https://docs.opnsense.org/manual/aliases.html).

To use GeoIP alias types - you need to configure a source for it first. See: [documentation](https://docs.opnsense.org/manual/how-tos/maxmind_geo_ip.html)


### Mass-Manage

If you want to mass-manage aliases - take a look at the [alias_multi](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_alias_multi.md) module. It is scales better for that use-case!


## Definition

| Parameter       | Type        | Required                           | Default value | Comment                                                                                                                                                          |
|:----------------|:------------|:-----------------------------------|:--------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| name            | string      | true                               | -             | Unique name of the alias                                                                                                                                         |
| description     | string      | false                              | -             | Description for the alias                                                                                                                                        |
| content         | list        | false for state changes, else true | -             | Values the alias should hold                                                                                                                                     | 
| type            | string      | false                              | 'host'        | Type of value the alias should hold. One of: 'host', 'network', 'port', 'url', 'urltable', 'geoip', 'networkgroup', 'mac', 'dynipv6host', 'internal', 'external' |
| state           | string      | false                              | 'present'     | Options: 'present', 'absent'                                                                                                                                     |
| enabled         | boolean     | false                              | true          | If the alias should be en- or disabled                                                                                                                           |
| updatefreq_days | float       | false                              | 7.0           | Needed only for the alias-type 'urltable'. Interval to update its content. Per example: 0.5 for every 12 hours                                                   |
| reload          | boolean | false                              | false         | -                                                                                                                                                                | If the running config should be reloaded on change - this will take some time. For mass-managing items you might want to reload it 'manually' after all changes are done => using the [reload module](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_reload.md). Defaults to 'false' as it is only needed in edge-cases and takes a long time. |

For basic parameters see: [Basics](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_basic.md#definition)

## Examples

```yaml
- hosts: localhost
  gather_facts: no
  module_defaults:
    ansibleguy.opnsense.alias:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'

    ansibleguy.opnsense.list:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'
      target: 'alias'

    ansibleguy.opnsense.reload:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'
      target: 'alias'

  tasks:
    - name: Example
      ansibleguy.opnsense.alias:
        name: 'ANSIBLE_TEST1'
        description: 'just a test'
        content: '1.1.1.1'
        state: 'present'
        # type: 'host'  # default
        # updatefreq_days: 3  # used only for type 'urltable'
        # ssl_ca_file: '/etc/ssl/certs/custom/ca.crt'
        # ssl_verify: False
        # api_key: !vault ...  # alternative to 'api_credential_file'
        # api_secret: !vault ...
        # debug: false

    - name: Adding
      ansibleguy.opnsense.alias:
        name: 'ANSIBLE_TEST2'
        content: '192.168.1.1'

    - name: Listing
      ansibleguy.opnsense.list:
      #  target: 'alias'
      register: existing_entries

    - name: Printing aliases
      ansible.builtin.debug:
        var: existing_entries.data  # type = list of dicts

    - name: Changing
      ansibleguy.opnsense.alias:
        name: 'ANSIBLE_TEST2'
        content: ['192.168.1.5', '192.168.10.4']

    - name: Removing
      ansibleguy.opnsense.alias:
        name: 'ANSIBLE_TEST3'
        state: 'absent'

    - name: Disabling
      ansibleguy.opnsense.alias:
        name: 'ANSIBLE_TEST2'
        enabled: false

    - name: Adding ports
      ansibleguy.opnsense.alias:
        name: 'ANSIBLE_TEST3'
        type: 'port'
        content: [80, 443, '9000:9002']

    - name: Adding url-table
      ansibleguy.opnsense.alias:
        name: 'ANSIBLE_TEST4'
        type: 'urltable'
        updatefreq_days: 2.6
        content: 'https://www.spamhaus.org/drop/drop.txt'

    - name: Adding dns-names
      ansibleguy.opnsense.alias:
        name: 'ANSIBLE_TEST5'
        content:
          - 'acme-v02.api.letsencrypt.org'
          - 'staging-v02.api.letsencrypt.org'
          - 'r3.o.lencr.org'

    - name: Adding network
      ansibleguy.opnsense.alias:
        name: 'ANSIBLE_TEST6'
        type: 'network'
        content: '192.168.0.0/24'

    - name: Adding geoips regions
      ansibleguy.opnsense.alias:
        name: 'ANSIBLE_TEST_1_2_GEOIP2'
        type: 'geoip'
        content: ['AT', 'DE', 'CH']

    - name: Reloading running config
      ansibleguy.opnsense.reload:
      #  target: 'alias'
```
