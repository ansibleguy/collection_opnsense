from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
     is_true, get_selected, validate_int_fields
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.base import Base


class Pipe:
    CMDS = {
        'add': 'addPipe',
        'del': 'delPipe',
        'set': 'setPipe',
        'search': 'get',
        'toggle': 'togglePipe',
    }
    API_KEY = 'pipe'
    API_KEY_1 = 'ts'
    API_KEY_2 = 'pipes'
    API_MOD = 'trafficshaper'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = [
        'bandwidth', 'bandwidth_metric', 'queue', 'mask', 'buckets', 'scheduler',
        'codel_enable', 'codel_target', 'codel_interval', 'codel_ecn_enable',
        'pie_enable', 'fqcodel_quantum', 'fqcodel_limit', 'fqcodel_flows',
        'delay',
    ]
    FIELDS_ALL = ['enabled', 'description']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'bandwidth_metric': 'bandwidthMetric',
    }
    INT_VALIDATIONS = {
        # 'id': {'min': 1, 'max': 65535},
        'queue': {'min': 2, 'max': 100},
        'buckets': {'min': 1, 'max': 65535},
        'codel_target': {'min': 1, 'max': 10000},
        'codel_interval': {'min': 1, 'max': 10000},
        'fqcodel_quantum': {'min': 1, 'max': 65535},
        'fqcodel_limit': {'min': 1, 'max': 65535},
        'fqcodel_flows': {'min': 1, 'max': 65535},
        'delay': {'min': 1, 'max': 3000},
    }
    EXIST_ATTR = 'pipe'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        self.m = module
        self.p = module.params
        self.r = result
        self.s = Session(module=module) if session is None else session
        self.exists = False
        self.pipe = {}
        self.call_cnf = {  # config shared by all calls
            'module': self.API_MOD,
            'controller': self.API_CONT,
        }
        self.existing_entries = None
        self.b = Base(instance=self)

    def check(self):
        if self.p['state'] == 'present' and self.p['bandwidth'] is None:
            self.m.fail_json('You need to provide bandwidth to create a shaper pipe!')

        validate_int_fields(module=self.m, data=self.p, field_minmax=self.INT_VALIDATIONS)

        self.b.find(match_fields=['description'])
        if self.exists:
            self.call_cnf['params'] = [self.pipe['uuid']]

        if self.p['state'] == 'present':
            self.r['diff']['after'] = self.b.build_diff(data=self.p)

    @staticmethod
    def _simplify_existing(pipe: dict) -> dict:
        # makes processing easier
        return {
            'uuid': pipe['uuid'],
            'enabled': is_true(pipe['enabled']),
            'bandwidth': pipe['bandwidth'],
            'bandwidth_metric': get_selected(pipe['bandwidthMetric']),
            'queue': pipe['queue'],
            'mask': get_selected(pipe['mask']),
            'buckets': pipe['buckets'],
            'scheduler': get_selected(pipe['scheduler']),
            'pie_enable': is_true(pipe['pie_enable']),
            'codel_enable': is_true(pipe['codel_enable']),
            'codel_ecn_enable': is_true(pipe['codel_ecn_enable']),
            'codel_target': pipe['codel_target'],
            'codel_interval': pipe['codel_interval'],
            'fqcodel_quantum': pipe['fqcodel_quantum'],
            'fqcodel_limit': pipe['fqcodel_limit'],
            'fqcodel_flows': pipe['fqcodel_flows'],
            'delay': pipe['delay'],
            'description': pipe['description'],
        }

    def get_existing(self) -> list:
        return self.b.get_existing()

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
