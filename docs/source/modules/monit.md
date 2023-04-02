# Monit

**STATE**: stable

**TESTS**: [Playbook](https://github.com/ansibleguy/collection_opnsense/blob/latest/tests/monit.yml)

**API Docs**: [Core - Monit](https://docs.opnsense.org/development/api/core/monit.html)

**Service Docs**: [Monit](https://docs.opnsense.org/manual/monit.html)

## Info

For mail alerts to work:

* Don't forget to configure your mailing settings at the general monit page
* You will also need to set your sender-mail address in the 'format' field using the 'monit_alert' module. See the examples below.

Interfaces for 'monit_services' must be provided as used in the network config (_p.e. 'opt1' instead of 'DMZ'_)
  * per example see menu: 'Interface - Assignments - Interface ID (in brackets)'
  * this brings problems if the interface-names are not the same on both nodes when using HA-setups

## Definition

For basic parameters see: [Basics](https://github.com/ansibleguy/collection_opnsense/blob/latest/docs/use_basic.md#definition)

### ansibleguy.opnsense.monit_alert

| Parameter    | Type    | Required | Default value | Aliases        | Comment                                                                                                                                                                                                                                                                                                                                                                                                   |
|:-------------|:--------|:---------|:--------------|:---------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| recipient            | string  | true     | -             | email, mail    | Mail address to send the alert to                                                                                                                                                                                                                                                                                                                                                                         |
| not_on            | boolean | false    | true          | not            | Do not send alerts for the following events but on all others                                                                                                                                                                                                                                                                                                                                             |
| events            | list    | false    | -             | -              | Filter event-types to alert on. Invertable using the 'not_on' parameter. One or multiple of: 'action', 'checksum', 'bytein', 'byteout', 'connection', 'content', 'data', 'exec', 'fsflags', 'gid', 'icmp', 'instance', 'invalid', 'link', 'nonexist', 'packetin', 'packetout', 'permission', 'pid', 'ppid', 'resource', 'saturation', 'size',  'speed', 'status', 'timeout', 'timestamp', 'uid', 'uptime' |
| format            | string  | false    | -             | -              | The email format for alerts. Subject: $SERVICE on $HOST failed. “Mail format” is a newline-separated list of properties to control the mail formatting. It is also needed to correctly set the From address                                                                                                                                                                                                                                                                                                                                          |
| reminder            | int     | false    | 10            | -              | Send a reminder after some cycles. Integer between 0 and 86400                                                                                                                                                                                                                                                                                                                                            |
| description            | string     | false    | -             | desc              | Send a reminder after some cycles                                                                                                                                                                                                                                                                                                                                                                         |
| match_fields            | string     | false    | ['recipient'] | -          | Fields that are used to match configured alerts with the running config - if any of those fields are changed, the module will think it's a new entry. At least one of: 'recipient', 'not_on', 'events', 'reminder', 'description'                                                                                                                                                                         |

### ansibleguy.opnsense.monit_test

| Parameter    | Type    | Required                                    | Default value | Aliases | Comment                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
|:-------------|:--------|:--------------------------------------------|:--------------|:--------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| name            | string  | true                                        | -             | -       | Unique name of the test                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| type            | string  | false                                       | 'Custom'      | -       | Type of test. 'Custom' will not be idempotent - will be translated on the server-side. See 'list' module output for details. One of: 'Existence', 'SystemResource', 'ProcessResource', 'ProcessDiskIO', 'FileChecksum', 'Timestamp', 'FileSize', 'FileContent', 'FilesystemMountFlags', 'SpaceUsage', 'InodeUsage', 'DiskIO', 'Permisssion', 'UID', 'GID', 'PID', 'PPID', 'Uptime', 'ProgramStatus', 'NetworkInterface', 'NetworkPing', 'Connection', 'Custom' |
| condition            | string  | false for state changes, else true            | -             | -       | The test condition. Per example: 'cpu is greater than 50%' or 'failed host 127.0.0.1 port 22 protocol ssh'                                                                                                                                                                                                                                                                                                                                                     |
| action            | string  | false for state changes, else true            | 'alert'        | -       | One of: 'alert', 'restart', 'start', 'stop', 'exec', 'unmonitor'                                                                                                                                                                                                                                                                                                                                                                                               |
| path            | path  | false, true if present and type is 'execute' | -             | -       | The absolute path to the script to execute - if action is set to 'execute'. Make sure the script is executable by the Monit service                                                                                                                                                                                                                                                                                                                                                                                   |

### ansibleguy.opnsense.monit_service

| Parameter | Type   | Required                                        | Default value | Aliases     | Comment                                                                                                                                                                                   |
|:----------|:-------|:------------------------------------------------|:--------------|:------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| name      | string | true                                            | -             | -           | Unique service name                                                                                                                                                                       |
| type      | string | false for state changes, else true                | -             | -           | One of: 'process', 'file', 'fifo', 'filesystem', 'directory', 'host', 'system', 'custom', 'network'                                                                                       |
| pidfile   | path   | false                                           | -             | -           |                                                                                                                                                                                           |
| match     | string | false                                           | -             | -           |                                                                                                                                                                                           |
| path      | path   | false                                           | -             | -           | According to the service type path can be a file or a directory                                                                                                                           |
| service_timeout   | path   | false                                           | -             | svc_timeout | Integer between 1 and 86400                                                                                                                                                               |
| address   | string | false, true if type is one of 'network', 'host' | -             | -           | The target IP address for 'host' and 'network' checks                                                                                                                                     |
| interface | string | false, true if type is one of 'network'         | -             | -           | The existing Interface for 'Network' checks. Alternative to 'address'                                                                                                                     |
| start | string | false         | -             | -           | Absolute path to the executable with its arguments to run at service-start                                                                                                                |
| stop | string | false         | -             | -           | Absolute path to the executable with its arguments to run at service-stop                                                                                                                 |
| tests | list   | false         | -             | -           | Name of tests to link to the service. Not all test-types are compatible with all service-types                                                                                            |
| depends | list   | false         | -             | -           | Optionally define a (list of) service(s) which are required before monitoring this one, if any of the dependencies are either stopped or unmonitored this service will stop/unmonitor too |
| polltime | string   | false         | -             | -           | Set the service poll time. Either as a number of cycles 'NUMBER CYCLES' or Cron-style '* 8-19 * * 1-5'                                                                                    |
| description | string   | false         | -             | -           |                                                                                                                                                                                           |


## Examples

### Alerts

```yaml
- hosts: localhost
  gather_facts: no
  module_defaults:
    group/ansibleguy.opnsense.all:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'

    ansibleguy.opnsense.list:
      target: 'monit_alert'

  tasks:
    - name: Example      
      ansibleguy.opnsense.monit_alert:
        recipient: 'monit-alert@template.ansibleguy.net'
        # not_on: false
        # events: []
        # format: ''
        # reminder: 10
        # description: 'example'
        # match_fields: ['recipient']
        # enabled: true
        # reload: true

    - name: Adding simple
      ansibleguy.opnsense.monit_alert:
        recipient: 'monit-alert@template.ansibleguy.net'

    - name: Changing
      ansibleguy.opnsense.monit_alert:
        recipient: 'monit-alert@template.ansibleguy.net'
        format: |
          From: monit-alert@template.ansibleguy.net
          Reply-To: netmaster@template.ansibleguy.net
          Subject: $SERVICE at $HOST failed
        not_on: true
        events: ['timestamp']
        description: 'alert1'
        reminder: 500

    - name: Disabling
      ansibleguy.opnsense.monit_alert:
        recipient: 'monit-alert@template.ansibleguy.net'
        format: |
          From: monit-alert@template.ansibleguy.net
          Reply-To: netmaster@template.ansibleguy.net
          Subject: $SERVICE at $HOST failed
        not_on: true
        events: ['timestamp']
        description: 'alert1'
        reminder: 500
        enabled: false

    - name: Removing
      ansibleguy.opnsense.monit_alert:
        recipient: 'monit-alert@template.ansibleguy.net'
        state: 'absent'

    - name: Listing
      ansibleguy.opnsense.list:
        # target: 'monit_alert'
      register: existing_entries

    - name: Printing alerts
      ansible.builtin.debug:
        var: existing_entries.data
```

### Tests

```yaml
- hosts: localhost
  gather_facts: no
  module_defaults:
    group/ansibleguy.opnsense.all:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'

    ansibleguy.opnsense.list:
      target: 'monit_test'

  tasks:
    - name: Example      
      ansibleguy.opnsense.monit_test:
        name: 'example'
        # type: ''
        # condition: ''
        # action: 'alert'
        # path: ''
        # enabled: true
        # reload: true

    - name: Adding memory tests
      ansibleguy.opnsense.monit_test:
        name: 'test1'
        condition: 'memory usage is greater than 90%'
        type: 'SystemResource'
        action: 'alert'

    - name: Changing
      ansibleguy.opnsense.monit_test:
        name: 'test1'
        condition: 'memory usage is greater than 90%'
        type: 'SystemResource'
        action: 'exec'
        path: '/usr/local/bin/test1.sh'

    - name: Disabling
      ansibleguy.opnsense.monit_test:
        name: 'test1'
        condition: 'memory usage is greater than 90%'
        type: 'SystemResource'
        action: 'exec'
        path: '/usr/local/bin/test1.sh'
        enabled: false

    - name: Removing
      ansibleguy.opnsense.monit_test:
        name: 'test1'
        state: 'absent'

    - name: Adding connection tests
      ansibleguy.opnsense.monit_test:
        name: 'test2'
        condition: 'failed host 127.0.0.1 port 22 protocol ssh'
        type: 'Connection'

    - name: Listing
      ansibleguy.opnsense.list:
        # target: 'monit_test'
      register: existing_entries

    - name: Printing tests
      ansible.builtin.debug:
        var: existing_entries.data
```

### Services

```yaml
- hosts: localhost
  gather_facts: no
  module_defaults:
    group/ansibleguy.opnsense.all:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'

    ansibleguy.opnsense.list:
      target: 'monit_service'

  tasks:
    - name: Example      
      ansibleguy.opnsense.monit_service:
        name: 'example'
        # type: ''
        # pidfile: ''
        # match: ''
        # path: ''
        # timeout: 300
        # address: ''
        # interface: ''
        # start: ''
        # stop: ''
        # tests: []
        # depends: []
        # polltime: ''
        # description: 'example'
        # enabled: true
        # reload: true

    - name: Adding simple
      ansibleguy.opnsense.monit_service:
        name: 'service1'
        type: 'custom'
        start: '/usr/local/bin/test1_start.sh'

    - name: Changing
      ansibleguy.opnsense.monit_service:
        name: 'service1'
        type: 'custom'
        start: '/usr/local/bin/service1_start.sh'
        stop: '/usr/local/bin/service1_stop.sh'
        tests: ['test1']

    - name: Adding another
      ansibleguy.opnsense.monit_service:
        name: 'service2'
        type: 'network'
        interface: 'opt2'
        depends: ['service1']

    - name: Disabling
      ansibleguy.opnsense.monit_service:
        name: 'service2'
        type: 'network'
        interface: 'opt2'
        depends: ['service1']
        enabled: false

    - name: Removing
      ansibleguy.opnsense.monit_service:
        name: 'service2'
        state: 'absent'

    - name: Listing
      ansibleguy.opnsense.list:
        # target: 'monit_service'
      register: existing_entries

    - name: Printing services
      ansible.builtin.debug:
        var: existing_entries.data
```

### Practical example

Mail notification on IDS alert: see [documentation](https://docs.opnsense.org/manual/monit.html#example-3)

```yaml
- hosts: localhost
  gather_facts: no
  module_defaults:
    group/ansibleguy.opnsense.all:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'

  tasks:
    - name: Adding test
      ansibleguy.opnsense.monit_test:
        name: 'SURICATA_EVE'
        condition: 'content = "blocked"'
        type: 'FileContent'
        action: 'alert'

    - name: Adding service
      ansibleguy.opnsense.monit_service:
        name: 'SURICATA_ALERT'
        type: 'file'
        path: '/var/log/suricata/eve.json'
        tests: ['SURICATA_EVE']
```
