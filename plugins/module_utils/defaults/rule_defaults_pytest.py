def test_categories_is_exposed():
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.defaults.rule import \
        RULE_MOD_ARGS

    assert 'categories' in RULE_MOD_ARGS
    assert RULE_MOD_ARGS['categories']['type'] == 'list'
