from types import SimpleNamespace

from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.alias import Alias
from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.rule import Rule
from ansible_collections.oxlorg.opnsense.plugins.modules.alias_multi import \
    MultiCallbacks as AliasMultiCallbacks
from ansible_collections.oxlorg.opnsense.plugins.modules.rule_multi import \
    MultiCallbacks as RuleMultiCallbacks


def test_alias_build_request_uses_cached_category_selection():
    alias = Alias.__new__(Alias)
    alias.p = {'categories': ['Ops', 'VPN']}
    alias.r = {'diff': {'before': {}, 'after': {}}}
    alias.RESP_JOIN_CHAR = ','
    alias.existing_categories = {
        'uuid-ops': {'value': 'Ops'},
        'uuid-vpn': {'value': 'VPN'},
    }
    alias._base_build_request = lambda: {'alias': {}}

    def fake_find_multiple_links(field, existing, existing_field_id, **_kwargs):
        assert field == 'categories'
        assert existing == alias.existing_categories
        assert existing_field_id == 'value'
        alias.p[field] = ['uuid-ops', 'uuid-vpn']
        return True

    alias.find_multiple_links = fake_find_multiple_links

    request = alias.build_request()

    assert request == {'alias': {'categories': 'uuid-ops,uuid-vpn'}}
    assert alias.p['categories'] == ['Ops', 'VPN']


def test_rule_build_request_uses_cached_category_selection():
    rule = Rule.__new__(Rule)
    rule.p = {'categories': ['Allow', 'Critical']}
    rule.r = {'diff': {'before': {}, 'after': {}}}
    rule.RESP_JOIN_CHAR = ','
    rule.existing_categories = {
        'uuid-allow': {'value': 'Allow'},
        'uuid-critical': {'value': 'Critical'},
    }
    rule._base_build_request = lambda: {'rule': {}}

    def fake_find_multiple_links(field, existing, existing_field_id, **_kwargs):
        assert field == 'categories'
        assert existing == rule.existing_categories
        assert existing_field_id == 'value'
        rule.p[field] = ['uuid-allow', 'uuid-critical']
        return True

    rule.find_multiple_links = fake_find_multiple_links

    request = rule.build_request()

    assert request == {'rule': {'categories': 'uuid-allow,uuid-critical'}}
    assert rule.p['categories'] == ['Allow', 'Critical']


def test_alias_multi_callbacks_cache_categories():
    meta_entry = SimpleNamespace(
        search=lambda: {
            'uuid-a': {'name': 'custom_alias', 'categories': {'cat-1': {'value': 'Ops'}}},
            'uuid-b': {'name': 'bogons', 'categories': {'cat-2': {'value': 'Builtin'}}},
        },
        simplify_existing=lambda entry: entry,
        _get_category_selection=lambda: {'cat-1': {'value': 'Ops'}},
    )

    cache = AliasMultiCallbacks.get_existing(meta_entry)
    entry = SimpleNamespace(existing_entries=None, existing_categories=None)
    AliasMultiCallbacks.set_existing(entry, cache)

    assert cache['main'] == [{'name': 'custom_alias', 'categories': {'cat-1': {'value': 'Ops'}}, 'uuid': 'uuid-a'}]
    assert cache['categories'] == {'cat-1': {'value': 'Ops'}}
    assert entry.existing_entries == cache['main']
    assert entry.existing_categories == cache['categories']


def test_rule_multi_callbacks_cache_categories():
    meta_entry = SimpleNamespace(
        p={'match_fields': ['description']},
        search=lambda match_fields: {
            'uuid-r1': {'description': 'Allow VPN', 'categories': {'cat-1': {'value': 'VPN'}}},
        },
        simplify_existing=lambda entry: entry,
        _get_category_selection=lambda: {'cat-1': {'value': 'VPN'}},
    )

    cache = RuleMultiCallbacks.get_existing(meta_entry)
    entry = SimpleNamespace(existing_entries=None, existing_categories=None)
    RuleMultiCallbacks.set_existing(entry, cache)

    assert cache['main'] == [{'description': 'Allow VPN', 'categories': {'cat-1': {'value': 'VPN'}}, 'uuid': 'uuid-r1'}]
    assert cache['categories'] == {'cat-1': {'value': 'VPN'}}
    assert entry.existing_entries == cache['main']
    assert entry.existing_categories == cache['categories']
