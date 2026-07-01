from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import GeneralModule
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.main import is_unset
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.validate import is_ip, is_valid_domain


class Nut(GeneralModule):
    CMDS = {
        'set': 'set',
        'search': 'get',
    }
    API_KEY_PATH = 'nut'
    API_KEY_PATH_REQ = API_KEY_PATH
    API_MOD = 'nut'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'

    FIELDS_TRANSLATE = {
        # General section
        'enabled': ('general', 'enable'),
        'mode': ('general', 'mode'),
        'name': ('general', 'name'),
        'listen': ('general', 'listen'),
        # Account section
        'admin_password': ('account', 'admin_password'),
        'monitor_password': ('account', 'mon_password'),
        # USBHID-Driver section
        'usbhid_enable': ('usbhid', 'enable'),
        'usbhid_args': ('usbhid', 'args'),
        # APCSMART-Driver section
        'apcsmart_enable': ('apcsmart', 'enable'),
        'apcsmart_args': ('apcsmart', 'args'),
        # APCUPSD-Driver section
        'apcupsd_enable': ('apcupsd', 'enable'),
        'apcupsd_host': ('apcupsd', 'hostname'),
        'apcupsd_port': ('apcupsd', 'port'),
        # BCMXCPUSB-Driver section
        'bcmxcpusb_enable': ('bcmxcpusb', 'enable'),
        'bcmxcpusb_args': ('bcmxcpusb', 'args'),
        # BlazerUSB-Driver section
        'blazerusb_enable': ('blazerusb', 'enable'),
        'blazerusb_args': ('blazerusb', 'args'),
        # BlazerSerial-Driver section
        'blazerser_enable': ('blazerser', 'enable'),
        'blazerser_args': ('blazerser', 'args'),
        # Netclient section
        'netclient_enable': ('netclient', 'enable'),
        'netclient_address': ('netclient', 'address'),
        'netclient_port': ('netclient', 'port'),
        'netclient_user': ('netclient', 'user'),
        'netclient_password': ('netclient', 'password'),
        # QX-Driver section
        'qx_enable': ('qx', 'enable'),
        'qx_args': ('qx', 'args'),
        # Riello-Driver section
        'riello_enable': ('riello', 'enable'),
        'riello_args': ('riello', 'args'),
        # SNMP-Driver section
        'snmp_enable': ('snmp', 'enable'),
        'snmp_args': ('snmp', 'args'),
    }

    FIELDS_CHANGE = list(FIELDS_TRANSLATE.keys())
    FIELDS_ALL = FIELDS_CHANGE
    FIELDS_DIFF_NO_LOG = [
        'admin_password', 'monitor_password', 'netclient_password'
    ]

    FIELDS_TYPING = {
        'bool': [
            'enabled', 'usbhid_enable', 'apcsmart_enable', 'apcupsd_enable',
            'bcmxcpusb_enable', 'blazerusb_enable', 'blazerser_enable',
            'netclient_enable', 'qx_enable', 'riello_enable', 'snmp_enable'
        ],
        'str': [
            'name', 'admin_password', 'monitor_password', 'apcupsd_host',
            'netclient_address', 'netclient_user', 'netclient_password'
        ],
        'int': ['apcupsd_port', 'netclient_port'],
        'list': [
            'listen', 'usbhid_args', 'apcsmart_args', 'bcmxcpusb_args',
            'blazerusb_args', 'blazerser_args', 'qx_args', 'riello_args',
            'snmp_args'
        ],
        'select': ['mode'],
    }

    STR_VALIDATIONS = {
        'name': r'^([0-9a-zA-Z._\-]){1,128}$',
    }
    INT_VALIDATIONS = {
        'apcupsd_port': {'min': 1, 'max': 65535},
        'netclient_port': {'min': 1, 'max': 65535},
    }

    TIMEOUT = 60.0

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        GeneralModule.__init__(self=self, m=module, r=result, s=session)

    @staticmethod
    def _is_ip_or_domain(value) -> bool:
        # Ignoring empty
        if is_unset(value):
            return True

        return is_ip(value, ignore_empty=True) or is_valid_domain(value)

    def check(self) -> None:
        self._base_check()
        if isinstance(self.p['listen'], list):
            for ip in self.p['listen']:
                if not is_ip(ip, ignore_empty=True):
                    self.m.fail_json(
                        f"It seems you provided a invalid IP address as 'listen': '{ip}'"
                    )

        else:
            ip = self.p['listen']
            if not is_ip(ip, ignore_empty=True):
                self.m.fail_json(
                    f"It seems you provided a invalid IP address as 'listen': '{ip}'"
                )

        for field in ['apcupsd_host', 'netclient_address']:
            ip = self.p[field]
            if field == 'apcupsd_host' and ip == 'localhost':
                # Default is localhost
                continue

            if not self._is_ip_or_domain(ip):
                self.m.fail_json(
                    f"It seems you provided a invalid IP or domain as '{field}': '{ip}'"
                )
