#!/usr/bin/python
# encoding: utf-8

# Example script to remove incident relationships.

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

# Breaking the correlation between parent incident incident_id and child incident incident_id2.
result1 = icm_api.edit_relation(action='remove', incident_id='TICKET_ID', relation_type='child', incident_id2='TICKET_ID')
print(result1)

# Removing parent incident.
result2 = icm_api.edit_relation(action='remove', incident_id='TICKET_ID', relation_type='parent')
print(result2)

# Removing relationship between two incidents.
result3 = icm_api.edit_relation(action='remove', incident_id='TICKET_ID', relation_type='relation', incident_id2='TICKET_ID')
print(result3)
