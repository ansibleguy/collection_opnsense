from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    ModuleSoftError
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    simplify_translate, validate_int_fields
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.rule import \
    validate_values
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.base import Base


class Rule:
    CMDS = {
        'add': 'addRule',
        'del': 'delRule',
        'set': 'setRule',
        'search': 'get',
        'toggle': 'toggleRule',
    }
    API_KEY = 'rule'
    API_KEY_1 = 'filter'
    API_KEY_2 = 'rules'
    API_MOD = 'firewall'
    API_CONT = 'filter'
    FIELDS_CHANGE = [
        'sequence', 'action', 'quick', 'interface', 'direction',
        'ip_protocol', 'protocol', 'source_invert', 'source_net', 'source_port',
        'destination_invert', 'destination_net', 'destination_port', 'log',
        'description',
    ]
    FIELDS_ALL = ['enabled']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'ip_protocol': 'ipprotocol',
        'source_invert': 'source_not',
        'destination_invert': 'destination_not',
    }
    FIELDS_TYPING = {
        'bool': ['enabled', 'log', 'quick', 'source_invert', 'destination_invert'],
        'select': ['action', 'direction', 'ip_protocol', 'protocol', 'gateway'],
        'list': ['interface'],
    }
    EXIST_ATTR = 'rule'
    TIMEOUT = 60.0  # urltable etc reload
    INT_VALIDATIONS = {
        'sequence': {'min': 1, 'max': 99999},
    }

    def __init__(
            self, module: AnsibleModule, result: dict, cnf: dict = None,
            session: Session = None, fail_verify: bool = True, fail_proc: bool = True
    ):
        self.m = module
        self.r = result
        self.s = Session(
            module=module,
            timeout=self.TIMEOUT,
        ) if session is None else session
        self.p = self.m.params if cnf is None else cnf  # to allow override by rule_multi
        self.fail_verify = fail_verify
        self.fail_proc = fail_proc
        self.exists = False
        self.rule = {}
        self.log_name = None
        self.call_cnf = {  # config shared by all calls
            'module': self.API_MOD,
            'controller': self.API_CONT,
        }
        self.existing_entries = None
        self.b = Base(instance=self)

    def simplify_existing(self, rule: dict):
        # makes processing easier
        return simplify_translate(
            existing=rule,
            typing=self.FIELDS_TYPING,
            translate=self.FIELDS_TRANSLATE,
        )

    def _build_log_name(self) -> str:
        if self.p['description'] not in [None, '']:
            log_name = self.p['description']

        else:
            log_name = f"{self.p['action'].upper()}: FROM "

            if self.p['source_invert']:
                log_name += 'NOT '

            log_name += f"{self.p['source_net']} <= PROTO {self.p['protocol']} => "

            if self.p['destination_invert']:
                log_name += 'NOT '

            log_name += f"{self.p['destination_net']}:{self.p['destination_port']}"

        return log_name

    def check(self):
        validate_int_fields(
            module=self.m,
            data=self.p,
            field_minmax=self.INT_VALIDATIONS,
            error_func=self._error
        )
        self._build_log_name()

        self.b.find(match_fields=self.p['match_fields'])
        if self.exists:
            self.call_cnf['params'] = [self.rule['uuid']]

        if self.p['state'] == 'present':
            validate_values(
                error_func=self._error,
                module=self.m,
                cnf=self.p
            )
            self.r['diff']['after'] = self.b.build_diff(data=self.p)

    def _error(self, msg: str, verification: bool = True):
        if (verification and self.fail_verify) or (not verification and self.fail_proc):
            self.m.fail_json(msg)

        else:
            self.m.warn(msg)
            raise ModuleSoftError

    def process(self):
        self.b.process()

    def search_call(self) -> (dict, list):
        return self.b.search()

    def create(self):
        self.b.create()

    def update(self):
        self.b.update()

    def delete(self):
        self.b.delete()

    def get_existing(self) -> list:
        return self.b.get_existing()
