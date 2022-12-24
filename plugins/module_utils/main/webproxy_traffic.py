from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import GeneralModule


class Traffic(GeneralModule):
    CMDS = {
        'set': 'set',
        'search': 'get',
    }
    API_KEY_1 = 'proxy'
    API_KEY_2 = 'general'
    API_KEY = 'traffic'
    API_MOD = 'proxy'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = [
        'download_kb_max', 'upload_kb_max', 'throttle_kb_bandwidth',
        'throttle_kb_host_bandwidth', 'enabled',
    ]
    FIELDS_ALL = FIELDS_CHANGE
    FIELDS_TRANSLATE = {
        'download_kb_max': 'maxDownloadSize',
        'upload_kb_max': 'maxUploadSize',
        'throttle_kb_bandwidth': 'OverallBandwidthTrotteling',
        'throttle_kb_host_bandwidth': 'perHostTrotteling',
    }
    FIELDS_TYPING = {
        'int': [
            'download_kb_max', 'upload_kb_max', 'throttle_kb_bandwidth',
            'throttle_kb_host_bandwidth',
        ],
        'bool': ['enabled']
    }
    TIMEOUT = 60.0

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        GeneralModule.__init__(self=self, m=module, r=result, s=session)
