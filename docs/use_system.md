# OPNSense - System module

**STATE**: testing

**TESTS**: [Playbook](https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/system.yml)

**API DOCS**: [Core - Firmware](https://docs.opnsense.org/development/api/core/firmware.html)

## Definition

| Parameter  | Type    | Required | Default value | Comment                                                                                  |
|:-----------|:--------|:---------|:--------------|:-----------------------------------------------------------------------------------------|
| action     | string  | true     | -             | Action to execute. One of: 'poweroff', 'reboot', 'update', 'upgrade', 'audit'            |
| wait   | boolean | false    | true          | If the module should wait for the action to finish. Available for 'upgrade' and 'reboot' |
| timeout | int     | false    | 90            | Seconds to wait for the action to finish - if 'wait' is enabled                          |
| poll_interval | int  | false    | 2             | Interval in which to check if the firewall is online                                     |

For basic parameters see: [Basics](https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_basic.md#definition)


## Examples

```yaml
- hosts: localhost
  gather_facts: no
  module_defaults:
    ansibleguy.opnsense.system:
      firewall: 'opnsense.template.ansibleguy.net'
      api_credential_file: '/home/guy/.secret/opn.key'

  tasks:
    - name: Reboot the box - will wait until finished
      ansibleguy.opnsense.system:
        action: 'reboot'

    - name: Reboot the box - don't wait
      ansibleguy.opnsense.system:
        action: 'reboot'
        wait: false

    - name: Shutdown the box
      ansibleguy.opnsense.system:
        action: 'poweroff'

    - name: Pull updates
      ansibleguy.opnsense.system:
        action: 'update'

    - name: Start upgrade - will wait until finished
      ansibleguy.opnsense.system:
        action: 'upgrade'
        timeout: 120  # depends on your download speed and firmware-version

    - name: Run audit
      ansibleguy.opnsense.system:
        action: 'audit'
```
