from typing import Callable
from re import match as regex_match
from re import compile as regex_compile
from re import IGNORECASE as REGEX_IGNORECASE
from re import UNICODE as REGEX_UNICODE
from socket import getservbyname
from ipaddress import ip_address, ip_network, IPv4Address, IPv6Address, IPv6Network, AddressValueError, \
    NetmaskValueError

from ansible.module_utils.basic import AnsibleModule

# pylint: disable=W0611
#   (proxied imports)
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.main import \
    is_unset, ensure_list, is_true, unset_check_error
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.handler import \
    exit_bug

MATCH_DOMAIN = regex_compile(
    r'^(([a-zA-Z]{1})|([a-zA-Z]{1}[a-zA-Z]{1})|'
    r'([a-zA-Z]{1}[0-9]{1})|([0-9]{1}[a-zA-Z]{1})|'
    r'([a-zA-Z0-9][-_.a-zA-Z0-9]{0,61}[a-zA-Z0-9]))\.'
    r'([a-zA-Z]{2,13}|[a-zA-Z0-9-]{2,30}.[a-zA-Z]{2,3})$'
)
MATCH_EMAIL_USER = regex_compile(
    # dot-atom
    r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+"
    r"(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*$"
    # quoted-string
    r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|'
    r"""\\[\001-\011\013\014\016-\177])*"$)""",
    REGEX_IGNORECASE
)
MATCH_EMAIL_DOMAIN = regex_compile(
    # domain
    r'(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+'
    r'(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?$)'
    # literal form, ipv4 address (SMTP 4.1.3)
    r'|^\[(25[0-5]|2[0-4]\d|[0-1]?\d?\d)'
    r'(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}\]$',
    REGEX_IGNORECASE
)
IP_MIDDLE_OCTET = r"(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5]))"
IP_LAST_OCTET = r"(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))"
MATCH_URL_RAW = regex_compile(
    r"^"
    # protocol identifier
    r"(?:(?:https?|ftp)://)"
    # user:pass authentication
    r"(?:\S+(?::\S*)?@)?"
    r"(?:"
    r"(?P<private_ip>"
    # IP address exclusion
    # private & local networks
    r"(?:(?:10|127)" + IP_MIDDLE_OCTET + r"{2}" + IP_LAST_OCTET + r")|"
    r"(?:(?:169\.254|192\.168)" + IP_MIDDLE_OCTET + IP_LAST_OCTET + r")|"
    r"(?:172\.(?:1[6-9]|2\d|3[0-1])" + IP_MIDDLE_OCTET + IP_LAST_OCTET + r"))"
    r"|"
    # IP address dotted notation octets
    # excludes loopback network 0.0.0.0
    # excludes reserved space >= 224.0.0.0
    # excludes network & broadcast addresses
    # (first & last IP address of each class)
    r"(?P<public_ip>"
    r"(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])"
    r"" + IP_MIDDLE_OCTET + r"{2}"
    r"" + IP_LAST_OCTET + r")"
    r"|"
    # host name
    r"(?:(?:[a-z\u00a1-\uffff0-9]-?)*[a-z\u00a1-\uffff0-9]+)"
    # domain name
    r"(?:\.(?:[a-z\u00a1-\uffff0-9]-?)*[a-z\u00a1-\uffff0-9]+)*"
    # TLD identifier
    r"(?:\.(?:[a-z\u00a1-\uffff]{2,}))"
    r")"
    # port number
    r"(?::\d{2,5})?"
    # resource path
    r"(?:/\S*)?"
    # query string
    r"(?:\?\S*)?"
    r"$",
    REGEX_UNICODE | REGEX_IGNORECASE
)
MATCH_URL = regex_compile(MATCH_URL_RAW)
MATCH_MAC_ADDRESS = regex_compile(r'^(?:[0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}$')
MATCH_PARTIAL_MAC_ADDRESS = regex_compile(r'^(?:[0-9a-fA-F]{2}:){1,5}[0-9a-fA-F]{2}$')
# see: https://en.wikipedia.org/wiki/Hostname#Restrictions_on_valid_host_names
MATCH_HOSTNAME = regex_compile(r'^[a-zA-Z0-9-\.]{1,253}$')
MATCH_UUID = regex_compile(r'^[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}$')


def _is_matching(compiled_regex, value: (str, None)) -> bool:
    if value is None:
        value = ''

    return compiled_regex.match(value) is not None


def is_valid_domain(value: str) -> bool:
    # see: https://validators.readthedocs.io/en/latest/_modules/validators/domain.html#domain
    return _is_matching(compiled_regex=MATCH_DOMAIN, value=value)


def is_valid_email(value) -> bool:
    # see: https://validators.readthedocs.io/en/latest/_modules/validators/email.html
    if not value or '@' not in value:
        return False

    email_user, email_domain = value.rsplit('@', 1)

    if not _is_matching(compiled_regex=MATCH_EMAIL_USER, value=email_user):
        return False

    if not _is_matching(compiled_regex=MATCH_EMAIL_DOMAIN, value=email_domain):
        # Try for possible IDN domain-part
        try:
            domain_part = email_domain.encode('idna').decode('ascii')
            return _is_matching(compiled_regex=MATCH_EMAIL_DOMAIN, value=domain_part)

        except UnicodeError:
            return False

    return True


