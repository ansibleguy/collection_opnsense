from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    validate_int_fields, validate_port
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class Rule(BaseModule):
    FIELD_ID = 'description'
    CMDS = {
        'add': 'addrule',
        'del': 'delrule',
        'set': 'setrule',
        'search': 'get',
        'toggle': 'togglerule',
    }
    API_KEY_PATH = 'ts.rules.rule'
    API_MOD = 'trafficshaper'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = [
        'target', 'interface', 'interface2', 'protocol', 'max_packet_length',
        'source_invert', 'source_net', 'source_port', 'destination_invert',
        'destination_net', 'destination_port', 'dscp', 'direction', 'sequence',
    ]
    FIELDS_ALL = ['enabled', FIELD_ID]
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
        'list': ['dscp', 'destination_net', 'source_net'],
        'select': [
            'interface', 'interface2', 'protocol', 'direction', 'target',
        ],
    }
    INT_VALIDATIONS = {
        'sequence': {'min': 1, 'max': 1000000},
        'max_packet_length': {'min': 2, 'max': 65535},
    }
    EXIST_ATTR = 'rule'
    TIMEOUT = 20.0  # 'get' timeout
    SEARCH_ADDITIONAL = {
        'existing_pipes': 'ts.pipes.pipe',
        'existing_queues': 'ts.queues.queue',
    }

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.rule = {}
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

        self.b.find(match_fields=[self.FIELD_ID])

        if self.p['state'] == 'present':
            self.b.find_single_link(
                field='target_pipe',
                existing=self.existing_pipes,
                existing_field_id='description',
                fail=False,
                set_field='target',
            )

            if not hasattr(self.p, 'target') or self.p['target'] is None:
                self.b.find_single_link(
                    field='target_queue',
                    existing=self.existing_queues,
                    existing_field_id='description',
                    set_field='target',
                    fail=True,
                )

            self.r['diff']['after'] = self.b.build_diff(data=self.p)

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

    def reload(self) -> None:
        if self.p['reset']:
            self.API_CMD_REL = 'flushreload'

        self.b.reload()
