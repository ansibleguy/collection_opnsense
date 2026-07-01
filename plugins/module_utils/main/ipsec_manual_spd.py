from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.validate import \
    is_unset, MATCH_UUID


class ManualSPD(BaseModule):
    FIELD_ID = 'name'
    CMDS = {
        'add': 'add',
        'del': 'del',
        'set': 'set',
        'search': 'search',
        'detail': 'get',
        'toggle': 'toggle',
    }
    API_KEY_PATH = 'spd'
    API_MOD = 'ipsec'
    API_CONT = 'manual_spd'
    API_CONT_REL = 'service'
    FIELDS_CHANGE = ['request_id', 'connection_child', 'source', 'destination', 'name']
    FIELDS_ALL = ['enabled']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'name': 'description',
        'request_id': 'reqid',
    }
    FIELDS_TYPING = {
        'bool': ['enabled'],
        'list': [],
        'select': ['connection_child'],
        'int': ['request_id'],
    }
    INT_VALIDATIONS = {
        'request_id': {'min': 1, 'max': 65535},
    }
    EXIST_ATTR = 'spd'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None, fail: dict = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session, f=fail)
        self.spd = {}

    def check(self) -> None:
        self._base_check()

        if self.p['state'] == 'present' and not is_unset(self.p['connection_child']):
            self.find_single_link(
                field='connection_child',
                existing=self._search_connection_child(),
                existing_field_id='value',
            )

    def _search_connection_child(self) -> dict:
        res = self.s.get(cnf={
            **self.call_cnf, **{'command': self.CMDS['detail']}
        })['spd']['connection_child']

        # temporary workaround for API-bug: https://github.com/opnsense/core/issues/9224 & 9365
        tmp_fix = False
        for values in res.values():
            if 'value' not in values:
                continue

            if values['value'].startswith(' -'):
                tmp_fix = True
                break

            if values['value'].find(' - ') != -1:
                connection, child = values['value'].split(' - ', 1)
                if MATCH_UUID.match(connection.strip()) is not None:
                    tmp_fix = True
                    values['value'] = f" - {child.strip()}"

        if tmp_fix:
            if '-' in self.p['connection_child']:
                self.p['connection_child'] = self.p['connection_child'].split('-')[1]

            self.p['connection_child'] = f" - {self.p['connection_child'].strip()}"

        return res
