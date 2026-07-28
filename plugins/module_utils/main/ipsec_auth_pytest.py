import pytest


from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule
from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.ipsec_auth import BaseAuth


@pytest.fixture
def auth(mocker):
    mocker.patch.object(BaseModule, '__init__', return_value=None)
    instance = BaseAuth(m=None, r={}, s=None, f=None)
    instance.m = mocker.Mock()
    instance.m.fail_json.side_effect = AssertionError
    instance.p = {
        'state': 'present',
        'connection': 'TEST_CONN',
        'authentication': 'psk',
        'certificates': None,
        'public_keys': None,
        'eap_id': None,
    }
    instance.existing_entries = None
    instance.existing_conns = {'dummy': {'description': 'TEST_CONN'}}
    return instance


def test_check_resolves_connection_before_matching(mocker, auth):
    calls = []

    mocker.patch.object(auth, '_call_search', side_effect=lambda: calls.append('_call_search') or {})
    mocker.patch.object(
        auth,
        'find_single_link',
        side_effect=lambda **kwargs: calls.append('find_single_link'),
    )
    mocker.patch.object(auth, '_base_check', side_effect=lambda: calls.append('_base_check'))

    auth.check()

    assert calls == ['_call_search', 'find_single_link', '_base_check']