def is_valid_url(value: str) -> bool:
    # see: https://validators.readthedocs.io/en/latest/_modules/validators/url.html
    return _is_matching(compiled_regex=MATCH_URL, value=value)


def is_valid_mac_address(value: str) -> bool:
    # see: https://validators.readthedocs.io/en/latest/_modules/validators/mac_address.html
    return _is_matching(compiled_regex=MATCH_MAC_ADDRESS, value=value)


def is_valid_partial_mac_address(value: str) -> bool:
    # see: https://validators.readthedocs.io/en/latest/_modules/validators/mac_address.html
    return _is_matching(compiled_regex=MATCH_PARTIAL_MAC_ADDRESS, value=value)


def is_valid_network(value: str) -> bool:
    if '-' in value:
        for _value in value.split('-', 1):
            if not is_ip(_value):
                return False

        return True

    value = value.lstrip('!')
    return is_ip_or_network(value)


def is_valid_host(value: str) -> bool:
    if is_valid_domain(value):
        return True

    for _value in value.split('-', 1):
        _value = _value.strip('!')
        if not is_ip(_value):
            return False

    return True


def validate_port(module: AnsibleModule, port: int, error_func: Callable = None) -> bool:
    if error_func is None:
        error_func = module.fail_json

    if is_unset(port):
        return True

    if 1 <= int(port) <= 65535:
        return True

    error_func(f"Value '{port}' is an invalid port!")
    return False


def validate_port_or_range(module: AnsibleModule, port: str, error_func: Callable = None, range_sep: str = '-') -> bool:
    if error_func is None:
        error_func = module.fail_json

    if port == 'any' or is_unset(port):
        return True

    for _value in port.split(range_sep, 1):
        if _value.isdecimal() and (1 <= int(_value) <= 65535):
            continue

        try:
            getservbyname(_value)
            continue
        except OSError:
            pass

        error_func(f"Value '{port}' is an invalid port or range!")
        return False

    return True


def validate_int_fields(
        module: AnsibleModule, data: dict, field_minmax: dict,
        error_func: Callable = None
):
    if error_func is None:
        error_func = module.fail_json

    for field, valid in field_minmax.items():
        try:
            value = int(data[field])

        except (TypeError, ValueError, KeyError):
            continue

        if 'min' in valid and value < valid['min']:
            error_func(
                f"Value of field '{field}' is not valid - "
                f"Must be greater than or equal to {valid['min']}!"
            )

        elif 'max' in valid and value > valid['max']:
            error_func(
                f"Value of field '{field}' is not valid - "
                f"Must be less than or equal to {valid['max']}!"
            )


def validate_str_fields(
        module: AnsibleModule, data: dict, field_regex: dict = None,
        field_minmax_length: dict = None, allow_empty: bool = False,
) -> None:
    if field_minmax_length is not None:
        for field, min_max_length in field_minmax_length.items():
            if not allow_empty and 'min' in min_max_length and min_max_length['min'] == 0:
                allow_empty = True

            if not unset_check_error(params=data, field=field, fail=not allow_empty):
                continue

            if 'min' not in min_max_length or 'max' not in min_max_length:
                exit_bug("Values of 'STR_LEN_VALIDATIONS' must have a 'min' and 'max' attribute!")

            if min_max_length['min'] < len(str(data[field])) > min_max_length['max']:
                module.fail_json(
                    f"Value of field '{field}' is not valid - "
                    f"Invalid length must be between {min_max_length['min']} and {min_max_length['max']}!"
                )

    if field_regex is not None:
        for field, regex in field_regex.items():
            if not unset_check_error(params=data, field=field, fail=not allow_empty):
                continue

            if regex_match(regex, data[field]) is None:
                module.fail_json(
                    f"Value of field '{field}' is not valid - "
                    f"Must match regex '{regex}'!"
                )


def is_ip(host: str, ignore_empty: bool = False, strip_enclosure: bool = True) -> bool:
    if ignore_empty and is_unset(host):
        return True

    if strip_enclosure and host.startswith('['):
        host = host[1:-1]

    try:
        ip_address(host)
        return True

    except ValueError:
        return False


def is_ip4(host: str, ignore_empty: bool = False) -> bool:
    if ignore_empty and is_unset(host):
        return True

    try:
        IPv4Address(host)
        return True

    except (AddressValueError, NetmaskValueError):
        return False


def is_ip6(host: str, ignore_empty: bool = False, strip_enclosure: bool = True) -> bool:
    if ignore_empty and is_unset(host):
        return True

    if strip_enclosure and host.startswith('['):
        host = host[1:-1]

    try:
        IPv6Address(host)
        return True

    except (AddressValueError, NetmaskValueError):
        return False


def is_network(entry: str, strict: bool = False) -> bool:
    try:
        ip_network(entry, strict=strict)
        return True

    except ValueError:
        return False


def is_ip_or_network(entry: str, strict: bool = False) -> bool:
    valid = is_ip(entry)

    if valid:
        return valid

    return is_network(entry=entry, strict=strict)


def is_ip6_network(entry: str, strict: bool = False) -> bool:
    try:
        return isinstance(ip_network(entry, strict=strict), IPv6Network)

    except ValueError:
        return False


def valid_hostname(name: str) -> bool:
    _valid_domain = is_valid_domain(name)
    _valid_hostname = _is_matching(compiled_regex=MATCH_HOSTNAME, value=name)
    return all([_valid_domain, _valid_hostname])
