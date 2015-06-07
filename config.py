__author__ = 'christopher'

import ConfigParser
import runtime
import logger




def create_config():
    config = ConfigParser.RawConfigParser()
    config.add_section('Configuration')
    config.set('Configuration', 'host', 'localhost')
    config.set('Configuration', 'port', '81')
    config.set('Configuration', 'password', 'changeme')
    config.set('Configuration', 'motd', '')
    config.set('Configuration', 'gui', 'false')
    config.set('Configuration', 'server', 'true')
    config.set('Configuration', 'verbose', 'false')
    config.set('Configuration', 'debug', 'false')
    config.set('Configuration', 'drop_claim_radius', '20')
    with open('config.cfg', 'wb') as configfile:
        config.write(configfile)

def read_config():
    config = ConfigParser.RawConfigParser()
    config.read('config.cfg')
    runtime.host = config.get('Configuration', 'host')
    runtime.port = config.get('Configuration', 'port')
    runtime.password = config.get('Configuration', 'password')
    runtime.motd = config.get('Configuration', 'motd')
    runtime.gui = config.getboolean('Configuration', 'gui')
    runtime.server = config.getboolean('Configuration', 'server')
    runtime.verbose = config.getboolean('Configuration', 'verbose')
    runtime.debug = config.getboolean('Configuration', 'debug')
    runtime.drop_claim_radius = config.get('Configuration', 'drop_claim_radius')

def save_config():
    config = ConfigParser.RawConfigParser()
    config.add_section('Configuration')
    config.set('Configuration', 'host',runtime.host)
    config.set('Configuration', 'port', runtime.port)
    config.set('Configuration', 'password', runtime.password)
    config.set('Configuration', 'motd', runtime.motd)
    config.set('Configuration', 'gui', runtime.gui)
    config.set('Configuration', 'server', runtime.server)
    config.set('Configuration', 'verbose', runtime.verbose)
    config.set('Configuration', 'debug', runtime.debug)
    config.set('Configuration', 'drop_claim_radius', runtime.drop_claim_radius)
    with open('config.cfg', 'wb') as configfile:
        config.write(configfile)

try:
    with open('config.cfg') as file:
        read_config()
except IOError as e:
    logger.log_debug("No config file, so one is being created")
    logger.log_debug("Pleas edit the config file and try again")
    create_config()