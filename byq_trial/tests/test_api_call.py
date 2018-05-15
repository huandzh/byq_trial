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
        self.api_getresult = APICall('/openapi/getresult/',
                                     auth=self.auth)

    def test_gettasklist(self):
        payload = {}
        res = self.api_gettasklist.call(payload)
        # api return results
        self.assertEqual(res.status_code, 200)
        res_json = res.json()
        # api return task list
        self.assertEqual(res_json['code'], 200)

    def test_getresult_can_limit(self):
        size_n = 2
        one_task_id = "179139"  # a task id avaiable
        payload = {
            "api_type": "realtime_flow",
            "task_id": one_task_id,
            "params_dict": {
                "realtime_flow": {
                    "offset": "0",
                    "size": "%s" % size_n,
                    "insert_from": "20180510000000",
                    "insert_to": "20180511235959",
                    "media_type": "",
                    "sentiment_type": "",
                    "search_word": "",
                    "relate_type": "",
                    "province": "",
                    "city": "",
                    "county": ""
                }
            }
        }
        res = self.api_getresult.call(payload)
        self.assertEqual(res.status_code, 200)
        res_json = res.json()
        # api return result
        self.assertEqual(res_json['code'], 200)
        # params works : limit by 2
        self.assertEqual(len(res_json['data']['list']), size_n)


if __name__ == '__main__':
    unittest.main()
