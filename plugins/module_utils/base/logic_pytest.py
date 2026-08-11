from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.logic import BaseLogic
from ansible_collections.oxlorg.opnsense.plugins.module_utils.test.mock_pytest import \
    MockAnsibleModule


class DummySearchLogic(BaseLogic):
    CMDS = {
        'search': 'search_rule',
        'detail': 'get_rule',
    }
    API_KEY_PATH = 'rule'
    API_MOD = 'firewall'
    API_CONT = 'source_nat'
    FIELDS_ALL = []
    FIELDS_CHANGE = []
    FIELDS_TYPING = {}

    def check(self) -> None:
        return


def test_search_skips_detail_lookup_for_automatic_entries(mocker):
    module = MockAnsibleModule()
    module.params.update({
        'description': 'automatic_isakmp_wan',
    })
    result = {'changed': False, 'diff': {'before': {}, 'after': {}}}
    logic = DummySearchLogic(module, result)

    automatic_entry = {
        'uuid': 'auto-rule-1',
        'description': 'automatic_isakmp_wan',
        'is_automatic': True,
    }

    mocker.patch.object(logic, 'api_search_post', return_value=[automatic_entry])
    api_get = mocker.patch.object(logic, '_api_get')

    entries = logic.search(match_fields=['description'])

    assert entries == [automatic_entry]
    assert logic.raw == automatic_entry
    api_get.assert_not_called()
