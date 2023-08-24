"""
This module provides functionalities to parse JSON data.
"""
import logging
from typing import List, Dict
import json


class JSONParser:
    """
    A class to parse JSON data.
    """
    @staticmethod
    def json_to_object(data: List[Dict]) -> List[Dict]:
        """
        Transform JSON to a formatted object.

        :param data: List of dictionaries representing the JSON data.
        :return: List of dictionaries representing the transformed data.
        """
        logging.info('json_to_object()')

        interfaces = {}
        for row in data:
            code_id = row['code_id']

            if code_id not in interfaces:
                interfaces[code_id] = {
                    'code_id': code_id,
                    'direction': row['direction'],
                    'apps': []
                }

            app = {row['app_type']: row['app_name'], 'format': row['format']}
            if row['connection_app']:
                connection = {'app': row['connection_app'],
                              'detail': row['connection_detail']}

                if row['interface_id']:
                    connection['interface'] = {
                        'id': row['interface_id'],
                        'url': row['interface_url']
                    }

                app['connection'] = connection
            interfaces[code_id]['apps'].append(app)
        return list(interfaces.values())

    def parse(self, data):
        """
        Parse the given JSON data.

        :param data: JSON data to be parsed
        :return: Parsed data
        """
        return json.loads(data)

    def dumps(self, data):
        """
        Dumps the given JSON data.

        :param data: JSON data to be parsed
        :return: Dumps data
        """
        return json.dumps(data)
