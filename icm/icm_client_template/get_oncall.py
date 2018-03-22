#!/usr/bin/python
# encoding: utf-8

# Example script to query all on-call schedules.

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

# Add team ID filter to get on-call list for specific team.
result = icm_api.get_oncall(collection='currentoncall')

print(result)
