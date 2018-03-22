#!/usr/bin/python
# encoding: utf-8

# Example script to create incident in ICM.

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

# Initializing new incident
incident = icm_api.new_incident()

# Setting incident description, title and severity
incident['DescriptionEntries'][0]['DescriptionEntry']['Text'] = 'Example description'
incident['Title'] = "Example title"
incident['Severity'] = 4

# Creating incident in ICM
result = icm_api.create_incident(incident=incident)

print(result)
