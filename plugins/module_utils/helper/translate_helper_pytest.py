import pytest

def test_get_selected():
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.translate import get_selected


def test_get_selected_value():
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.translate import get_selected_value


def test_get_selected_opt_list():
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.translate import get_selected_opt_list


def test_get_selected_opt_list_idx():
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.translate import get_selected_opt_list_idx


def test_get_selected_multi():
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.translate import get_selected_multi


def test_get_selected_list():
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.translate import get_selected_list


def test_get_key_by_value_from_selection():
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.translate import \
        get_key_by_value_from_selection


def test_get_key_by_value_end_from_selection():
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.translate import \
        get_key_by_value_end_from_selection


def test_get_key_by_value_beg_from_selection():
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.translate import \
        get_key_by_value_beg_from_selection


def test_get_simple_existing():
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.translate import \
        get_key_by_value_beg_from_selection


# todo: add more tests for simplify_translate and other essential functions to catch regressions

@pytest.mark.parametrize('existing, translate, simple', [
    ({'api_name': 'value'}, {'ansible_name': 'api_name'}, {'ansible_name': 'value'}),
    ({'api': {'name': 'value'}}, {'ansible_name': ('api', 'name')}, {'ansible_name': 'value'}),
])
def test_simplify_translate(existing, translate, simple):
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.translate import simplify_translate

    assert simple == simplify_translate(existing=existing, translate=translate, ignore=['api'])

