# OPNSense - Traffic shaper modules

**STATE**: unstable

**TESTS**: [shaper_pipe](https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/shaper_pipe.yml)

**API DOCS**: [Core - Traffic Shaper](https://docs.opnsense.org/development/api/core/trafficshaper.html)

## Definition

For basic parameters see: [Basics](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_basic.md#definition)

### ansibleguy.opnsense.shaper_pipe

| Parameter    | Type            | Required                                   | Default value | Aliases          | Comment                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
|:-------------|:----------------|:-------------------------------------------|:--------------|:-----------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| description  | string          | true                                       | -             | desc             | Description for the pipe - will be used to identify the entry. It must be unique!                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| bw           | int             | true for creation, false for state changes | -             | bandwidth        | Bandwidth limit for the pipe - used in combination with 'bw_metric'                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| bw_metric    | string          | false                                      | Mbit          | bandwidth_metric | Metric of the provided bandwidth - one of: 'bit', 'Kbit', 'Mbit', 'Gbit'                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| queue        | int             | false                                      | -             | -                | Integer between 2 and 100                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| mask         | string          | false                                      | -             | -                | One of: 'none', 'src-ip', 'dst-ip'. Dynamic pipe creation by source or destination address. Choose destination to give every IP in destination field of rules the specified bandwidth. A pipe with 1Mbit e.g. would let 3 clients lend 1Mbit each so 3Mbit max. Normally this is used for download pipes. Choose source to give every IP in the source field of rules the specified bandwidth. Normally this is used for upload pipes. Leave this value empty if you want to create a pipe with a fixed bandwidth. |
| buckets        | int             | false                                      | -             | -                | Integer between 1 and 65535                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| scheduler        | string             | false                                      | -             | -                | One of: 'fifo', 'rr', 'qfq', 'fq_codel', 'fq_pie'                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| delay        | int             | false                                      | -             | -                | Integer between 1 and 3000                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| pie_enable       | boolean         | false                                      | false          | -                | Enable PIE active queue management                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| codel_enable       | boolean         | false                                      | false         | -                | Enable CoDel active queue management                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| codel_ecn_enable       | boolean         | false                                      | false          | -                |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| codel_target        | int             | false                                      | -             | -                | Integer between 1 and 10000                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| codel_interval        | int             | false                                      | -             | -                | Integer between 1 and 10000                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| fqcodel_quantum        | int             | false                                      | -             | -                | Integer between 1 and 65535                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| fqcodel_limit        | int             | false                                      | -             | -                | Integer between 1 and 65535                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| fqcodel_flows        | int             | false                                      | -             | -                | Integer between 1 and 65535                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |


## Usage

The pipe's description is used to match the configured entries with the existing ones. It must be unique!


## Examples

```yaml
- hosts: localhost
  gather_facts: no
  module_defaults:
    ansibleguy.opnsense.shaper_pipe:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'

    ansibleguy.opnsense.list:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'

  tasks:
    - name: Example
      ansibleguy.opnsense.shaper_pipe:
        description: 'example'
        bandwidth: 50
        # bw_metric: 'Mbit'
        # queue: 50
        # mask: 'none'
        # buckets: 100
        # pie_enable: false
        # codel_enable: false
        # codel_ecn_enable: false
        # codel_target: 100
        # codel_interval: 100
        # fqcodel_quantum: 100
        # fqcodel_limit: 100
        # fqcodel_flows: 100
        # delay: 100
        # enabled: true
        # debug: false
        # state: 'present'

    - name: Adding pipe
      ansibleguy.opnsense.shaper_pipe:
        description: 'test1'
        bandwidth: 50

    - name: Disabling pipe
      ansibleguy.opnsense.shaper_pipe:
        description: 'test1'
        bandwidth: 50
        enabled: false

    - name: Listing pipes
      ansibleguy.opnsense.list:
        target: 'shaper_pipe'
      register: existing_entries

    - name: Printing pipes
      ansible.builtin.debug:
        var: existing_entries.data

    - name: Removing pipe
      ansibleguy.opnsense.shaper_pipe:
        description: 'test1'
        state: 'absent'
```
