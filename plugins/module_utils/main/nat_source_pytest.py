import pytest

from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.nat_source import SNat
from ansible_collections.oxlorg.opnsense.plugins.module_utils.test.mock_pytest import \
    AnsibleError, MockAnsibleModule


BASE_PARAMS = {
    'state': 'present',
    'enabled': True,
    'sequence': 1,
    'no_nat': False,
    'interface': '',
    'target': '',
    'target_port': '',
    'description': 'ANSIBLE_TEST_SNAT',
    'ip_protocol': 'inet',
    'protocol': '',
    'source_invert': False,
    'source_net': 'any',
    'source_port': '',
    'destination_invert': False,
    'destination_net': '192.168.0.1',
    'destination_port': '',
    'log': False,
    'static_port': False,
    'match_fields': ['uuid'],
}


def _build_snat(mocker, exists: bool) -> SNat:
    module = MockAnsibleModule()
    module.params.update(BASE_PARAMS)
    result = {'changed': False, 'diff': {'before': {}, 'after': {}}}
    snat = SNat(module=module, result=result)

    mocker.patch.object(snat, 'find', side_effect=lambda **kwargs: setattr(snat, 'exists', exists))
    mocker.patch.object(snat, '_base_check')

    return snat


def test_check_requires_target_and_interface_when_creating(mocker):
    snat = _build_snat(mocker, exists=False)

    with pytest.raises(AnsibleError):
        snat.check()


def test_check_allows_empty_target_on_existing_rule(mocker):
    # simulates adopting an already-existing rule (e.g. match_fields: [uuid]) that has
    # an empty target - a valid state meaning "use the interface's own address"
    snat = _build_snat(mocker, exists=True)

    snat.check()
