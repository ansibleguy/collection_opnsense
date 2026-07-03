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
    (
            {'api_name': 'value'},
            {'ansible_name': 'api_name'},
            {'ansible_name': 'value', '__ansible_translated': ''},
    ),
    (
            {'api': {'name': 'value'}},
            {'ansible_name': ('api', 'name')},
            {'ansible_name': 'value', '__ansible_translated': ''},
    ),
])
def test_simplify_translate(existing, translate, simple):
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.translate import simplify_translate

    assert simple == simplify_translate(existing=existing, translate=translate, ignore=['api'])


@pytest.mark.parametrize(
    "translate_map, ignore_list, optional_list, input_data, expected",
    [
        # 1. Flat translation & pass-through of unmapped fields
        (
                {"ansible_name": "api_name"},
                [], [],
                {"api_name": "value1", "unmapped": "value2"},
                {"ansible_name": "value1", "unmapped": "value2"}
        ),
        # 2. Nested tuple translation
        (
                {"ansible_ip": ("network", "ip")},
                ["network"], [],
                {"network": {"ip": "192.168.1.1"}},
                {"ansible_ip": "192.168.1.1"}
        ),
        # 3. Ignored fields are dropped during pass-through
        (
                {"ansible_name": "api_name"},
                ["drop_me"], [],
                {"api_name": "value1", "drop_me": "secret"},
                {"ansible_name": "value1"}
        ),
        # 4. Optional fields (skips gracefully if flat key is missing)
        (
                {"ansible_opt": "api_opt"},
                [], ["ansible_opt"],
                {"other_key": "value"},
                {"other_key": "value"}
        ),
        # 5. Optional fields (skips gracefully if nested key is missing)
        (
                {"ansible_nested_opt": ("data", "missing")},
                ["data"], ["ansible_nested_opt"],
                {"data": {"present": "value"}},
                {}
        )
    ]
)
def test_translate_field_names(translate_map, ignore_list, optional_list, input_data, expected):
    """Tests the core mapping, nested extraction, ignoring, and optional omission logic."""
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.translate import SimplifyTranslate

    translator = SimplifyTranslate(
        translate=translate_map,
        ignore=ignore_list,
        optional=optional_list
    )
    result = translator._translate_field_names_api_to_ansible(input_data)
    assert result == expected


@pytest.mark.parametrize(
    "bool_invert, input_data, expected",
    [
        # 1. Auto string-to-int conversion (bottom of _ensure_field_value_typing)
        (
                [],
                {"port": "8080", "name": "server1"},
                {"port": 8080, "name": "server1"}
        ),
        # 2. Boolean inversion
        (
                ["is_disabled"],
                {"is_disabled": False, "is_active": True},
                {"is_disabled": True, "is_active": True}
        ),
    ]
)
def test_typing_builtins(bool_invert, input_data, expected):
    """Tests the native python type conversions (numeric strings & bool inversion)."""
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.translate import SimplifyTranslate

    translator = SimplifyTranslate(bool_invert=bool_invert)

    data = input_data.copy()
    translator._ensure_field_value_typing(data)

    assert data == expected


@pytest.mark.parametrize(
    "value_map, input_data, expected",
    [
        # 1. Matches map and translates successfully
        (
                {"state": {"enabled": "1", "disabled": "0"}},
                {"state": "0", "unrelated": "val"},
                {"state": "disabled", "unrelated": "val"}
        ),
        # 2. Doesn't match map, leaves value as is
        (
                {"state": {"enabled": "1"}},
                {"state": "unknown"},
                {"state": "unknown"}
        )
    ]
)
def test_apply_field_value_mapping(value_map, input_data, expected):
    """Tests the reversal/mapping of API specific values to Ansible friendly values."""
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.translate import SimplifyTranslate

    translator = SimplifyTranslate(value_map=value_map)
    data = input_data.copy()
    translator._apply_field_value_mapping(data)
    assert data == expected


def test_ensure_field_value_typing_external_helpers(mocker):
    """Tests that external helper functions are called correctly based on typing map."""
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.translate import SimplifyTranslate

    mock_is_true = mocker.patch(
        'ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.translate.is_true',
        return_value=True,
    )
    mock_format_int = mocker.patch(
        'ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.translate.format_int',
        return_value=443,
    )

    translator = SimplifyTranslate(
        typing={
            "bool": ["active_flag"],
            "int": ["port_number"]
        }
    )

    data = {"active_flag": "yes", "port_number": "443_str"}
    translator._ensure_field_value_typing(data)

    mock_is_true.assert_called_once_with("yes")
    mock_format_int.assert_called_once_with("443_str")

    assert data["active_flag"] is True
    assert data["port_number"] == 443


def test_translate_orchestrator_error_handling(mocker):
    """Tests that the main translate() method catches exceptions and calls exit_bug."""
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.translate import SimplifyTranslate

    mock_exit_bug = mocker.patch('ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.translate.exit_bug')

    translator = SimplifyTranslate(
        translate={"ansible_bad": ("missing", "path")}
    )

    result = translator.translate({"unrelated": "data"})

    assert result == {}
    mock_exit_bug.assert_called_once()

    call_arg = mock_exit_bug.call_args[0][0]
    assert "Failed to translate API entry" in call_arg
