# Development

The basic API interaction is handled in 'ansibleguy.opnsense.plugins.module_utils.api'.

It is a generic abstraction layer for interacting with the api - therefore all plugins should be able to function with it!

## API Definition

To get to know the API - you will have to read into the API's XML-config that is linked in [the OPNSense docs](https://docs.opnsense.org/development/api.html#introduction).

Per example: [Alias.xml](https://github.com/opnsense/core/blob/master/src/opnsense/mvc/app/models/OPNsense/Firewall/Alias.xml)

As XML isn't the most readable format - I would recommend translating it to YAML or JSON.

Here is a nice online-tool to do so: [XML-to-YAML](https://codebeautify.org/xml-to-yaml) | [XML-to-JSON](https://codebeautify.org/xml-to-json)


## Module

There is a [module-template](https://github.com/ansibleguy/collection_opnsense/blob/stable/plugins/modules/_tmpl.py) that can be copied - so you don't have to re-write the basic structure.

## API

One can choose to either:

- create a http-session - faster if multiple calls are needed

  p.e. _check current state => create/update/delete_

  ```python3
  from ansible_collections.ansibleguy.opnsense.plugins.module_utils.api import Session
  session = Session(module=module)
  session.get(cnf={'controller': 'alias', 'command': 'addItem', 'data': {'name': 'dummy', ...}})
  session.post(cnf={'controller': 'alias', 'command': 'delItem', 'params': [uuid]})
  session.close()
  ```

- use a single call - if only one is needed

  p.e. toggle a cronjob or restart a service

  ```python3
  from ansible_collections.ansibleguy.opnsense.plugins.module_utils.api import single_get, single_post
  single_get(
      module=module, 
      cnf={'controller': 'alias', 'command': 'addItem', 'data': {'name': 'dummy', ...}}
  )
  single_post(
      module=module, 
      cnf={'controller': 'alias', 'command': 'delItem', 'params': [uuid]}
  )
  ```

For the controller/command/params/data definition - check the [OPNSense API Docs](https://docs.opnsense.org/development/api.html#core-api)!


## Debugging

### Verbose output
If you want to output something to ansible's runtime - use 'module.warn':

```python3
module.warn(f"{before} != {after}")
```

You can also use the 'debug' argument to enable verbose output of the api requests. 

```yaml
- name: Example
  ansibleguy.opnsense.alias:
    debug: true
```

'Multi' modules also support the 'debug' parameter on a per-item basis - so you don't get flooded.
