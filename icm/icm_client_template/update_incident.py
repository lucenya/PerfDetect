#!/usr/bin/python
# encoding: utf-8

# Example script to update incident.

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

# Updating ticket title and adding new description entry
body = {'Title': 'New title',
        'NewDescriptionEntry': {'Text': 'New description entry',
                                'RenderType': 'Plaintext'}}

result = icm_api.update_incident(incident_id='TICKET_ID', body=body)

print(result)
