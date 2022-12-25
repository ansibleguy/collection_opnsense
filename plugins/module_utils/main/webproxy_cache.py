from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import GeneralModule


class Cache(GeneralModule):
    CMDS = {
        'set': 'set',
        'search': 'get',
    }
    API_KEY_PATH = 'proxy.general.cache.local'
    API_KEY_PATH_REQ = API_KEY_PATH
    API_MOD = 'proxy'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = [
        'memory_mb', 'size_mb', 'directory', 'layer_1', 'layer_2',
        'size_mb_max', 'memory_kb_max', 'memory_cache_mode',
        'cache_linux_packages', 'cache_windows_updates',
    ]
    FIELDS_ALL = FIELDS_CHANGE
    FIELDS_TRANSLATE = {
        'memory_mb': 'cache_mem',
        'size_mb': 'size',
        'size_mb_max': 'maximum_object_size',
        'memory_kb_max': 'maximum_object_size_in_memory',
        'layer_1': 'l1',
        'layer_2': 'l2',
    }
    FIELDS_TYPING = {
        'bool': ['cache_linux_packages', 'cache_windows_updates'],
        'select': ['memory_cache_mode'],
        'int': [
            'memory_mb', 'size_mb', 'layer_1', 'layer_2', 'size_mb_max',
            'memory_kb_max'
        ],
    }
    INT_VALIDATIONS = {
        'size_mb_max': {'min': 1, 'max': 99999},
        'memory_kb_max': {'min': 1, 'max': 99999},
    }

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        GeneralModule.__init__(self=self, m=module, r=result, s=session)
