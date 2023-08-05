#!/usr/bin/env python
import unittest
import logging

from vmwvro2.utils import url_host_replace
import json

logging.basicConfig(level=logging.DEBUG)



class Utils(unittest.TestCase):


    def test_ulr_host_replace_01(self):
        url = "https://cidedevvro11.admnet.vodafone.com:8281/vco/api/workflows/1d8c12ce-a551-4a03-aa54-2165f9a0f525/executions/ff8080816403837c0164ec4b24636c34/state/"
        newhost = "http://localhost:8888"

        result = url_host_replace(url, newhost)

        self.assertRegex(result, r'^http://localhost:8888/')


    def test_ulr_host_replace_02(self):
        url = "https://cidedevvro11.admnet.vodafone.com:8281/vco/api/workflows/1d8c12ce-a551-4a03-aa54-2165f9a0f525/executions/ff8080816403837c0164ec4b24636c34/state/"
        newhost = "localhost:8888"

        result = url_host_replace(url, newhost)

        self.assertRegex(result, r'^https://localhost:8888/')


            
if __name__ == '__main__':
    unittest.main()

