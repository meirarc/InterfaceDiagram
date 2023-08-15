"""
This module defines the InterfaceDiagram class used to generate diagrams
from some input data.
"""
import xml.etree.ElementTree as ET
import logging
from typing import List, Dict, Tuple

from src.main.config import (
    # Constant fill colors
    FIRST_FILL_COLOR,                # Main system (that drives the interface direction) color
    MIDDLE_FILL_COLOR,               # Middlewares colors
    GATEWAY_FILL_COLOR,              # Gateway Colors
    OTHER_FILL_COLOR,                # Other Middleware colors
    LAST_FILL_COLOR,                 # Connected App colors
    CONNECTION_OUT_FILL_COLOR,       # Outbound Connection colors
    CONNECTION_IN_FILL_COLOR,        # Inbound Connection colors

    # Constant stroke colors
    FIRST_STROKE_COLOR,              # Main system (that drives the interface direction) color
    MIDDLE_STROKE_COLOR,             # Middlewares colors
    GATEWAY_STROKE_COLOR,            # Gateway Colors
    OTHER_STROKE_COLOR,              # Other Middleware colors
    LAST_STROKE_COLOR,               # Connected App colors
    CONNECTION_OUT_STROKE_COLOR,     # Outbound Connection colors
    CONNECTION_IN_STROKE_COLOR,      # Inbound Connection colors

    # Constant size parameters
    Y_OFFSET,                        # additional space between each protocol
    PROTOCOL_HEIGHT,                 # protocol height
    PROTOCOL_WIDTH,                  # protocol width
    APP_WIDTH,                       # application width

    # Constant for the app sequencing
    APP_TYPES                        # Types of applications in scope to the diagrams
)


