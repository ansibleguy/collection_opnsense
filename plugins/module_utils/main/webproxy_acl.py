from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import GeneralModule


class General(GeneralModule):
    CMDS = {
        'set': 'set',
        'search': 'get',
    }
    API_KEY_1 = 'proxy'
    API_KEY_2 = 'forward'
    API_KEY = 'acl'
    API_MOD = 'proxy'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = [
        'allow', 'exclude', 'banned', 'exclude_domains', 'block_domains',
        'block_user_agents', 'block_mime_types', 'exclude_google', 'youtube_filter',
        'ports_tcp', 'ports_ssl',
    ]
    FIELDS_ALL = FIELDS_CHANGE
    FIELDS_TRANSLATE = {
        'allow': 'allowedSubnets',
        'exclude': 'unrestricted',
        'banned': 'bannedHosts',
        'exclude_domains': 'whiteList',
        'block_domains': 'blackList',
        'block_user_agents': 'browser',
        'block_mime_types': 'mimeType',
        'exclude_google': 'googleapps',
        'youtube_filter': 'youtube',
        'ports_tcp': 'safePorts',
        'ports_ssl': 'sslPorts',
    }
    FIELDS_TYPING = {
        'list': [
            'allow', 'exclude', 'banned', 'exclude_domains', 'block_domains',
            'block_user_agents', 'block_mime_types', 'exclude_google',
            'ports_tcp', 'ports_ssl',
        ],
        'select': ['youtube_filter']
    }
    FIELDS_IGNORE = ['remoteACLs']

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        GeneralModule.__init__(self=self, m=module, r=result, s=session)
