#!/usr/bin/python
# encoding: utf-8

# Example script to transfer incident.

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

body = {'TransferParameters': {
    'OwningTenantPublicId': 'e3386e8a-24fc-4a7f-a6cf-dfa02b927cxx',
    'OwningTeamPublicId': 'TestService\TestTeam',
    'Description': {'Text': 'Demo', 'RenderType': 'Plaintext', 'ChangedBy': 'alias'}}}

incident = icm_api.update_incident(incident_id='TICKET_ID', body=body, entity='TransferIncident')

print(incident)
