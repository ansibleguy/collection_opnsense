from ansible.module_utils.basic import AnsibleModule


def purge(module: AnsibleModule, result: dict, item_to_purge: dict, diff_param: str, obj_func):
    result['changed'] = True

    if module.params['action'] == 'delete':
        result['diff']['before'][item_to_purge[diff_param]] = item_to_purge
        result['diff']['after'][item_to_purge[diff_param]] = None

    else:
        result['diff']['before'][item_to_purge[diff_param]] = {'enabled': True}
        result['diff']['after'][item_to_purge[diff_param]] = {'enabled': False}

    if not module.check_mode:
        _obj = obj_func(item_to_purge)

        if module.params['action'] == 'delete':
            _obj.delete()

        else:
            _obj.disable()


def check_purge_filter(module: AnsibleModule, item: dict) -> bool:
    to_purge = True

    for filter_key, filter_value in module.params['filters'].items():
        if module.params['filter_invert']:
            # purge all except matches
            if module.params['filter_partial']:
                if str(item[filter_key]).find(filter_value) != -1:
                    to_purge = False
                    break

            else:
                if item[filter_key] == filter_value:
                    to_purge = False
                    break

        else:
            # purge only matches
            if module.params['filter_partial']:
                if str(item[filter_key]).find(filter_value) == -1:
                    to_purge = False
                    break

            else:
                if item[filter_key] != filter_value:
                    to_purge = False
                    break

    return to_purge
