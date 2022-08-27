from ansible_collections.ansibleguy.opnsense.plugins.module_utils.alias_obj import Alias


def process_alias(alias: Alias):
    if alias.cnf['state'] == 'absent':
        if alias.exists:
            alias.delete()

    else:
        if alias.cnf['content'] is not None and len(alias.cnf['content']) > 0:
            if alias.exists:
                alias.update()

            else:
                alias.create()

        if alias.exists:
            if alias.cnf['enabled']:
                alias.enable()

            else:
                alias.disable()
