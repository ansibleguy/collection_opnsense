from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    is_true, get_selected_list, get_selected
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.rule import \
    validate_values, get_state_change, get_config_change
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
        'enabled', 'sequence', 'action', 'quick', 'interface', 'direction',
        'ip_protocol', 'protocol', 'source_invert', 'source_net', 'source_port',
        'destination_invert', 'destination_net', 'destination_port', 'log',
        'description',
    ]
    FIELDS_ALL = FIELDS_CHANGE
    FIELDS_TRANSLATE = {
        'ip_protocol': 'ipprotocol',
        'source_invert': 'source_not',
        'destination_invert': 'destination_not',
    }
    EXIST_ATTR = 'rule'
    TIMEOUT = 60.0  # urltable etc reload

    def __init__(
            self, module: AnsibleModule, result: dict, cnf: dict = None,
            session: Session = None, fail: bool = True
    ):
        self.m = module
        self.r = result
        self.s = Session(
            module=module,
            timeout=self.TIMEOUT,
        ) if session is None else session
        self.p = self.m.params if cnf is None else cnf  # to allow override by rule_multi
        self.fail = fail
        self.exists = False
        self.rule = {}
        self.log_name = None
        self.call_cnf = {  # config shared by all calls
            'module': self.API_MOD,
            'controller': self.API_CONT,
        }
        self.existing_entries = None
        self.b = Base(instance=self)

    def process(self):
        if self.p['state'] == 'absent':
            if self.exists:
                self.delete()

        else:
            if self.exists:
                config_changed, state_changed = self._changed()
                if config_changed:
                    self.update()

                elif state_changed:
                    if self.p['enabled']:
                        self.enable()

                    else:
                        self.disable()

            else:
                self.create()

    @staticmethod
    def simplify_existing(rule):
        # because the return of api/firewall/filter/get is too verbose for easy access
        simple = {
            'uuid': rule['uuid'],
            'enabled': is_true(rule['enabled']),
            'log': is_true(rule['log']),
            'quick': is_true(rule['quick']),
            'source_invert': is_true(rule['source_not']),
            'destination_invert': is_true(rule['destination_not']),
            'action': get_selected(data=rule['action']),
            'interface': get_selected_list(data=rule['interface']),
            'direction': get_selected(data=rule['direction']),
            'ip_protocol': get_selected(data=rule['ipprotocol']),
            'protocol': get_selected(data=rule['protocol']),
            'gateway': get_selected(data=rule['gateway']),
        }

        for field in [
            'sequence', 'source_net', 'source_not', 'source_port', 'destination_net',
            'destination_not', 'destination_port', 'description'
        ]:
            simple[field] = rule[field]

        return simple

    def create(self):
        self.r['changed'] = True
        self.r['diff']['after'] = self.b.build_diff(data=self.p)
        if not self.m.check_mode:
            self.s.post(cnf={
                **self.call_cnf, **{
                    'command': self.CMDS['add'],
                    'data': self.b.build_request()
                }
            })

    def _changed(self) -> tuple:
        self.r['diff']['after'] = self.b.build_diff(data=self.p)

        config_changed = get_config_change(
            before=self.r['diff']['before'],
            after=self.r['diff']['after'],
        )
        state_changed = get_state_change(
            before=self.r['diff']['before'],
            after=self.r['diff']['after'],
        )
        self.r['changed'] = any([config_changed, state_changed])

        if self.m.params['debug'] and self.r['changed']:
            self.m.warn(f"{self.r['diff']} {config_changed} {state_changed}")

        return config_changed, state_changed

    def delete(self):
        self.r['changed'] = True
        if not self.m.check_mode:
            # NOTE: there is currently no practical way to check if the rule is in use..
            rule_deletion = self._delete_call()

            if 'status' in rule_deletion and rule_deletion['status'] == 'failed':
                self.r['changed'] = False
                self.m.warn(f"Unable to delete rule '{self.log_name}' as it is currently referenced!")

        if self.r['changed']:
            self.r['diff']['before'] = self.b.build_diff(data=self.rule)

            if self.m.params['debug']:
                self.m.warn(f"{self.r['diff']}")

    def _delete_call(self) -> dict:
        return self.s.post(cnf={
            **self.call_cnf, **{'command': self.CMDS['del']}
        })

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
        self._build_log_name()
        self.b.find(match_fields=self.p['match_fields'])

        if self.p['state'] == 'present':
            validate_values(error_func=self._error, module=self.m, cnf=self.p)

    def _error(self, msg: str):
        if self.fail:
            self.m.fail_json(msg)

        else:
            self.m.warn(msg)

    def search_call(self) -> (dict, list):
        return self.b.search()

    def update(self):
        self.b.update()

    def enable(self):
        self.b.enable()

    def disable(self):
        self.b.disable()

    def get_existing(self) -> list:
        return self.b.get_existing()
