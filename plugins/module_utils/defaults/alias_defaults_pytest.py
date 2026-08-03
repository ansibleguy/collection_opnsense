def test_categories_is_exposed():
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.defaults.alias import ALIAS_MOD_ARGS

    assert 'categories' in ALIAS_MOD_ARGS
    assert ALIAS_MOD_ARGS['categories']['type'] == 'list'
