from proteus import config

from os import environ
import logging

"""
Configuration of DHIS2 server API
"""
api_url = environ.get('DHIS2_API_URL')


# Connection to gnuhealth server
def connect_to_gnu():
    username = environ.get('GNUHEALTH_USERNAME')
    password = environ.get('GNUHEALTH_PASSWORD')
    dbname = environ.get('GNUHEALTH_DBNAME')
    hostname = environ.get('GNUHEALTH_HOSTNAME')
    port = environ.get('GNUHEALTH_PORT')

    health_server = 'http://' + username + ':' + password + '@' + hostname + ':' + port + '/' + dbname + '/'
    logging.info(f"trying to connect to {health_server}")

    try:
        config.set_xmlrpc(health_server)
        logging.info(f"connection established successfully with {health_server}")
    except Exception as e:
        logging.error(f"connection failed: {e}")
