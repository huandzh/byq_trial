#! -*- coding:utf-8 -*-
"""API calls for yuqing

.. moduleauthor:: Huan Di <hd@iamhd.top>

"""
import requests
from byq_trial.auth import SimpleAuth


class APICall:
    """API Call for yuqing service
    """
    api_root = 'http://yuqing.baidu.com'

    def __init__(self, uri, auth, method='POST'):
        """Init call.

        :param auth: auth using
        :param uri: uri in docs
        :param payload: extra params other than shared
        :param method: method calling

        .. notes:: only `SimpleAuth` is implemented.

        """
        self.auth = auth
        if not isinstance(self.auth, SimpleAuth):
            raise NotImplementedError(
                'Authorization other than `SimpleAuth` is not implemented')
        self.uri = uri
        self.url = self.api_root + self.uri
        self.method = method
        # init headers and payload_template
        self.regen_headers()
        self.regen_payload_template()
        # init
        self.last_response = None

    def regen_headers(self):
        """Regenerate headers.
        """
        self.headers = self.auth.gen_headers(self.url)

    def regen_payload_template(self):
        """Regenerate payload_template.

        A payload_template contains `user_key`, `token` and `timestamp`.
        """
        self.payload_template = self.auth.gen_payload_template()

    def call(self, payload):
        """Call API.

        :param payload:

        """
        payload_template = self.payload_template.copy()
        if self.method == 'POST':
            for k, v in payload.items():
                payload_template.setdefault(k, v)
            response = requests.post(self.url,
                                     data=payload_template,
                                     headers=self.headers)
            self.last_response = response
            return response

    def json(self):
        """Return json of last response.

        :returns: json of last_response
        :rtype: json dict

        """

        if self.last_response is None:
            return None
        else:
            return self.last_response.json()