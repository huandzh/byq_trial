#! -*- coding:utf-8 -*-
"""Authorization for yuqing

.. moduleauthor:: Huan Di <hd@iamhd.top>

"""
import hmac
import hashlib
import urllib.parse
import datetime
import time
import json

# secrets

SECRET_NAMES = set(['access_key',
                    'secret_key',
                    'api_key',
                    'api_secret'])


def load_secrets(file_path):
    with open(file_path, 'r') as fp:
        secrets = json.load(fp)
    assert isinstance(secrets, dict), 'Error: secrets should be a dict'
    assert SECRET_NAMES == secrets.keys(), 'Error: missing keys in secrets'
    return secrets

# signers


def get_timestamp_now():
    """Get timestamp for utc now.

    :returns: timestamp
    :rtype: string

    """
    utc_time = datetime.datetime.utcnow()
    timestamp = utc_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    return timestamp


def get_yuqing_token_now(api_secret, api_key):
    """Get token for yuqing service, using timestamp for now.

    :param api_secret: str, yuqing api secret
    :param api_key: str, yuqing api key
    :returns: (timestamp, token) for yuqing service
    :rtype: (string, string)

    """
    # Beware: timestamp for yuqing is of different format from bce_signer
    timestamp = str(int(time.time()))
    token = hmac.new(api_secret.encode('utf-8'),
                     (api_key + timestamp).encode('utf-8'),
                     hashlib.sha1).hexdigest()
    return timestamp, token


def parse_host_path_from(url):
    """Parse a url and get host and path

    :param url: str, url
    :returns: (host, path)
    :rtype: (string, string)

    """
    url_parsed = urllib.parse.urlparse(url)
    host = url_parsed.netloc
    path = url_parsed.path
    return host, path


class BasicBCESigner:
    """Class as a simple bce_signer for yuqing.

    It's not a fully implemented signer.
    """

    # default settings
    VERSION = 1
    BCE_VERSION_TEMPLATE = 'bce-auth-v{VERSION}'
    METHOD = 'POST'
    EXPIRE_TIME = '1800'

    def __init__(self, access_key, secret_key,
                 url, method=METHOD):
        """Init signer.

        :param access_key: str, baidu AK
        :param secret_key: str, baidu SK
        :param url: str, full url calling
        :param method: str, http method calling

        """
        self.access_key = access_key
        self.secret_key = secret_key
        self.url = url
        self.method = method
        self.bce_version = BasicBCESigner.BCE_VERSION_TEMPLATE.format(
            VERSION=BasicBCESigner.VERSION)

    def gen(self):
        """Gen signature string, a shortcut using default params

        :returns: signature string
        :rtype: string

        """
        return BasicBCESigner.gen_authorization(self.access_key,
                                                self.secret_key,
                                                get_timestamp_now(),
                                                BasicBCESigner.EXPIRE_TIME,
                                                self.url,
                                                self.method,
                                                self.bce_version)

    @staticmethod
    def gen_authorization(access_key, secret_key,
                          timestamp, expire_time,
                          url, method,
                          bce_version):
        """Gen authorization string

        :param access_key: str, baidu AK
        :param secret_key: str, baidu SK
        :param timestamp: str, timestamp
        :param expire_time: str, expire_time as string
        :param url: str, full url calling
        :param method: str, http method calling
        :param bce_version: str, bce_version like `bce-auth-v1`
        :returns: signature string
        :rtype: string

        """

        key = BasicBCESigner._gen_signing_key(access_key, secret_key,
                                              timestamp, expire_time,
                                              bce_version)
        host, path = parse_host_path_from(url)
        signature = BasicBCESigner._gen_signature(key,
                                                  path, method, host)
        return '/'.join([bce_version,
                         access_key,
                         timestamp,
                         expire_time,
                         'host',
                         signature])

    @staticmethod
    def _gen_signature(key, path, method, host):
        """Gen signature.

        :param key: str, signing key
        :param path: str, api endpoint
        :param method: str, method calling
        :param host: str, api host root
        :returns: hexdigest
        :rtype: string

        """
        to_sign = '\n'.join([method,  # as Upper
                             path,  # example '/openapi/gettasklist'
                             '',  # all method for yuqing is POST
                             'host:' + host])
        # hmac.new requires bytes
        signed = hmac.new(
            key.encode('utf-8'),
            to_sign.encode('utf-8'),
            hashlib.sha256).hexdigest()
        return signed

    @staticmethod
    def _gen_signing_key(access_key, secret_key,
                         timestamp, expire_time,
                         bce_version):
        """Gen signing key.

        :param access_key: str, baidu AK
        :param secret_key: str, baidu SK
        :param timestamp: str, timestamp
        :param expire_time: str, expire_time as string
        :param bce_version: str, bce_version, like `bce-auth-v1`
        :returns: signing key
        :rtype: string

        """
        to_sign = '/'.join([
            bce_version,
            access_key,
            timestamp,
            expire_time])
        signed = hmac.new(
            secret_key.encode('utf-8'),
            to_sign.encode('utf-8'),
            hashlib.sha256).hexdigest()
        return signed


class SimpleAuth:
    """Class for simple authorization.
    """
    secrets_file_path = 'secrets.json'

    def __init__(self):
        """Init from a secrest json.

        :param file_path: where secrets store

        """
        self.reload_secrets()

    def reload_secrets(self):
        """Reload secrets.
        """
        secrets = load_secrets(self.secrets_file_path)
        self.access_key = secrets['access_key']
        self.secret_key = secrets['secret_key']
        self.user_key = self.api_key = secrets['api_key']
        self.user_secret = self.api_secret = secrets['api_secret']

    def gen_authorization(self, url, method='POST'):
        """Generate authorization string

        :param url: str, url calling
        :param method: str, method calling
        :returns: authorization string
        :rtype: string

        """
        bce_signer = BasicBCESigner(self.access_key,
                                    self.secret_key,
                                    url,
                                    method)
        return bce_signer.gen()

    def gen_timestamp_token(self):
        """Generate timestamp and token

        :returns: (timestamp, token)
        :rtype: (string, string)

        """
        timestamp, token = get_yuqing_token_now(self.api_secret,
                                                self.api_key)
        return timestamp, token

    def gen_payload_template(self):
        """Generate payload template.

        :returns: payload template
        :rtype: dict

        """
        timestamp, token = self.gen_timestamp_token()
        return {'user_key': self.user_key,
                'token': token,
                'timestamp': timestamp}

    def gen_headers(self, url, method='POST'):
        """Generate headers

        :param url: str, url calling
        :param method: str, method calling
        :returns: headers with authorization
        :rtype: dict

        """
        host, _ = parse_host_path_from(url)
        authorization = self.gen_authorization(url, method)
        headers = {'Host': host,
                   'Content-Type': 'application/x-www-form-urlencoded',
                   'Authorization': authorization,
                   'Accept': '*/*'}
        return headers

    def gen(self, url, method='POST'):
        """FIXME! briefly describe function

        :param url: str, url calling
        :param method: str, method calling
        :returns: (payload_template, headers)
        :rtype: (dict, dict)

        """
        headers = self.gen_headers(url, method)
        payload = self.gen_payload_template()
        return payload, headers
