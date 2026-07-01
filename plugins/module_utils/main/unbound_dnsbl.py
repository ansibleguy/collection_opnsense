from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class DnsBL(BaseModule):
    FIELD_ID = 'name'
    CMDS = {
        'add': 'addDnsbl',
        'set': 'setDnsbl',
        'del': 'delDnsbl',
        'search': 'searchDnsbl',
        'detail': 'getDnsbl',
    }
    API_KEY_PATH = 'blocklist'
    API_MOD = 'unbound'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'dnsbl'
    FIELDS_CHANGE = [
        'enabled', 'providers', 'download_urls', 'domains_allow', 'domains_block', 'wildcard_domains_block',
        'source_networks', 'cache_ttl', 'nxdomain_address', 'nxdomain',
    ]
    FIELDS_ALL = [FIELD_ID]
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'name': 'description',
        'providers': 'type',
        'download_urls': 'lists',
        'nxdomain_address': 'address',
        'domains_allow': 'allowlists',
        'domains_block': 'blocklists',
        'wildcard_domains_block': 'wildcards',
        'source_networks': 'source_nets',
    }
    FIELDS_TYPING = {
        'bool': ['enabled', 'nxdomain'],
        'int': ['cache_ttl'],
        'list': [
            'providers', 'download_urls', 'domains_allow', 'domains_block',
            'wildcard_domains_block', 'source_networks',
        ],
    }
    EXIST_ATTR = 'bl'
    TIMEOUT = 60.0  # 'reload' timeout

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.bl = {}
