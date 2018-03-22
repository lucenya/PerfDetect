#!/usr/bin/python
# encoding: utf-8

# Example script to add attachment to incident.

import icm
import logging
import base64

logging.basicConfig(format='%(asctime)s.%(msecs)-3d UTC - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)

import credentials
host = credentials.host
cert = credentials.cert
key = credentials.key
connector_id = credentials.connector_id

icm_api = icm.ICMApi(icm_host=host, cert=cert, key=key, connector_id=connector_id, debug=True)

filename = 'attachment.txt'

with open(filename, 'rb') as attachment_file:
    content = base64.b64encode(attachment_file.read())

body = {'Attachment': {'Filename': filename, 'ContentsBase64': content}}

incident = icm_api.update_incident(incident_id='TICKET_ID', body=body, entity='CreateAttachment')

print(incident)
