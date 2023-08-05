#!/usr/bin/env python
import unittest
import logging
import json

from vmwvro2.workflow import Workflow,WorkflowRun
from vmwvro2.sessions import SessionList
from vmwvro2.settings import ConfigVMWvro
from vmwvro2.utils import safeget

logging.basicConfig(level=logging.DEBUG)


#sl = SessionList()
#s = sl.getSession()



class LoadConfig(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("setup")
        ConfigVMWvro()
        print("2nd")
        ConfigVMWvro()

    def test_config_credentials(self):
        credentials = ConfigVMWvro.credentials
        self.assertIsNotNone(credentials)

    def test_config_redirect(self):
        """
        vro-links:
            redirect: False
        """
        redirect = safeget(ConfigVMWvro.config,"vro-links","redirect")
        self.assertIsNotNone(redirect)
 

    def test_config_config(self):
        config = ConfigVMWvro.config
        self.assertIsNotNone(config)
        print(config)

    def test_session(self):
        sl = SessionList()

        
            
if __name__ == '__main__':
    unittest.main()

