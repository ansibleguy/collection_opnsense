import pytest


from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.main import to_digit, is_unset
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.logic import BaseLogic


@pytest.fixture
def logic(mocker):
    """
    Provides a pristine instance of the actual BaseLogic class.
    We patch __init__ to return None so we don't have to construct
    complex AnsibleModule mock objects just to test data parsing logic.
    """
    mocker.patch.object(BaseLogic, '__init__', return_value=None)
    instance = BaseLogic()

    instance.FIELDS_ALL = []
    instance.p = {}
    instance.e = None

    instance.EXIST_ATTR = "default_e"
    instance.default_e = {"fallback": "data"}
    instance.RESP_JOIN_CHAR = ","
    instance.ATTR_AK_PATH_SPLIT_CHAR = "."

    instance.ATTR_TRANSLATE = "_translate"
    instance.ATTR_VALUE_MAP = "_value_map"
    instance.ATTR_BOOL_INVERT = "_bool_invert"
    instance.ATTR_JOIN_CHAR = "_join_char"
    instance.ATTR_AK_PATH_REQ = "_ak_path_req"
    instance.ATTR_AK_PATH = "_ak_path"

    return instance


# --- Unit Tests ---

@pytest.mark.parametrize(
    "field, p_data, e_data, expected",
    [
        ("username", {"username": "admin_p"}, {"username": "admin_e"}, "admin_p"),
        ("username", {}, {"username": "admin_e"}, "admin_e"),
        ("username", {}, {}, ""),
        ("username", {"username": None}, {"username": "admin_e"}, None),
    ]
)
def test_extract_raw_data(logic, field, p_data, e_data, expected):
    logic.p = p_data
    logic.e = e_data
    result = logic._build_request_extract_raw_data(field)
    assert result == expected


@pytest.mark.parametrize(
    "field, opn_data, value_map, bool_invert, join_char, expected",
    [
        ("status", "active", {"status": {"active": 1, "inactive": 0}}, [], None, 1),
        ("status", "unknown", {"status": {"active": 1}}, [], None, "unknown"),
        ("is_admin", True, {}, [], None, 1),
        ("is_admin", True, {}, ["is_admin"], None, 0),
        ("roles", ["admin", "user"], {}, [], None, "admin,user"),
        ("roles", ["admin", "user"], {}, [], "|", "admin|user"),
        ("optional_field", None, {}, [], None, ""),
        ("name", "John", {}, [], None, "John"),
    ]
)
def test_format_data(logic, field, opn_data, value_map, bool_invert, join_char, expected):
    setattr(logic, logic.ATTR_VALUE_MAP, value_map)
    setattr(logic, logic.ATTR_BOOL_INVERT, bool_invert)
    if join_char is not None:
        setattr(logic, logic.ATTR_JOIN_CHAR, join_char)

    result = logic._build_request_format_data(field, opn_data)
    assert result == expected


@pytest.mark.parametrize(
    "initial_req, opn_field, value, expected_req",
    [
        ({}, "username", "admin", {"username": "admin"}),
        ({}, ("user", "profile", "name"), "John", {"user": {"profile": {"name": "John"}}}),
        ({"user": {"id": 1}}, ("user", "profile", "name"), "John", {"user": {"id": 1, "profile": {"name": "John"}}}),
        ({}, ["primary_key", "secondary_key"], "123", {"primary_key": "123"}),
        ({}, (), "val", {(): "val"}),
    ]
)
def test_handle_field_name_translation(opn_field, value, expected_req, initial_req):
    BaseLogic._build_request_handle_field_name_translation(initial_req, opn_field, value)
    assert initial_req == expected_req


@pytest.mark.parametrize(
    "ak_path_req, ak_path, payload, expected",
    [
        ("api.v1.users", None, {"id": 1}, {"api": {"v1": {"users": {"id": 1}}}}),
        (None, "namespace.module.CreateUser", {"id": 1}, {"CreateUser": {"id": 1}}),
        (None, "UpdateUser", {"id": 1}, {"UpdateUser": {"id": 1}}),
        (None, None, {"id": 1}, {"id": 1}),
    ]
)
def test_wrap_payload(logic, ak_path_req, ak_path, payload, expected):
    if ak_path_req:
        setattr(logic, logic.ATTR_AK_PATH_REQ, ak_path_req)
    if ak_path:
        setattr(logic, logic.ATTR_AK_PATH, ak_path)

    result = logic._build_request_wrap_payload(payload)
    assert result == expected


def test_base_build_request_orchestration(mocker, logic):
    logic.FIELDS_ALL = ["field1", "field2", "field3"]
    setattr(logic, logic.ATTR_TRANSLATE, {"field1": "mapped_field1"})
    logic.e = None  # To trigger the is_unset fallback logic
    ignore_fields = ["field3"]

    mock_extract = mocker.patch.object(
        logic, '_build_request_extract_raw_data', side_effect=["raw1", "raw2"]
    )
    mock_format = mocker.patch.object(
        logic, '_build_request_format_data', side_effect=["fmt1", "fmt2"]
    )
    mock_assign = mocker.patch.object(
        BaseLogic, '_build_request_handle_field_name_translation'  # Note: patch staticmethod on Class
    )
    mock_wrap = mocker.patch.object(
        logic, '_build_request_wrap_payload', return_value={"final": "payload"}
    )

    result = logic._base_build_request(ignore_fields)
    assert logic.e == logic.default_e

    assert mock_extract.call_args_list == [
        mocker.call("field1"),
        mocker.call("field2")
    ]

    assert mock_format.call_args_list == [
        mocker.call("field1", "raw1"),
        mocker.call("field2", "raw2")
    ]

    assert mock_assign.call_count == 2

    args_call_1 = mock_assign.call_args_list[0][0]
    args_call_2 = mock_assign.call_args_list[1][0]

    assert args_call_1[1:] == ("mapped_field1", "fmt1")
    assert args_call_2[1:] == ("field2", "fmt2")

    mock_wrap.assert_called_once()
    assert result == {"final": "payload"}
