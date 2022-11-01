---
name: Bug report
about: Create a report to help us improve
title: '[Module] - Issue Title'
labels: bug
assignees: ''

---

## Tasks

Please make sure to go through these steps before opening an issue:

- [ ] Read the documentation of the affected module: [Docs](https://github.com/ansibleguy/collection_opnsense/tree/stable/docs)

- [ ] Read the troubleshooting info: [Info](https://github.com/ansibleguy/collection_opnsense#errors)

## Basic info

- [ ] Affected Module: 

### Versions
* Controller
  - [ ] Collection version: 

     (```ansible-galaxy collection list | grep opnsense```)

  - [ ] Ansible version:

    (```python3 -m pip list | grep ansible``` or ```apt policy ansible```)

  - [ ] Python version:


* OPNSense

  - [ ] System version: 

  - [ ] Plugin version:

    (_if applicable_) 

### Describe the bug

A clear and concise description of what the bug is.

### Expected behavior

A clear and concise description of what you expected to happen.

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
