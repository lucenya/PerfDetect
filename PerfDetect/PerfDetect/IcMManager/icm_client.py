#!/usr/bin/python
# encoding: utf-8

"""
Simple Fire-and-Forget ICM API wrapper for Python.
"""

import json
import logging
import requests
import xml.etree.ElementTree
from uuid import uuid1
from datetime import datetime
from xml.sax.saxutils import escape

__author__ = 'Mario Mett <mmett@microsoft.com>'
__version__ = '0.5.0'

__all__ = ['ICMApi', 'ICMError', 'new_incident', 'create_incident', 'update_incident',
           'get_incident', 'get_incidents', 'get_oncall', 'edit_relation']

module_logger = logging.getLogger('ICM-API')


class ICMError(Exception):
    def __init__(self, msg, code=''):
        self.msg = msg
        self.code = code

    def __str__(self):
        if self.code:
            return '%s: %s' % (self.code, self.msg)
        else:
            return self.msg


def _xml_envelope():
    """
    XML envelope header.
    """
    return """<?xml version="1.0" encoding="UTF-8"?>
<s:Envelope xmlns:s="http://www.w3.org/2003/05/soap-envelope" xmlns:a="http://www.w3.org/2005/08/addressing">
   <s:Header>
      <a:Action s:mustUnderstand="1">http://tempuri.org/IConnectorIncidentManager/AddOrUpdateIncident2</a:Action>
      <a:MessageID>urn:uuid:{message_id}</a:MessageID>
      <a:To s:mustUnderstand="1">https://icm.ad.msoppe.msft.net/Connector3/ConnectorIncidentManager.svc</a:To>
   </s:Header>
   <s:Body>
      <AddOrUpdateIncident2 xmlns="http://tempuri.org/">
         <connectorId>{connector_id}</connectorId>
         <incident xmlns:b="http://schemas.datacontract.org/2004/07/Microsoft.AzureAd.Icm.Types" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">
{incident_content}
         </incident>
         <routingOptions>{routing_options}</routingOptions>
      </AddOrUpdateIncident2>
   </s:Body>
</s:Envelope>"""


def envelope_dictionary():
    """
    Initial incident XML structure as dictionary.
    """
    return {'CommitDate': None,
            'Component': None,
            'CorrelationId': 'NONE://Default',
            'CustomFields': None,
            'CustomerName': None,
            'Description': None,
            'DescriptionEntries': [{
                'DescriptionEntry': {
                    'Cause': 'Other',
                    'ChangedBy': None,
                    'Date': '$now$',
                    'DescriptionEntryId': 0,
                    'RenderType': 'Html',
                    'SubmitDate': '$now$',
                    'SubmittedBy': None,
                    'Text': 'Required'}}],
            'ExtendedData': None,
            'HowFixed': None,
            'ImpactStartDate': None,
            'ImpactedServices': None,
            'ImpactedTeams': None,
            'IncidentSubType': None,
            'IncidentType': None,
            'IsCustomerImpacting': None,
            'IsNoise': None,
            'IsSecurityRisk': None,
            'Keywords': None,
            'MitigatedDate': None,
            'Mitigation': None,
            'MonitorId': 'NONE://Default',
            'OccurringLocation': {
                'DataCenter': None,
                'DeviceGroup': None,
                'DeviceName': None,
                'Environment': None,
                'ServiceInstanceId': None},
            'OwningAlias': None,
            'OwningContactFullName': None,
            'RaisingLocation': {
                'DataCenter': None,
                'DeviceGroup': None,
                'DeviceName': None,
                'Environment': None,
                'ServiceInstanceId': None},
            'ReproSteps': None,
            'ResolutionDate': None,
            'RoutingId': 'NONE://Default',
            'ServiceResponsible': None,
            'Severity': 3,
            'Source': {
                'CreateDate': '$now$',
                'CreatedBy': 'Monitor',
                'IncidentId': '$uuid$',
                'ModifiedDate': '$now$',
                'Origin': 'Monitor',
                'Revision': None,
                'SourceId': '00000000-0000-0000-0000-000000000000'},
            'Status': 'Active',
            'SubscriptionId': None,
            'SupportTicketId': None,
            'Title': 'Required',
            'TrackingTeams': None,
            'TsgId': None,
            'TsgOutput': None,
            'ValueSpecifiedFields': 'None'}


