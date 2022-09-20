from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    is_true, get_selected, validate_int_fields
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.base import Base


class Queue:
    CMDS = {
        'add': 'addQueue',
        'del': 'delQueue',
        'set': 'setQueue',
        'search': 'get',
        'toggle': 'toggleQueue',
    }
    API_KEY = 'queue'
    API_KEY_1 = 'ts'
    API_KEY_2 = 'queues'
    API_MOD = 'trafficshaper'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = [
        'codel_enable', 'codel_ecn_enable', 'pie_enable',  'mask',
        'pipe', 'buckets', 'codel_target', 'codel_interval', 'weight',
    ]
    FIELDS_ALL = ['enabled', 'description']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    INT_VALIDATIONS = {
        'weight': {'min': 1, 'max': 100},
        'buckets': {'min': 1, 'max': 65535},
        'codel_target': {'min': 1, 'max': 10000},
        'codel_interval': {'min': 1, 'max': 10000},
    }
    EXIST_ATTR = 'queue'
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
        self.queue = {}
        self.pipe_found = False
        self.call_cnf = {  # config shared by all calls
            'module': self.API_MOD,
            'controller': self.API_CONT,
        }
        self.existing_entries = None
        self.existing_pipes = None
        self.b = Base(instance=self)

    def check(self):
        validate_int_fields(module=self.m, data=self.p, field_minmax=self.INT_VALIDATIONS)

        # checking if item exists
        self.b.find(match_fields=['description'])
        if self.exists:
            self.call_cnf['params'] = [self.queue['uuid']]

        if self.p['state'] == 'present':
            if self.p['pipe'] in [None, '']:
                self.m.fail_json("You need to provide a 'pipe' to create a shaper queue!")

            if self.p['weight'] in [None, '']:
                if not self.exists:
                    self.m.fail_json("You need to provide 'weight' to create a shaper queue!")

                else:
                    self.p['weight'] = self.queue['weight']

        self._find_pipe()

        if self.p['state'] == 'present':
            if not self.pipe_found:
                self.m.fail_json(f"Provided pipe does not exist: '{self.p['pipe']}'")

            self.r['diff']['after'] = self.b.build_diff(data=self.p)

    def _search_call(self) -> dict:
        raw = self.s.get(cnf={
            **self.call_cnf, **{'command': self.CMDS['search']}
        })[self.API_KEY_1]
        self.existing_pipes = raw['pipes']['pipe']
        return raw[self.API_KEY_2][self.API_KEY]

    @staticmethod
    def _simplify_existing(queue: dict) -> dict:
        # makes processing easier
        return {
            'uuid': queue['uuid'],
            'enabled': is_true(queue['enabled']),
            'weight': queue['weight'],
            'mask': get_selected(queue['mask']),
            'buckets': queue['buckets'],
            'pie_enable': is_true(queue['pie_enable']),
            'codel_enable': is_true(queue['codel_enable']),
            'codel_ecn_enable': is_true(queue['codel_ecn_enable']),
            'codel_target': queue['codel_target'],
            'codel_interval': queue['codel_interval'],
            'description': queue['description'],
            'pipe': get_selected(queue['pipe']),
        }

    def _find_pipe(self):
        if len(self.existing_pipes) > 0:
            for uuid, pipe in self.existing_pipes.items():
                if pipe['description'] == self.p['pipe']:
                    self.p['pipe'] = uuid
                    self.pipe_found = True
                    break

    def get_existing(self) -> list:
        existing = []

        for entry in self.b.get_existing():
            entry['pipe'] = self.existing_pipes[entry['pipe']]['description']
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