class InterfaceDiagram:
    """
    Class to represent and generate an Interface Diagram.
    """
    def __init__(self, interfaces, encoder, log_level=logging.ERROR):
        logging.basicConfig(level=log_level)
        logging.info('Init Class InterfaceDiagram')

        # Configuration parameters
        self.config = {
            'interfaces': interfaces,  # Input File
            'encoder': encoder         # Encoder to write the out file
        }

        self.list_of_ids = []  # Control of ids

        # Sequencing of application
        self.app_lists = self.populate_app_lists(self.config['interfaces'])
        self.app_order, self.app_count = self.create_app_order(self.app_lists)

        # Variant size parameters as a dictionary
        self.size_parameters = {
            'y_protocol': 0,
            'y_protocol_start': 40,
            'app_height': 80 + (PROTOCOL_HEIGHT + Y_OFFSET) * (len(self.config['interfaces']) - 1),
            'page_width': ((self.app_count * 2) - 1) * APP_WIDTH
        }

        # Public xml content
        self.xml_content = {
            'mxfile': None,
            'root': None
        }


    def populate_app_lists(self, interfaces: List[Dict]) -> Dict[str, List[str]]:
        """
        Populate the interfaces object in separated objects by types.
        app_types = ['sap', 'middleware', 'gateway', 'connected_app'] 

        :param interfaces: The list of interfaces.
        :return: A dictionary where the keys are the app types and the values are the app names.
        """
        logging.info('populate_app_lists(%s)', interfaces)

        app_lists = {
            'sap_apps': [],
            'middlewares': [],
            'gateways': [],
            'other_middlewares':[],
            'connected_apps': []
        }

        for interface in interfaces:
            for app in interface['apps']:
                for app_type, app_names in app_lists.items():
                    if app_type[:-1] in app and app[app_type[:-1]] not in app_names:
                        app_names.append(app[app_type[:-1]])

        return app_lists


    def create_app_order(self, app_lists: Dict[str, List[str]]) -> Tuple[Dict[str, int], int]:
        """
        Define the sequence of the applications that will be displayed on the diagrams
        app_types = ['sap', 'middleware', 'gateway', 'connected_app'] 

        :param app_lists: A dictionary where keys are the app_types and values are the app_names.
        :return: A dictionary where the keys are the app names and the values are their orders.
        """
        logging.info('create_app_order()')

        app_list = (
            app_lists['sap_apps'] +
            app_lists['middlewares'] +
            app_lists['gateways'] +
            app_lists['other_middlewares'] +
            app_lists['connected_apps']
        )

        app_order = {app: i for i, app in enumerate(app_list)}
        return app_order, len(app_list)


    def initialize_xml_structure(self) -> None:
        """
        Create the initial elements of the XML file readable by draw.io
        The initial structure must need to contain the:
          mxfile, diagram, mxGraphModel, root, mxCell(0), mxCell(1)
        """
        logging.info('initialize_xml_structure()')

        self.xml_content['mxfile'] = ET.Element('mxfile', {'host': 'app.diagrams.net',
                                    'modified': '2023-07-25T12:42:08.179Z',
                                    'agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                        'AppleWebKit/537.36 (KHTML, like Gecko) '
                                        'Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.82'),
                                    'etag': '70Szxm5LCrq_Rskbk8Uq', 'version': '21.6.5',
                                    'type': 'device'})

        diagram = ET.SubElement(self.xml_content['mxfile'], 'diagram',
                                {'name': 'Page-1', 'id': 'xI1n7PUDQ-lDr-DjmP3Y'})

        page_width =  f'{self.size_parameters["page_width"]}'
        page_height = f'{self.size_parameters["app_height"]}'

        mx_graph_model = ET.SubElement(diagram, 'mxGraphModel', {'dx': '1182', 'dy': '916',
                                                        'grid': '1', 'gridSize': '10', 
                                                        'guides': '1', 'tooltips': '1', 
                                                        'connect': '1', 'arrows': '1', 'fold': '1',
                                                        'page': '1', 'pageScale': '1', 
                                                        'pageWidth': page_width,
                                                        'pageHeight': page_height, 
                                                        'math': '0', 'shadow': '0'})

        self.xml_content['root'] = ET.SubElement(mx_graph_model, 'root')
        ET.SubElement(self.xml_content['root'], 'mxCell', {'id': '0'})
        ET.SubElement(self.xml_content['root'], 'mxCell', {'id': '1', 'parent': '0'})


    def create_app(self, app_name: str, fill_color: str, stroke_color: str) -> None:
        """
        This method creates an application shape in the Draw.io diagram structure. 
        Each application shape is represented as an 'mxCell' XML element with specific attributes.
        
        :param app_name: The name of the application.
        :param fill_color: The color used to fill the shape.
        :param stroke_color: The color used for the outline of the shape.
        """
        logging.info('Creating app %s, fill_color: %s, stroke_color: %s',
                     app_name, fill_color, stroke_color)

        if app_name not in self.app_order:
            logging.error('App name %s is not in the app order.', app_name)
            return

        object_id = app_name
        # Ensure that each ID is unique
        if object_id not in self.list_of_ids:
            self.list_of_ids.append(object_id)
            # Create an 'mxCell' XML element for the application shape

            style = (f'rounded=1;whiteSpace=wrap;html=1;fillColor={fill_color};'
                     f'strokeColor={stroke_color};verticalAlign=top;')

            mx_cell = ET.SubElement(
                self.xml_content['root'],
                'mxCell',
                {
                    'id': object_id,
                    'value': app_name,
                    'style': style,
                    'parent': '1',
                    'vertex': '1'
                }
            )

            x_value = f'{APP_WIDTH * 2 * self.app_order[app_name]}'
            width_value = f'{APP_WIDTH}'
            height_value = str(self.size_parameters["app_height"])

            ET.SubElement(
                mx_cell,
                'mxGeometry',
                {
                    'x': x_value,
                    'y': '0',
                    'width': width_value,
                    'height': height_value,
                    'as': 'geometry'
                }
            )


    def create_protocol(self, protocol_config: dict) -> None:
        """
        This method creates a protocol shape in the Draw.io diagram structure. 
        Each application shape is represented as an 'mxCell' XML element with specific attributes.
        
        :param protocol_config: A dictionary containing the configuration for the protocol.
            Expected keys are:
                - 'app_name': The name of the application.
                - 'direction': Indicate an inbound or outbound flow, reference from SAP system.
                - 'row': The row to create the protocol
                - 'format': The text to be added inside the protocol shape
                - 'position': The position that the shape will be created on the diagram
        """
        app_name = protocol_config['app_name']
        direction = protocol_config['direction']
        row = protocol_config['row']
        app_format = protocol_config['format']
        position = protocol_config['position']

        logging.info('create_protocol(%s)',protocol_config)

        if app_name not in self.app_order:
            logging.error('App name %s is not in the app order.', app_name)
            return

        object_id = f'{direction}_{app_name}_{row}'
        # Ensure that each ID is unique
        if object_id not in self.list_of_ids:
            self.list_of_ids.append(object_id)

            # Create an 'mxCell' XML element for the protocol shape
            style = ('shape=delay;whiteSpace=wrap;html=1;fillColor=#eeeeee;'
                     'strokeColor=#36393d;rotation=0;fontSize=10;')

            mx_cell = ET.SubElement(self.xml_content['root'], 'mxCell', {
                'id': object_id, 
                'value': app_format, 
                'style': style, 
                'parent': '1', 
                'vertex': '1' 
            })

            ET.SubElement(mx_cell, 'mxGeometry', {
                'x': f'{position + (APP_WIDTH * 2 * self.app_order[app_name])}', 
                'y': f'{self.size_parameters["y_protocol"]}', 
                'width': f'{PROTOCOL_WIDTH}', 
                'height': f'{PROTOCOL_HEIGHT}', 
                'as': 'geometry' 
            })


    def create_connection(self, source:str, target:str, row:int, direction:str) -> None:
        """
        This method creates an connections in the Draw.io diagram structure. 
        Each application shape is represented as an 'mxCell' XML element with specific attributes.
        
        :param source: The name of the source application
        :param target: The name of the target application
        :param row: The row to create the protocol
        :param direction: indicate an inbound or outbouind flow, reference from SAP system.
        """
        logging.info('create_protocol(%s, %s, %s, %s)',source, target, row, direction)

        object_id = f'conn_{source}_{target}_{row}'
        # Ensure that each ID is unique
        if object_id not in self.list_of_ids:
            self.list_of_ids.append(object_id)

            # Define parameters based on the direction (Outbound/Inbound)
            fill_color = (CONNECTION_OUT_FILL_COLOR if direction == "Outbound"
                          else CONNECTION_IN_FILL_COLOR)
            stroke_color = (CONNECTION_OUT_STROKE_COLOR if direction == "Outbound"
                            else CONNECTION_IN_STROKE_COLOR)
            source_connection = (f'out_{source}_{row}' if direction == "Outbound"
                                 else f'in_{target}_{row}')
            target_connection = (f'in_{target}_{row}' if direction == "Outbound"
                                 else f'out_{source}_{row}')

            # Styles for the 'mxCell' XML element
            style = (f'edgeStyle=orthogonalEdgeStyle;rounded=0;fillColor={fill_color};'
                    f'strokeColor={stroke_color};orthogonalLoop=1;jettySize=auto;'
                    'html=1;strokeWidth=3')

            # Attributes for the 'mxCell' XML element
            mx_cell_attrs = {
                'id': object_id,
                'value': '',
                'invert': 'true',
                'style': style,
                'parent': '1',
                'edge': '1',
                'source': f'{source_connection}',
                'target': f'{target_connection}'
            }

            # Create an 'mxCell' XML element for the connections
            mx_cell = ET.SubElement(self.xml_content['root'], 'mxCell', mx_cell_attrs)

            # Attributes for the 'mxGeometry' XML element
            mx_geometry_attrs = {
                'relative': '1',
                'as': 'geometry'
            }

            # Create an 'mxGeometry' XML element for the connections
            ET.SubElement(mx_cell, 'mxGeometry', mx_geometry_attrs)


    def create_detail(self, detail_params: dict) -> None:
        """
        This method creates a label in the Draw.io diagram structure. 
        Each label is represented as an 'mxCell' XML element with specific attributes.
        
        :param detail_params: A dictionary containing the necessary parameters.
        """
        source = detail_params['source']
        target = detail_params['target']
        row = detail_params['row']
        text = detail_params['text']
        direction = detail_params['direction']

        logging.info('create_detail(%s, %s, %d, %s, %s)', source, target, row, text, direction)

        object_id = f'detail_{source}_{target}_{row}'

        # Ensure that each ID is unique
        if object_id not in self.list_of_ids:
            self.list_of_ids.append(object_id)

            style = 'text;html=1;strokeColor=none;fillColor=none;align=center;'\
                    'verticalAlign=middle;whiteSpace=wrap;rounded=0'

            x_position = 120 + (APP_WIDTH * 2) * self.app_order[source]

            # Create an 'mxCell' XML element for the text shape related to the detail
            mx_cell_attrs = {
                'id': object_id,
                'value': text,
                'style': style,
                'parent': '1',
                'vertex': '1'
            }

            mx_cell = ET.SubElement(self.xml_content['root'], 'mxCell', mx_cell_attrs)

            # Create an 'mxGeometry' XML element for the connections
            mx_geometry_attrs = {
                'x': str(x_position),
                'y': str(self.size_parameters["y_protocol"] - 20),
                'width': '120',
                'height': '30',
                'as': 'geometry'
            }

            ET.SubElement(mx_cell, 'mxGeometry', mx_geometry_attrs)

    def create_detail_links(self, link_params: dict) -> None:
        """
        This method creates a text shape with a URL link button to the connection in the 
        Draw.io diagram structure. Each application shape is represented as an 'mxCell' 
        XML element with specific attributes.
        
        :param link_params: A dictionary containing the necessary parameters.
        """
        source = link_params['source']
        target = link_params['target']
        row = link_params['row']
        text = link_params['text']
        url = link_params['url']
        direction = link_params['direction']

        logging.info('create_ricefw_url(%s, %s, %d, %s, %s, %s)',
                     source, target, row, text, url, direction)

        object_id = f'ricefw_{source}_{target}_{row}'

        # Ensure that each ID is unique
        if object_id not in self.list_of_ids:
            self.list_of_ids.append(object_id)

            value = f'<a href={url}>{text}</a>'
            style = 'text;html=1;strokeColor=none;fillColor=none;align=center;'\
                    'verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=9'

            x_position = 120 + (APP_WIDTH * 2) * self.app_order[source]

            # Create an 'mxCell' XML element for the URL link of the RICEFW ID
            mx_cell_attrs = {
                'id': object_id,
                'value': value,
                'style': style,
                'vertex': '1',
                'parent': '1'
            }

            mx_cell = ET.SubElement(self.xml_content['root'], 'mxCell', mx_cell_attrs)

            # Create an 'mxGeometry' XML element for the connections
            mx_geometry_attrs = {
                'x': str(x_position),
                'y': str(self.size_parameters["y_protocol"] + 10),
                'width': '120',
                'height': '30',
                'as': 'geometry'
            }

            ET.SubElement(mx_cell, 'mxGeometry', mx_geometry_attrs)

    def create_instancies(self) -> None:
        """
        Loop into the interfaces to find all the applications and protocols 
        that need to be created on the draw.io diagram
        
        Create the application shapes in the selected order 

        Create the inbound and outbound protocols for each interface/application
        
        The combination of an application and the inbound and outbound protocols 
        results in a instance
        """
        logging.info('create_structure_app_and_protocols()')

        for row, interface in enumerate(self.config['interfaces']):
            self.size_parameters["y_protocol"] = (self.size_parameters["y_protocol_start"]  +
                                               (PROTOCOL_HEIGHT + Y_OFFSET) * row)

            for _, data in enumerate(interface['apps']):
                if 'sap_app' in data:
                    self.create_app(data['sap_app'], FIRST_FILL_COLOR, FIRST_STROKE_COLOR)
                    self.create_protocol({
                        'app_name': data["sap_app"],
                        'direction': "out",
                        'row': row,
                        'format': data["format"],
                        'position': 70
                    })

                elif 'middleware' in data:
                    self.create_app(data['middleware'], MIDDLE_FILL_COLOR, MIDDLE_STROKE_COLOR)

                    self.create_protocol({
                        'app_name': data["middleware"],
                        'direction': "out",
                        'row': row,
                        'format': '',
                        'position': 70
                    })

                    self.create_protocol({
                        'app_name': data["middleware"],
                        'direction': "in",
                        'row': row,
                        'format': '',
                        'position': -10
                    })

                elif 'gateway' in data:
                    self.create_app(data['gateway'], GATEWAY_FILL_COLOR, GATEWAY_STROKE_COLOR)

                    self.create_protocol({
                        'app_name': data["gateway"],
                        'direction': "out",
                        'row': row,
                        'format': '',
                        'position': 70
                    })

                    self.create_protocol({
                        'app_name': data["gateway"],
                        'direction': "in",
                        'row': row,
                        'format': '',
                        'position': -10
                    })

                elif 'other_middleware' in data:
                    self.create_app(data['other_middleware'], OTHER_FILL_COLOR, OTHER_STROKE_COLOR)

                    self.create_protocol({
                        'app_name': data["other_middleware"],
                        'direction': "out",
                        'row': row,
                        'format': '',
                        'position': 70
                    })

                    self.create_protocol({
                        'app_name': data["other_middleware"],
                        'direction': "in",
                        'row': row,
                        'format': '',
                        'position': -10
                    })

                elif 'connected_app' in data:
                    self.create_app(data['connected_app'], LAST_FILL_COLOR, LAST_STROKE_COLOR)

                    self.create_protocol({
                        'app_name': data["connected_app"],
                        'direction': "in",
                        'row': row,
                        'format': data["format"],
                        'position': -10
                    })


    def create_instancies_connections(self) -> None:
        """
        After creates the applicatoin and protocols shape, this function creates the 
        connections and the labels.
        
        The connections connect the shouce and target protocol for each interface
        
        The labels are created above the connection and the ricefw url created down 
        below to the connections arrows.
        
        the detail link generate a clickable link to an informed url.
        """
        logging.info('create_instancies_connections()')

        for row, interface in enumerate(self.config['interfaces']):
            self.size_parameters["y_protocol"] = (self.size_parameters["y_protocol_start"]  +
                                               (PROTOCOL_HEIGHT + Y_OFFSET) * row)

            for _, data in enumerate(interface['apps']):
                if 'connection' not in data:
                    continue

                app = data['connection']["app"]

                for app_type in APP_TYPES:
                    if app_type not in data:
                        continue

                    app_data = data[app_type]
                    direction = interface["direction"]

                    self.create_connection(app, app_data, row, direction)

                    detail = data['connection'].get("detail")
                    if detail:
                        self.create_detail({
                            'source': app,
                            'target': app_data,
                            'row': row,
                            'text': detail,
                            'direction': direction
                        })

                    interface_info = data['connection'].get("interface")
                    if interface_info:
                        interface_id = interface_info["id"]
                        interface_url = interface_info["url"]

                        self.create_detail_links({
                            'source': app,
                            'target': app_data,
                            'row': row,
                            'text': interface_id,
                            'url': interface_url,
                            'direction': direction
                        })


    def build_xml_file(self) -> None:
        """
        Create the whole structure of the xml file readable by draw.io
        """
        logging.info('build_xml_file()')

        self.initialize_xml_structure()
        self.create_instancies()
        self.create_instancies_connections()


    def generate_diagram_url(self):
        """
        Build the XML file and generate a dinamical url to access the diagram
        :return: draw.io diagram exported in a url format
        """
        logging.info('generate_diagram_url()')

        self.build_xml_file()
        data = ET.tostring(self.xml_content['mxfile'])
        data = self.config['encoder'].encode_diagram_data(data)
        return 'https://viewer.diagrams.net/?#R' + data
    