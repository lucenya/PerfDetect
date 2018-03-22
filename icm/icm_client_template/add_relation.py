#!/usr/bin/python
# encoding: utf-8

# Example script to add relations to incidents.

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

# Adding incident_id2 as a child of incident_id
result1 = icm_api.edit_relation(action='add', incident_id='TICKET_ID', relation_type='child', incident_id2='TICKET_ID')
print(result1)

# Adding incident_id2 as a parent of incident_id
result2 = icm_api.edit_relation(action='add', incident_id='TICKET_ID', relation_type='parent', incident_id2='TICKET_ID')
print(result2)

# Adding incident_id2 as related to incident_id
result3 = icm_api.edit_relation(action='add', incident_id='TICKET_ID', relation_type='related', incident_id2='TICKET_ID')
print(result3)
