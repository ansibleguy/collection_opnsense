---
name: Support
about: You have general problems using the collection
title: '[Support] - Issue Title'
labels: support
assignees: ''

---

## Tasks

Please make sure to go through these steps before opening an issue:

- [ ] Read the documentation of the affected module: [Docs](https://github.com/ansibleguy/collection_opnsense/tree/latest/docs)

- [ ] Read the troubleshooting info: [Info](https://github.com/ansibleguy/collection_opnsense#errors)

## Basic info

- [ ] Affected Module: 

### Versions
* Controller
  - [ ] Collection version: 

     (```ansible-galaxy collection list | grep opnsense```)

  - [ ] Ansible & Python version:

    (```ansible --version```)


* OPNSense

  - [ ] System version: 

  - [ ] Plugin version:

    (_if applicable_) 

### Describe the bug

A clear and concise description of what the bug is.

### Expected behavior

A clear and concise description of what you expected to happen.

### Debug output

Set the [debug option](https://github.com/ansibleguy/collection_opnsense/blob/latest/docs/develop.md#debugging) and copy its output.

```text
placeholder
```

If the issue is related to time-consumption, you may also add the content of the [profiling logs](https://github.com/ansibleguy/collection_opnsense/blob/latest/docs/develop.md#debugging).

```text
placeholder
```

### Screenshots

If applicable, add screenshots to help explain your problem.

### Additional context

Add any other context about the problem here.

## Reproduce
### Tasks
Task(s) that produce the error:

```yaml
- name: placeholder
```

### Config
Config used for the task(s):

```yaml
- name: placeholder
```

### OPNSense config
(_If the issue only occurs when non ansible-managed config is modified_)
