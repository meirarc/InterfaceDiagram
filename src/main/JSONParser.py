import logging
from typing import List, Dict

class JSONParser:
    @staticmethod
    def json_to_object(data: List[Dict]) -> List[Dict]:
        logging.info(f'json_to_object()')

        interfaces = {}
        for row in data:
            code_id = row['code_id']
            if code_id not in interfaces:
                interfaces[code_id] = {'code_id': code_id, 'direction': row['direction'], 'apps': []}
            app = {row['app_type']: row['app_name'], 'format': row['format']}
            if row['connection_app']:
                connection = {'app': row['connection_app'], 'detail': row['connection_detail']}
                if row['interface_id']:
                    connection['interface'] = {'id': row['interface_id'], 'url': row['interface_url']}
                app['connection'] = connection
            interfaces[code_id]['apps'].append(app)
        return list(interfaces.values())


