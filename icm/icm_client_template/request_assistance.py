#!/usr/bin/python
# encoding: utf-8

# Example script to request assistance.

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

# Requesting assistance from a contact
body = {'RequestAssistanceParameters': {
    'RequesterContactAlias': 'alias',
    'TargetContactAlias': 'alias',
    'RequestDescription': 'Requesting assistance'}}

request1 = icm_api.update_incident(incident_id='TICKET_ID', body=body, entity='RequestAssistance')
print(request1)

# Requesting assistance from a team​.
body = {'RequestAssistanceParameters': {
    'RequesterContactAlias': 'alias',
    'TargetTeamPublicId': 'TestService\TestTeam',
    'RequestDescription': 'Requesting assistance'}}

request2 = icm_api.update_incident(incident_id='TICKET_ID', body=body, entity='RequestAssistance')
print(request2)
