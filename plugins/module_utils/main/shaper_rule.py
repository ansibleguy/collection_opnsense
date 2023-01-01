from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    validate_int_fields, validate_port
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class Rule(BaseModule):
    CMDS = {
        'add': 'addrule',
        'del': 'delrule',
        'set': 'setrule',
        'search': 'get',
        'toggle': 'togglerule',
    }
    API_KEY = 'rule'
    API_KEY_1 = 'ts'
    API_KEY_2 = 'rules'
    API_MOD = 'trafficshaper'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = [
        'target', 'interface', 'interface2', 'protocol', 'max_packet_length',
        'source_invert', 'source_net', 'source_port', 'destination_invert',
        'destination_net', 'destination_port', 'dscp', 'direction',
    ]  # 'sequence' => not working
    FIELDS_ALL = ['enabled', 'description']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'max_packet_length': 'iplen',
        'protocol': 'proto',
        'source_port': 'src_port',
        'source_net': 'source',
        'source_invert': 'source_not',
        'destination_net': 'destination',
        'destination_invert': 'destination_not',
        'destination_port': 'dst_port',
    }
    FIELDS_TYPING = {
        'bool': ['enabled', 'source_invert', 'destination_invert'],
        'list': ['dscp'],
        'select': [
            'interface', 'interface2', 'protocol', 'destination_net', 'source_net',
            'direction', 'target',
        ],
    }
    INT_VALIDATIONS = {
        'sequence': {'min': 1, 'max': 1000000},
        'max_packet_length': {'min': 2, 'max': 65535},
    }
    EXIST_ATTR = 'rule'
    TIMEOUT = 20.0  # 'get' timeout

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.rule = {}
        self.target_found = False
        self.existing_queues = None
        self.existing_pipes = None

    def check(self) -> None:
        validate_int_fields(module=self.m, data=self.p, field_minmax=self.INT_VALIDATIONS)
        validate_port(module=self.m, port=self.p['source_port'])
        validate_port(module=self.m, port=self.p['destination_port'])

        if self.p['state'] == 'present':
            if self.p['target_pipe'] in [None, ''] and \
                    self.p['target_queue'] in [None, '']:
                self.m.fail_json(
                    "You need to provide a 'target_pipe' or 'target_queue' to "
                    "create a shaper rule!"
                )

        self.b.find(match_fields=['description'])
        if self.exists:
            self.call_cnf['params'] = [self.rule['uuid']]

        self._find_pipe()
        if not self.target_found:
            self._find_queue()

        if self.p['state'] == 'present':
            if not self.target_found:
                target_type = 'queue' if self.p['target_pipe'] in [None, ''] else 'pipe'
                self.m.fail_json(
                    f"Provided {target_type} does not exist: "
                    f"'{self.p[f'target_{target_type}']}'"
                )

            self.r['diff']['after'] = self.b.build_diff(data=self.p)

    def _search_call(self) -> dict:
        raw = self.s.get(cnf={
            **self.call_cnf, **{'command': self.CMDS['search']}
        })[self.API_KEY_1]
        self.existing_pipes = raw['pipes']['pipe']
        self.existing_queues = raw['queues']['queue']
        return raw[self.API_KEY_2][self.API_KEY]

    def _find_pipe(self) -> None:
        if self.p['target_pipe'] not in ['', None] and len(self.existing_pipes) > 0:
            for uuid, pipe in self.existing_pipes.items():
                if pipe['description'] == self.p['target_pipe']:
                    self.p['target'] = uuid
                    self.target_found = True
                    break

    def _find_queue(self) -> None:
        if self.p['target_queue'] not in ['', None] and len(self.existing_queues) > 0:
            for uuid, queue in self.existing_queues.items():
                if queue['description'] == self.p['target_queue']:
                    self.p['target'] = uuid
                    self.target_found = True
                    break

    def get_existing(self) -> list:
        existing = []

        for entry in self.b.get_existing():
            entry['target_pipe'], entry['target_queue'] = None, None
            target = entry['target']

            if target in self.existing_pipes:
                entry['target_pipe'] = self.existing_pipes[target]['description']

            elif target in self.existing_queues:
                entry['target_queue'] = self.existing_queues[target]['description']

            entry.pop('target')

            existing.append(entry)

        return existing
