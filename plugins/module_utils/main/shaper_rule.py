from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    is_true, get_selected, validate_int_fields, get_selected_list, validate_port
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.base import Base


class Rule:
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
    INT_VALIDATIONS = {
        'sequence': {'min': 1, 'max': 1000000},
        'max_packet_length': {'min': 2, 'max': 65535},
    }
    EXIST_ATTR = 'rule'
    TIMEOUT = 20.0  # 'get' timeout

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        self.m = module
        self.p = module.params
        self.r = result
        self.s = Session(
            module=module,
            timeout=self.TIMEOUT,
        ) if session is None else session
        self.exists = False
        self.rule = {}
        self.target_found = False
        self.call_cnf = {  # config shared by all calls
            'module': self.API_MOD,
            'controller': self.API_CONT,
        }
        self.existing_entries = None
        self.existing_queues = None
        self.existing_pipes = None
        self.b = Base(instance=self)

    def check(self):
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

            self.p['dscp'].sort()
            self.r['diff']['after'] = self.b.build_diff(data=self.p)

    def _search_call(self) -> dict:
        raw = self.s.get(cnf={
            **self.call_cnf, **{'command': self.CMDS['search']}
        })[self.API_KEY_1]
        self.existing_pipes = raw['pipes']['pipe']
        self.existing_queues = raw['queues']['queue']
        return raw[self.API_KEY_2][self.API_KEY]

    @staticmethod
    def _simplify_existing(rule: dict) -> dict:
        # makes processing easier
        target_uuid = get_selected(rule['target'])
        simple = {
            'uuid': rule['uuid'],
            'sequence': rule['sequence'],
            'enabled': is_true(rule['enabled']),
            'interface': get_selected(rule['interface']),
            'interface2': get_selected(rule['interface2']),
            'protocol': get_selected(rule['proto']),
            'source_invert': is_true(rule['source_not']),
            'destination_invert': is_true(rule['destination_not']),
            'destination_net': get_selected(rule['destination']),
            'source_net': get_selected(rule['source']),
            'source_port': rule['src_port'],
            'destination_port': rule['dst_port'],
            'max_packet_length': rule['iplen'],
            'direction': get_selected(rule['direction']),
            'dscp': get_selected_list(rule['dscp']),
            'description': rule['description'],
            'target': target_uuid,
        }
        simple['dscp'].sort()
        return simple

    def _find_pipe(self):
        if self.p['target_pipe'] not in ['', None] and len(self.existing_pipes) > 0:
            for uuid, pipe in self.existing_pipes.items():
                if pipe['description'] == self.p['target_pipe']:
                    self.p['target'] = uuid
                    self.target_found = True
                    break

    def _find_queue(self):
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

    def create(self):
        self.b.create()

    def update(self):
        self.b.update(enable_switch=True)

    def process(self):
        self.b.process()

    def delete(self):
        self.b.delete()

    def reload(self):
        self.b.reload()
