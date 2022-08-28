# OPNSense - System module

**STATE**: testing

**TESTS**: [Playbook](https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/system.yml)

**API DOCS**: [Core - Firmware](https://docs.opnsense.org/development/api/core/firmware.html)

## Usage

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
