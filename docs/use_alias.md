# OPNSense - Alias module

**STATE**: unstable

**TESTS**: [Playbook](https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/alias.yml)

**API DOCS**: [Core - Firewall](https://docs.opnsense.org/development/api/core/firewall.html)

This module allows you to manage single aliases.


## Info

For more detailed information on what alias types are supported - see [the documentation](https://docs.opnsense.org/manual/aliases.html).

To use GeoIP alias types - you need to configure a source for it first. See: [documentation](https://docs.opnsense.org/manual/how-tos/maxmind_geo_ip.html)


### Mass-Manage

If you want to mass-manage aliases - take a look at the [alias_multi](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_alias_multi.md) module. It is scales better for that use-case!


## Usage

```yaml
- hosts: localhost
  gather_facts: no
  module_defaults:
    ansibleguy.opnsense.alias:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'

    ansibleguy.opnsense.alias_list:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'

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
      ansibleguy.opnsense.alias_list:
      register: existing_aliases
      
    - name: Printing aliases
      ansible.builtin.debug:
        var: existing_aliases.aliases

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
```
