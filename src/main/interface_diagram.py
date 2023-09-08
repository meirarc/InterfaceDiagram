"""
This module defines the InterfaceDiagram class used to generate diagrams
from some input data.
"""
import logging
import xml.etree.ElementTree as ET
from typing import List, Dict, Tuple

from src.main import config
from src.main.logging_utils import debug_logging
from src.main.encoding_helper import EncodingHelper
from src.main.data_definitions import InterfaceStructure


class InterfaceDiagram:
    """
    Class to represent and generate an Interface Diagram.
    """
    @debug_logging
    def __init__(self,
                 interfaces: List[InterfaceStructure],
                 encoder: EncodingHelper()) -> None:
        """
        Initialize the InterfaceDiagram class.

        :param interfaces: List of interfaces to be represented in the diagram.
        :param encoder: Encoder to write the output file.
        :param log_level: Logging level. Default is logging.ERROR.
        """

        # Configuration parameters
        self.config = {
            'interfaces': interfaces,
            'encoder': encoder
        }

        self.list_of_ids = []  # Control of ids

        # Initialize application lists and orders
        self.app_lists = self.populate_app_lists(interfaces)
        self.app_order, self.app_count = self.create_app_order(self.app_lists)

        # Count the unique code_ids to get the correct number of rows
        unique_code_ids = len(
            set(interface.code_id for interface in interfaces))

        # Initialize size parameters
        self.size_parameters = {
            'y_protocol': 0,
            'y_protocol_start': 40,
            'app_height': 80 + (config.PROTOCOL_HEIGHT + config.Y_OFFSET) * (unique_code_ids - 1),
            'page_width': ((self.app_count * 2) - 1) * config.APP_WIDTH
        }

        # Initialize XML content
        self.xml_content = {
            'mxfile': None,
            'root': None
        }

    @debug_logging
    def populate_app_lists(self, interfaces: List[InterfaceStructure]) -> Dict[str, List[str]]:
        """
        Populate the list of applications for each type from the given interfaces.

        :param interfaces: List of interfaces.
        :return: Dictionary of lists of applications by type.
        """

        app_lists = {
            'sap_apps': [],
            'middlewares': [],
            'gateways': [],
            'other_middlewares': [],
            'connected_apps': []
        }

        for interface in interfaces:
            for app in interface.apps:
                for app_type_plural, app_names in app_lists.items():
                    app_type_singular = app_type_plural[:-1]
                    # Compare the app_type with the singular form of keys in app_lists
                    if app.app_type == app_type_singular:
                        if app.app_name and app.app_name not in app_names:
                            app_names.append(app.app_name)
        return app_lists

    @debug_logging
    def create_app_order(self, app_lists: Dict[str, List[str]]) -> Tuple[Dict[str, int], int]:
        """
        Create the order in which applications will appear in the diagram.

        :param app_lists: Dictionary of lists of applications by type.
        :return: Dictionary of application order and total count of applications.
        """

        app_list = (
            app_lists['sap_apps'] +
            app_lists['middlewares'] +
            app_lists['gateways'] +
            app_lists['other_middlewares'] +
            app_lists['connected_apps']
        )

        app_order = {app: i for i, app in enumerate(app_list)}
        return app_order, len(app_list)

    @debug_logging
    def initialize_xml_structure(self) -> None:
        """
        Create the initial elements of the XML file readable by draw.io
        The initial structure must need to contain the:
          mxfile, diagram, mxGraphModel, root, mxCell(0), mxCell(1)
        """
        mxfile_parameters = {'host': 'app.diagrams.net', 'modified': '2023-07-25T12:42:08.179Z',
                             'agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                       'AppleWebKit/537.36 (KHTML, like Gecko) '
                                       'Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.82'),
                             'etag': '70Szxm5LCrq_Rskbk8Uq', 'version': '21.6.5',
                             'type': 'device'}

        self.xml_content['mxfile'] = ET.Element('mxfile', mxfile_parameters)

        diagram = ET.SubElement(self.xml_content['mxfile'], 'diagram',
                                {'name': 'Page-1', 'id': 'xI1n7PUDQ-lDr-DjmP3Y'})

        page_width = f'{self.size_parameters["page_width"]}'
        page_height = f'{self.size_parameters["app_height"]}'

        mx_graph_model = ET.SubElement(diagram, 'mxGraphModel', {'dx': '1182', 'dy': '916',
                                                                 'grid': '1', 'gridSize': '10',
                                                                 'guides': '1', 'tooltips': '1',
                                                                 'connect': '1', 'arrows': '1',
                                                                 'fold': '1',
                                                                 'page': '1', 'pageScale': '1',
                                                                 'pageWidth': page_width,
                                                                 'pageHeight': page_height,
                                                                 'math': '0', 'shadow': '0'})

        self.xml_content['root'] = ET.SubElement(mx_graph_model, 'root')
        ET.SubElement(self.xml_content['root'], 'mxCell', {'id': '0'})
        ET.SubElement(self.xml_content['root'], 'mxCell', {
                      'id': '1', 'parent': '0'})

    @debug_logging
    def create_app(self, app_name: str, fill_color: str, stroke_color: str) -> None:
        """
        This method creates an application shape in the Draw.io diagram structure. 
        Each application shape is represented as an 'mxCell' XML element with specific attributes.

        :param app_name: The name of the application.
        :param fill_color: The color used to fill the shape.
        :param stroke_color: The color used for the outline of the shape.
        """
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

            x_value = f'{config.APP_WIDTH * 2 * self.app_order[app_name]}'
            width_value = f'{config.APP_WIDTH}'
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

    @debug_logging
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
                'x': f'{position + (config.APP_WIDTH * 2 * self.app_order[app_name])}',
                'y': f'{self.size_parameters["y_protocol"]}',
                'width': f'{config.PROTOCOL_WIDTH}',
                'height': f'{config.PROTOCOL_HEIGHT}',
                'as': 'geometry'
            })

    @debug_logging
    def create_connection(self, source: str, target: str, row: int, direction: str) -> None:
        """
        This method creates an connections in the Draw.io diagram structure. 
        Each application shape is represented as an 'mxCell' XML element with specific attributes.

        :param source: The name of the source application
        :param target: The name of the target application
        :param row: The row to create the protocol
        :param direction: indicate an inbound or outbouind flow, reference from SAP system.
        """

        object_id = f'conn_{source}_{target}_{row}'
        # Ensure that each ID is unique
        if object_id not in self.list_of_ids:
            self.list_of_ids.append(object_id)

            # Define parameters based on the direction (Outbound/Inbound)
            fill_color = (config.CONNECTION_OUT_FILL_COLOR if direction == "Outbound"
                          else config.CONNECTION_IN_FILL_COLOR)
            stroke_color = (config.CONNECTION_OUT_STROKE_COLOR if direction == "Outbound"
                            else config.CONNECTION_IN_STROKE_COLOR)
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
            mx_cell = ET.SubElement(
                self.xml_content['root'], 'mxCell', mx_cell_attrs)

            # Attributes for the 'mxGeometry' XML element
            mx_geometry_attrs = {
                'relative': '1',
                'as': 'geometry'
            }

            # Create an 'mxGeometry' XML element for the connections
            ET.SubElement(mx_cell, 'mxGeometry', mx_geometry_attrs)

    @debug_logging
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

        object_id = f'detail_{source}_{target}_{row}'

        # Ensure that each ID is unique
        if object_id not in self.list_of_ids:
            self.list_of_ids.append(object_id)

            style = 'text;html=1;strokeColor=none;fillColor=none;align=center;'\
                    'verticalAlign=middle;whiteSpace=wrap;rounded=0'

            x_position = 120 + (config.APP_WIDTH * 2) * self.app_order[source]

            # Create an 'mxCell' XML element for the text shape related to the detail
            mx_cell_attrs = {
                'id': object_id,
                'value': text,
                'style': style,
                'parent': '1',
                'vertex': '1'
            }

            mx_cell = ET.SubElement(
                self.xml_content['root'], 'mxCell', mx_cell_attrs)

            # Create an 'mxGeometry' XML element for the connections
            mx_geometry_attrs = {
                'x': str(x_position),
                'y': str(self.size_parameters["y_protocol"] - 20),
                'width': '120',
                'height': '30',
                'as': 'geometry'
            }

            ET.SubElement(mx_cell, 'mxGeometry', mx_geometry_attrs)

    @debug_logging
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

        object_id = f'ricefw_{source}_{target}_{row}'

        # Ensure that each ID is unique
        if object_id not in self.list_of_ids:
            self.list_of_ids.append(object_id)

            value = f'<a href={url}>{text}</a>'
            style = 'text;html=1;strokeColor=none;fillColor=none;align=center;'\
                    'verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=9'

            x_position = 120 + (config.APP_WIDTH * 2) * self.app_order[source]

            # Create an 'mxCell' XML element for the URL link of the RICEFW ID
            mx_cell_attrs = {
                'id': object_id,
                'value': value,
                'style': style,
                'vertex': '1',
                'parent': '1'
            }

            mx_cell = ET.SubElement(
                self.xml_content['root'], 'mxCell', mx_cell_attrs)

            # Create an 'mxGeometry' XML element for the connections
            mx_geometry_attrs = {
                'x': str(x_position),
                'y': str(self.size_parameters["y_protocol"] + 10),
                'width': '120',
                'height': '30',
                'as': 'geometry'
            }

            ET.SubElement(mx_cell, 'mxGeometry', mx_geometry_attrs)

    @debug_logging
    def create_instancies(self) -> None:
        """
        Loop into the interfaces to find all the applications and protocols 
        that need to be created on the draw.io diagram
        Create the application shapes in the selected order 
        Create the inbound and outbound protocols for each interface/application
        The combination of an application and the inbound and outbound protocols 
        results in an instance
        """

        color_map = {
            'sap_app': (config.FIRST_FILL_COLOR, config.FIRST_STROKE_COLOR),
            'middleware': (config.MIDDLE_FILL_COLOR, config.MIDDLE_STROKE_COLOR),
            'gateway': (config.GATEWAY_FILL_COLOR, config.GATEWAY_STROKE_COLOR),
            'other_middleware': (config.OTHER_FILL_COLOR, config.OTHER_STROKE_COLOR),
            'connected_app': (config.LAST_FILL_COLOR, config.LAST_STROKE_COLOR)
        }

        current_code_id = None
        row = -1  # Initialize to -1 so that the first iteration sets it to 0

        for interface in self.config['interfaces']:

            # Check if the code_id has changed
            if interface.code_id != current_code_id:
                row += 1
                current_code_id = interface.code_id

            self.size_parameters["y_protocol"] = (self.size_parameters["y_protocol_start"] +
                                                  (config.PROTOCOL_HEIGHT + config.Y_OFFSET) * row)

            for app in interface.apps:

                app_type = app.app_type
                app_name = app.app_name
                format_value = app.format

                fill_color, stroke_color = color_map.get(
                    app_type, ('#FFFFFF', '#000000'))

                self.create_app(app_name, fill_color, stroke_color)

                if app_type in ['middleware', 'gateway', 'other_middleware']:
                    directions = ["out", "in"]
                else:
                    directions = ["out"] if app_type == 'sap_app' else ["in"]

                for direction in directions:
                    self.create_protocol({
                        'app_name': app_name,
                        'direction': direction,
                        'row': row,
                        'format': format_value,
                        'position': 70 if direction == "out" else -10
                    })

    @debug_logging
    def create_instancies_connections(self) -> None:
        """
        After creating the application and protocols shapes, this function creates the 
        connections and labels.
        The connections connect the source and target protocol for each interface.
        The labels are created above the connection and the ricefw URL is created down 
        below the connections arrows.
        The detail link generates a clickable link to an informed URL.
        """

        current_code_id = None
        row = -1  # Initialize to -1 so that the first iteration sets it to 0

        for interface in self.config['interfaces']:

            if interface.code_id != current_code_id:
                row += 1
                current_code_id = interface.code_id

            self.size_parameters["y_protocol"] = (self.size_parameters["y_protocol_start"] +
                                                  (config.PROTOCOL_HEIGHT + config.Y_OFFSET) * row)

            for app in interface.apps:

                connection_app = app.connection.app
                if not connection_app:
                    continue

                app_name = app.app_name
                direction = interface.direction

                self.create_connection(
                    connection_app, app_name, row, direction)

                connection_detail = app.connection.detail
                if connection_detail:
                    self.create_detail({
                        'source': connection_app,
                        'target': app_name,
                        'row': row,
                        'text': connection_detail,
                        'direction': direction
                    })

                interface_info = app.interface
                if interface_info:
                    interface_id = interface_info.interface_id
                    interface_url = interface_info.interface_url

                    self.create_detail_links({
                        'source': connection_app,
                        'target': app_name,
                        'row': row,
                        'text': interface_id,
                        'url': interface_url,
                        'direction': direction
                    })

    @debug_logging
    def build_xml_file(self) -> None:
        """
        Create the whole structure of the xml file readable by draw.io
        """
        self.initialize_xml_structure()
        self.create_instancies()
        self.create_instancies_connections()

    @debug_logging
    def generate_diagram_url(self):
        """
        Build the XML file and generate a dinamical url to access the diagram
        :return: draw.io diagram exported in a url format
        """

        self.build_xml_file()
        data = ET.tostring(self.xml_content['mxfile'])
        data = self.config['encoder'].encode_diagram_data(data)
        return 'https://viewer.diagrams.net/?#R' + data
