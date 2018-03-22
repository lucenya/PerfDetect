#!/usr/bin/python
# encoding: utf-8

# Example script to get incident details from ICM.

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

# Get incident
incident = icm_api.get_incident(incident_id='TICKET_ID')
print(incident)

# Get description entries
entries = icm_api.get_incident(incident_id='TICKET_ID', entity='DescriptionEntries')
print(entries)

# Get incident parent
parent = icm_api.get_incident(incident_id='TICKET_ID', entity='ParentIncident')
print(parent)

# Get incident children
children = icm_api.get_incident(incident_id='TICKET_ID', entity='ChildIncidents')
print(children)

# Get related incidents
related = icm_api.get_incident(incident_id='TICKET_ID', entity='RelatedIncidents')
print(related)

# Get external incident links
external = icm_api.get_incident(incident_id='TICKET_ID', entity='ExternalIncidents')
print(external)
