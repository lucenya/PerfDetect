#!/usr/bin/python
# encoding: utf-8

# Example script to create, get and update root cause.

import icm
import logging

logging.basicConfig(format='%(asctime)s.%(msecs)-3d UTC - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)

import credentials
host = credentials.host
cert = credentials.cert
key = credentials.key
connector_id = credentials.connector_id

icm_api = icm.ICMApi(icm_host=host, cert=cert, key=key, connector_id=connector_id, debug=True)

# Create root cause
body = {'Category': 'Other',
        'Description': 'Description for your root cause',
        'Title': 'The title to use for your root cause',
        'Bugs': [
            {'BugId': '12345',
             'BugSource': 'TFS',
             'BugType': 'Detection'}]}

root_cause1 = icm_api.update_incident(incident_id='TICKET_ID', body=body, entity='RootCause')
print(root_cause1)

# Get root cause
root_cause2 = icm_api.get_incident(incident_id='TICKET_ID', entity='RootCause')
print(root_cause2)

# Update root cause
body = {'Category': 'Other',
        'Description': 'Description for your root cause',
        'Title': 'The title to use for your root cause'}
root_cause3 = icm_api.update_incident(incident_id='TICKET_ID', body=body, entity='RootCause')
print(root_cause3)
