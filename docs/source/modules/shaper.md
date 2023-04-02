# Traffic Shaper

**STATE**: stable

**TESTS**: [shaper_pipe](https://github.com/ansibleguy/collection_opnsense/blob/latest/tests/shaper_pipe.yml) | 
[shaper_queue](https://github.com/ansibleguy/collection_opnsense/blob/latest/tests/shaper_queue.yml) | 
[shaper_rule](https://github.com/ansibleguy/collection_opnsense/blob/latest/tests/shaper_rule.yml)

**API Docs**: [Core - Traffic Shaper](https://docs.opnsense.org/development/api/core/trafficshaper.html)

**Service Docs**: [Traffic Shaping](https://docs.opnsense.org/manual/shaping.html)

## Info

The description is used to match the configured entries with the existing ones. It must be unique!

Interfaces for 'shaper_rules' must be provided as used in the network config (_p.e. 'opt1' instead of 'DMZ'_)

  * per example see menu: 'Interface - Assignments - Interface ID (in brackets)'
  * this brings problems if the interface-names are not the same on both nodes when using HA-setups


## Definition

For basic parameters see: [Basics](https://github.com/ansibleguy/collection_opnsense/blob/latest/docs/use_basic.md#definition)

### ansibleguy.opnsense.shaper_pipe

| Parameter    | Type            | Required                                   | Default value | Aliases   | Comment                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
|:-------------|:----------------|:-------------------------------------------|:--------------|:----------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| description  | string          | true                                       | -             | desc      | Description for the pipe - will be used to identify the entry. It must be unique!                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| bandwidth           | int             | false for state changes, else true | -             | bw        | Bandwidth limit for the pipe - used in combination with 'bw_metric'                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| bandwidth_metric    | string          | false                                      | Mbit          | bw_metric | Metric of the provided bandwidth - one of: 'bit', 'Kbit', 'Mbit', 'Gbit'                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| queue        | int             | false                                      | -             | -         | Integer between 2 and 100                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| mask         | string          | false                                      | -             | -         | One of: 'none', 'src-ip', 'dst-ip'. Dynamic pipe creation by source or destination address. Choose destination to give every IP in destination field of rules the specified bandwidth. A pipe with 1Mbit e.g. would let 3 clients lend 1Mbit each so 3Mbit max. Normally this is used for download pipes. Choose source to give every IP in the source field of rules the specified bandwidth. Normally this is used for upload pipes. Leave this value empty if you want to create a pipe with a fixed bandwidth. |
| scheduler        | string             | false                                      | -             | -         | One of: 'fifo', 'rr', 'qfq', 'fq_codel', 'fq_pie'                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| delay        | int             | false                                      | -             | -         | Integer between 1 and 3000                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| pie_enable       | boolean         | false                                      | false          | -         | Enable PIE active queue management                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| codel_enable       | boolean         | false                                      | false         | -         | Enable CoDel active queue management                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| codel_ecn_enable       | boolean         | false                                      | false          | -         |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| codel_target        | int             | false                                      | -             | -         | Integer between 1 and 10000                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| codel_interval        | int             | false                                      | -             | -         | Integer between 1 and 10000                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| fqcodel_quantum        | int             | false                                      | -             | -         | Integer between 1 and 65535                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| fqcodel_limit        | int             | false                                      | -             | -         | Integer between 1 and 65535                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| fqcodel_flows        | int             | false                                      | -             | -         | Integer between 1 and 65535                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| buckets        | int             | false                                      | -             | -         | Integer between 1 and 65535                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |

### ansibleguy.opnsense.shaper_queue

| Parameter    | Type            | Required                                   | Default value | Aliases | Comment                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
|:-------------|:----------------|:-------------------------------------------|:--------------|:--------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| description  | string          | true                                       | -             | desc    | Description for the queue - will be used to identify the entry. It must be unique!                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| pipe  | string          | false for state changes, else true                                       | -             | -       | Pipe to link to the queue                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| weight         | string          | false for state changes, else true                                      | -             | -                | Integer between 1 and 100                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| mask         | string          | false                                      | -             | -                | One of: 'none', 'src-ip', 'dst-ip'. Dynamic queue creation by source or destination address. Choose destination to evenly share every IP in destination field of rules the specified bandwidth. A pipe with 1Mbit e.g. would let 4 clients lend 250Kbit each. Normally this is used for download queues. Choose source to evenly share every IP in the source field of rules the specified bandwidth. Normally this is used for upload queues. Leave this value empty if you want to specify multiple queues with different weights. |
| pipe  | string          | false for state changes, else true                                       | -             | -       | Pipe to link to the queue                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| pie_enable       | boolean         | false                                      | false          | -       | Enable PIE active queue management                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| codel_enable       | boolean         | false                                      | false         | -       | Enable CoDel active queue management                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| codel_ecn_enable       | boolean         | false                                      | false          | -       |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| codel_target        | int             | false                                      | -             | -                | Integer between 1 and 10000                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| codel_interval        | int             | false                                      | -             | -                | Integer between 1 and 10000                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| buckets        | int             | false                                      | -             | -                | Integer between 1 and 65535                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |

### ansibleguy.opnsense.shaper_rule

| Parameter    | Type    | Required                               | Default value | Aliases                           | Comment                                                                                                                     |
|:-------------|:--------|:---------------------------------------|:--------------|:----------------------------------|:----------------------------------------------------------------------------------------------------------------------------|
| description  | string  | true                                   | -             | desc                              | Description for the rule - will be used to identify the entry. It must be unique!                                           |
| target_pipe  | string  | true, false if 'target_queue' provided | -             | pipe                              | Pipe to link to the rule, alternative to 'target_queue'                                                                     |
| target_queue  | string  | true, false if 'target_pipe' provided                                  | -             | queue                             | Pipe to link to the rule, alternative to 'target_pipe'                                                                      |
| sequence        | int     | false                                  | -             | seq                               | Integer between 1 and 1000000                                                                                               |
| interface  | string  | false                                  | 'lan'         | int, i                            | Matching packets traveling to/from interface                                                                                |
| interface2  | string  | false                                  | -             | int2, i2                          | Secondary interface, matches packets traveling to/from interface (1) to/from interface (2). can be combined with direction. |
| protocol  | string  | false                                  | -             | proto, p                          | Protocol like 'ip', 'ipv4', 'tcp', 'udp' and so on - for options see the WEB-UI                                             |
| max_packet_length        | int     | false                                  | -             | max_packet_len, packet_len, iplen | Integer between 2 and 65535                                                                                                 |
| source_invert     | boolean | false                                  | false         | si, src_inv, src_not              | Inverted matching of the source                                                                                             |
| source_net     | string  | false                                  | 'any'         | s, src, source                    | Host, network or 'any', alias not supported                                                                                 |
| source_port     | string  | false                                  | -             | sp, src_port                      | Leave empty to allow all, alias not supported                                                                               |
| destination_invert     | boolean | false                                  | false         | di, dest_inv, dest_not            | Inverted matching of the destination                                                                                        |
| destination_net     | string  | false                                  | 'any'         | d, dest, destination              | Host, network or 'any', alias not supported                                                                                 |
| destination_port     | string  | false                                  | -             | dp, dest_port                     | Leave empty to allow all, alias not supported                                                                               |
| dscp     | list    | false                                  | -             | -                                 | One or multiple DSCP values - one of: 'be', 'ef', 'af11', 'af12', 'af13', 'af21', 'af22', 'af23', 'af31', 'af32', 'af33', 'af41', 'af42', 'af43', 'cs1', 'cs2', 'cs3', 'cs4', 'cs5', 'cs6', 'cs7'  |
| direction     | string  | false                                  | 'both'          | -                                 | One of: 'in', 'out', leave empty for 'both'                                                                                 |


## Examples

### Pipes

```yaml
- hosts: localhost
  gather_facts: no
  module_defaults:
    group/ansibleguy.opnsense.all:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'

    ansibleguy.opnsense.list:
      target: 'shaper_pipe'

  tasks:
    - name: Example
      ansibleguy.opnsense.shaper_pipe:
        description: 'example'
        bandwidth: 50
        # bandwidth_metric: 'Mbit'
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

### Queues

```yaml
- hosts: localhost
  gather_facts: no
  module_defaults:
    group/ansibleguy.opnsense.all:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'

    ansibleguy.opnsense.list:
      target: 'shaper_queue'

  tasks:
    - name: Example
      ansibleguy.opnsense.shaper_queue:
        description: 'example'
        pipe: 'example'
        weight: 50
        # mask: 'none'
        # buckets: 100
        # pie_enable: false
        # codel_enable: false
        # codel_ecn_enable: false
        # codel_target: 100
        # codel_interval: 100
        # enabled: true
        # debug: false
        # state: 'present'

    - name: Adding pipe
      ansibleguy.opnsense.shaper_pipe:
        description: 'testPipe1'
        bandwidth: 50

    - name: Adding queue
      ansibleguy.opnsense.shaper_queue:
        description: 'testQueue1'
        pipe: 'testPipe1'
        weight: 50

    - name: Disabling queue
      ansibleguy.opnsense.shaper_queue:
        description: 'testQueue1'
        pipe: 'testPipe1'
        weight: 50
        enabled: false

    - name: Listing queue
      ansibleguy.opnsense.list:
        target: 'shaper_queue'
      register: existing_entries

    - name: Printing queues
      ansible.builtin.debug:
        var: existing_entries.data

    - name: Removing queues
      ansibleguy.opnsense.shaper_queue:
        description: 'testQueue1'
        state: 'absent'
```

### Rules

```yaml
- hosts: localhost
  gather_facts: no
  module_defaults:
    group/ansibleguy.opnsense.all:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'

    ansibleguy.opnsense.list:
      target: 'shaper_rule'

  tasks:
    - name: Example
      ansibleguy.opnsense.shaper_rule:
        description: 'example'
        target_pipe: 'example'
        target_queue: 'example'
        # sequence: 1
        # interface: 'lan'
        # interface2: 'wan'
        # max_packet_length: 1024
        # protocol: 'ip'
        # source_invert: false
        # source_net: 'any'
        # source_port: 'any'
        # destination_invert: false
        # destination_net: 'any'
        # destination_port: 'any'
        # dscp: ['be']
        # direction: 'in'
        # enabled: true
        # debug: false
        # state: 'present'

    - name: Adding pipe
      ansibleguy.opnsense.shaper_pipe:
        description: 'testPipe1'
        bandwidth: 50

    - name: Adding queue
      ansibleguy.opnsense.shaper_queue:
        description: 'testQueue1'
        pipe: 'testPipe1'
        weight: 50

    - name: Adding rule - link it to queue
      ansibleguy.opnsense.shaper_rule:
        description: 'testRule1'
        target_queue: 'testQueue1'
        protocol: 'tcp'
        destination_port: 80

    - name: Adding rule - link it to pipe
      ansibleguy.opnsense.shaper_rule:
        description: 'testRule2'
        target_pipe: 'testPipe1'
        destination_invert: true
        destination: '172.16.0.0/12'

    - name: Disabling rule
      ansibleguy.opnsense.shaper_rule:
        description: 'testRule1'
        target_queue: 'testQueue1'
        protocol: 'tcp'
        destination_port: 80
        enabled: false

    - name: Listing rules
      ansibleguy.opnsense.list:
        target: 'shaper_rule'
      register: existing_entries

    - name: Printing rules
      ansible.builtin.debug:
        var: existing_entries.data

    - name: Removing rule
      ansibleguy.opnsense.shaper_queue:
        description: 'testRule1'
        state: 'absent'
```