class ICMApi(object):
    def __init__(self, icm_host, cert, key, connector_id=None, debug=False):
        """
        Initiate ICM API.
        :param icm_host:        ICM URL
        :param cert:            Certificate file location
        :param key:             Key file location
        :param connector_id:    Default connector ID
        :param debug:           True if in debug mode (more logging)
        """

        self.base_incident = envelope_dictionary()
        self.icm_host = icm_host
        self.cert = cert
        self.key = key
        self.connector_id = connector_id
        self.debug = debug

        self.headers = {'Host': self.icm_host,
                        'Expect': '100-continue'}
        self.wsdl = 'https://' + self.icm_host + '/Connector3/ConnectorIncidentManager.svc?wsdl'
        self.xmlns = 'http://schemas.datacontract.org/2004/07/Microsoft.AzureAd.Icm.Types'
        self.incidents = 'https://' + self.icm_host + '/api/cert/incidents({incident_id})'
        self.incidents_q = 'https://' + self.icm_host + '/api/cert/incidents?{query}'
        self.oncall_q = 'https://' + self.icm_host + '/api/cert/oncall/{collection}?{query}'

    def new_incident(self):
        """
        Returns empty incident dictionary.
        """
        return self.base_incident

    def create_incident(self, incident, connector_id=None, routing_options='None'):
        """
        Create incident in ICM.
        :param incident:            Incident body
        :param connector_id:        Optionally connector ID
        :param routing_options:     Routing options
        :return:                    Tuple with incident ID and performed action
        """

        if not connector_id:
            connector_id = self.connector_id

        field_mapping = {'message_id': str(uuid1()),
                         'connector_id': connector_id,
                         'incident_content': self._dictionary_to_xml(incident),
                         'routing_options': routing_options}

        for k, v in field_mapping.items():
            field_mapping[k] = v
        data = _xml_envelope().format(**field_mapping)

        self.headers['Content-type'] = 'application/soap+xml; charset=utf-8'
        response = self._make_request(method='POST', url=self.wsdl, data=data)

        try:
            tree = xml.etree.ElementTree.fromstring(response)
            incident_id = tree.find('.//{' + self.xmlns + '}IncidentId').text
            performed_action = tree.find('.//{' + self.xmlns + '}Status').text
            return_value = (incident_id, performed_action)
            return return_value
        except AttributeError:
            raise ICMError(response)

    def update_incident(self, incident_id, body, entity=None, method=None):
        """
        Update incident and incident entities.
        :param incident_id:     Incident ID
        :param body:            Request body in JSON
        :param entity:          Incident entity
        :param method:          Method to use on the API. Default is PATCH, if entity is provided,
                                default is POST.
        :return:                Empty string when successful
        """

        if not method:
            use_method = 'PATCH'
        else:
            use_method = method

        self.headers['Content-type'] = 'application/json; charset=utf-8'
        url = self.incidents.format(incident_id=str(incident_id))
        if entity:
            url += '/' + entity
            if not method:
                use_method = 'POST'

        if use_method.lower() == 'post':
            return self._make_request(method='POST', url=url, data=json.dumps(body))
        elif use_method.lower() == 'patch':
            return self._make_request(method='PATCH', url=url, data=json.dumps(body))
        else:
            raise ICMError('Method not supported')

    # noinspection PyTypeChecker
    def get_incident(self, incident_id, entity=None):
        """
        Get single incident.
        :param incident_id:     Incident ID
        :param entity:          Incident entity
        :return:                Dictionary with incident details
        """

        url = self.incidents.format(incident_id=str(incident_id))
        if entity:
            url += '/' + entity
        response = self._make_request(method='GET', url=url)
        if type(response) is dict:
            if 'CustomFieldGroups' in response:
                for group in response['CustomFieldGroups']:
                    for field in group['CustomFields']:
                        response[field['Name']] = field['Value']
        return response

    # noinspection PyTypeChecker
    def get_incidents(self, query, entity=None):
        """
        Get multiple incidents and search based on query.
        :param query:   Search query
        :param entity:  Entity to query from
        :return:        List of incidents as dictionary objects
        """

        self.headers['Content-type'] = 'application/json; charset=utf-8'
        url = self.incidents_q.format(query=str(query.replace(' ', '+')))
        if entity:
            url += '/' + entity

        result = []
        while True:
            response = self._make_request(method='GET', url=url)
            if type(response) is not dict:
                return response
            result += response['value']
            if 'odata.nextLink' not in response:
                return result
            url = response['odata.nextLink']

    # noinspection PyTypeChecker
    def get_oncall(self, collection, query=None):
        """
        Query against OnCall API collections.
        :param collection:  'currentoncall', 'contacts', 'tenants', 'tenantsilos' or 'teams'
        :param query:       Search query string
        :return:            Dictionary with response from API
        """

        collections = ['currentoncall', 'contacts', 'tenants', 'tenantsilos', 'teams']
        if collection not in collections:
            raise ICMError('Collection not supported')

        self.headers['Content-type'] = 'application/json; charset=utf-8'
        if query:
            url = self.oncall_q.format(collection=collection, query=str(query.replace(' ', '+')))
        else:
            url = self.oncall_q.format(collection=collection, query='')[:-1]

        result = []
        while True:
            response = self._make_request(method='GET', url=url)
            if type(response) is not dict:
                return response
            result += response['value']
            if 'odata.nextLink' not in response:
                return result
            url = response['odata.nextLink']

    def edit_relation(self, action, incident_id, relation_type, incident_id2='0'):
        """
        Add or remove incident relationships.
        :param action:          'add' relationship or 'delete' relationship
        :param incident_id:     First incident ID
        :param relation_type:   Relationship type. 'child', 'parent' or 'related'
        :param incident_id2:    Second incident ID
        :return:                Empty string if successful
        """

        if action == 'add':
            self.headers['Content-type'] = 'application/json; charset=utf-8'
            method = 'POST'
            body = {'url': self.incidents.format(incident_id=str(incident_id + 'L'))}
        elif action == 'remove':
            method = 'DELETE'
            body = None
        else:
            raise ICMError('Action not supported')

        url = self.incidents.format(incident_id=str(incident_id))
        if relation_type == 'child':
            url += '/$links/ChildIncidents'
            if action == 'remove':
                url += '(%s)' % incident_id2
        elif relation_type == 'parent':
            url += '/$links/ParentIncident'
        elif relation_type == 'related':
            url += '/$links/RelatedIncidents'
            if action == 'remove':
                url += '(%s)' % incident_id2
        else:
            raise ICMError('Type not supported')

        return self._make_request(method=method, url=url, data=json.dumps(body))

    def _make_request(self, method, url, data=None):
        """
        Creates request to ICM API and returns response content.
        """

        logging.debug('Request: %s:%s' % (method, url))
        if self.debug:
            logging.debug('Request content: %s' % str(data))
            logging.debug('Request headers: %s' % str(self.headers))

        try:
            if method == 'POST':
                response = requests.post(url=url, cert=(self.cert, self.key),
                                         headers=self.headers, data=data, timeout=10)
            elif method == 'GET':
                response = requests.get(url=url, cert=(self.cert, self.key),
                                        headers=self.headers, timeout=10)
            elif method == 'PATCH':
                response = requests.patch(url=url, cert=(self.cert, self.key),
                                          headers=self.headers, data=data, timeout=10)
            elif method == 'DELETE':
                response = requests.delete(url=url, headers=self.headers, timeout=10)
            else:
                raise ICMError('Method not supported')
        except requests.ConnectionError as e:
            raise ICMError(e.message)
        except requests.Timeout:
            raise ICMError('Timeout')

        logging.debug('Response status: %s' % response.status_code)
        if self.debug:
            logging.debug('Response content: %s' % response.text)
            logging.debug('Response headers: %s' % str(response.headers))

        response_content = response.text
        if 'Content-Type' in response.headers:
            if 'application/json;' in response.headers['Content-Type']:
                response_content = response.json()

        if response.status_code >= 300:
            raise ICMError(response_content, response.status_code)

        return response_content

    def _dictionary_to_xml(self, dictionary, indent=12, ns='b:', ws='\n'):
        """
        Converts incident dictionary to XML string.
        """

        out_xml = ''
        _indent = ' ' * indent

        key_o = '<{ns}{key}>'.format(ns=ns, key='{key}')
        key_c = '</{ns}{key}>'.format(ns=ns, key='{key}') + ws

        for key, value in sorted(dictionary.items()):
            if type(value) is dict:
                out_xml += _indent + key_o.format(key=key) + ws
                out_xml += self._dictionary_to_xml(value, indent + 3) + ws
                out_xml += _indent + key_c.format(key=key)
            elif type(value) is list:
                out_xml += _indent + key_o.format(key=key) + ws
                for item in value:
                    out_xml += self._dictionary_to_xml(item, indent + 3) + ws
                out_xml += _indent + key_c.format(key=key)
            elif type(value) is bool:
                if value:
                    out_xml += _indent + key_o.format(key=key) + 'true' + key_c.format(key=key)
                else:
                    out_xml += _indent + key_o.format(key=key) + 'false' + key_c.format(key=key)
            else:
                if value or type(value) is int:
                    if value == '$now$':
                        _now = str(datetime.utcnow().isoformat())
                        out_xml += _indent + key_o.format(key=key) + _now + key_c.format(key=key)
                    elif value == '$uuid$':
                        _uuid = str(uuid1())
                        out_xml += _indent + key_o.format(key=key) + _uuid + key_c.format(key=key)
                    else:
                        _value = escape(str(value))
                        out_xml += _indent + key_o.format(key=key) + _value + key_c.format(key=key)
                else:
                    out_xml += _indent + '<' + ns + key + ' i:nil="true" />' + ws
        return out_xml[:-1]


if __name__ == '__main__':
    print('This file should not be executed.')
