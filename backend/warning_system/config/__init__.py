from proteus import config

from os import environ
import logging

"""
Configuration of DHIS2 server API
"""
api_url = environ.get('DHIS2_API_URL')


# Connection to gnuhealth server
def connect_to_gnu(user='admin',
                   password='opendx28',
                   dbname='ghs1',
                   hostname='localhost',
                   port='8000'):

    health_server = 'http://' + user + ':' + password + '@' + hostname + ':' + port + '/' + dbname + '/'
    logging.info(f"trying to connect to {health_server}")
    conf = config.set_xmlrpc(health_server)
    logging.info(f"connected to conf")

    return conf

