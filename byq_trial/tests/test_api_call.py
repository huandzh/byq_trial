#! -*- coding:utf-8 -*-
"""Tests for yuqing api calls

.. moduleauthor:: Huan Di <hd@iamhd.top>

"""

import unittest
from byq_trial import SimpleAuth, APICall


class APICallTest(unittest.TestCase):
    def setUp(self):
        SimpleAuth.secrets_file_path = 'secrets.json'
        self.auth = SimpleAuth()
        self.api_gettasklist = APICall('/openapi/gettasklist',
                                       auth=self.auth)

    def test_gettasklist(self):
        payload = {}
        res = self.api_gettasklist.call(payload)
        # api return results
        self.assertEqual(res.status_code, 200)
        res_json = res.json()
        # api return task list
        self.assertEqual(res_json['code'], 200)


if __name__ == '__main__':
    unittest.main()
