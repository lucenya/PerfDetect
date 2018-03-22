#!/usr/bin/python
# encoding: utf-8

# Example script to query tenant details.

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

# Example to get single tenant details. Remove query to get all tenants in ICM.
result = icm_api.get_oncall(collection='tenants', query="$filter=Name eq 'VIRO'")

print(result)
