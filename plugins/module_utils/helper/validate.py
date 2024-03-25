from re import compile as regex_compile
from re import IGNORECASE as REGEX_IGNORECASE
from re import UNICODE as REGEX_UNICODE

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
