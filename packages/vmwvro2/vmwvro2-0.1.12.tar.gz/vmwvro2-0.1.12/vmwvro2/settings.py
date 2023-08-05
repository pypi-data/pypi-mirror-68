"""
Manage configuration and credentials file
"""

import logging
import os
import yaml
import sys

from vmwvro2.config import VRO_CONFIG_FILE, VRO_CREDENTIALS_FILE



logger = logging.getLogger(__name__)
#logger.setLevel(logging.INFO)
logger.setLevel(logging.DEBUG)



class ConfigVMWvro:

    config = None
    credentials = None

    @classmethod
    def __init__(cls, path=None, config=None, redis=None):

        if config:
            cls.config = config
            return

        cls.load(path)    

        if redis:
            if not cls.config.get('cache'):
                cls.config['cache'] = {}

            cls.config['cache']['redis'] = redis


    @classmethod
    def load(cls, path=None):

        if cls.config:
            return 

        #Read config/credentials files
        #path = ".secrets/vro-credentials.yml"
        #dirname = os.path.expanduser("~")
        #configFile = os.path.join(dirname, path)
        #configFile = "/etc/vmwvro2/vro-credentials.yml"
        configFile = VRO_CREDENTIALS_FILE

        # Get credentias from file
        logger.debug("Reading credentias from %s",configFile)
        cls.credentials = {}
        try:
            with open(configFile, 'r') as stream:
                cls.credentials = yaml.load(stream, Loader=yaml.FullLoader)
        except:
            exc = sys.exc_info()[0]
            logger.warning(exc)



        #Read vmwvro2 from file
        cls.config = {}

        configFile = VRO_CONFIG_FILE
        logger.debug("Reading config from %s",configFile)

        try:
            with open(configFile, 'r') as stream:
                cls.config = yaml.load(stream, Loader=yaml.FullLoader)
        except:
            exc = sys.exc_info()[0]
            logger.error(exc)

