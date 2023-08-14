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
    def __init__(self, interfaces, encoder, log_level=logging.ERROR):
        logging.basicConfig(level=log_level)
        logging.info(f'Init Class InterfaceDiagram')

        self.interfaces = interfaces  # Input File
        self.list_of_ids = []         # Control of ids
        self.encoder = encoder

        # Sequencing of application
        self.app_lists = self.populate_app_lists(self.interfaces)
        self.app_order, self.app_count = self.create_app_order(self.app_lists)

        # Variant size parameters
        self.y_protocol = 0
        self.y_protocol_start = 40
        self.app_height = 80 + (PROTOCOL_HEIGHT + Y_OFFSET) * (len(self.interfaces) - 1)
        self.page_width = 0
        self.page_width = ((self.app_count * 2) - 1) * APP_WIDTH

        # Public xml content
        self.mxfile = None
        self.root = None


    def populate_app_lists(self, interfaces: List[Dict]) -> Dict[str, List[str]]:
        """
        Populate the interfaces object in separated objects by types.
        app_types = ['sap', 'middleware', 'gateway', 'connected_app'] 

        :param interfaces: The list of interfaces.
        :return: A dictionary where the keys are the app types and the values are the app names.
        """
        logging.info(f'populate_app_lists({interfaces})')

        app_lists = {
            'sap_apps': [],
            'middlewares': [],
            'gateways': [],
            'other_middlewares':[],
            'connected_apps': []
        }

        for interface in interfaces:
            for app in interface['apps']:
                for app_type in app_lists.keys():
                    if app_type[:-1] in app and app[app_type[:-1]] not in app_lists[app_type]:
                        app_lists[app_type].append(app[app_type[:-1]])
        return app_lists


    def create_app_order(self, app_lists: Dict[str, List[str]]) -> Tuple[Dict[str, int], int]:
        """
        Define the sequence of the applications that will be displayed on the diagrams
        app_types = ['sap', 'middleware', 'gateway', 'connected_app'] 

        :param app_lists: A dictionary where keys are the app_types and values are the app_names.
        :return: A dictionary where the keys are the app names and the values are their orders.
        """
        logging.info(f'create_app_order()')

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
        logging.info(f'initialize_xml_structure()')

        self.mxfile = ET.Element('mxfile', {'host': 'app.diagrams.net',
                                    'modified': '2023-07-25T12:42:08.179Z',
                                    'agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                        'AppleWebKit/537.36 (KHTML, like Gecko) '
                                        'Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.82'),
                                    'etag': '70Szxm5LCrq_Rskbk8Uq', 'version': '21.6.5',
                                    'type': 'device'})

        diagram = ET.SubElement(self.mxfile, 'diagram', 
                                {'name': 'Page-1', 'id': 'xI1n7PUDQ-lDr-DjmP3Y'})

        mx_graph_model = ET.SubElement(diagram, 'mxGraphModel', {'dx': '1182', 'dy': '916',
                                                                 'grid': '1', 'gridSize': '10', 
                                                                 'guides': '1', 'tooltips': '1', 
                                                                 'connect': '1', 'arrows': '1', 
                                                                 'fold': '1', 'page': '1', 
                                                                 'pageScale': '1', 
                                                                 'pageWidth': f'{self.page_width}',
                                                                 'pageHeight': f'{self.app_height}',
                                                                 'math': '0', 'shadow': '0'})
        self.root = ET.SubElement(mx_graph_model, 'root')
        ET.SubElement(self.root, 'mxCell', {'id': '0'})
        ET.SubElement(self.root, 'mxCell', {'id': '1', 'parent': '0'})


    def create_app(self, app_name: str, fill_color: str, stroke_color: str) -> None:
        """
        This method creates an application shape in the Draw.io diagram structure. 
        Each application shape is represented as an 'mxCell' XML element with specific attributes.
        
        :param app_name: The name of the application.
        :param fill_color: The color used to fill the shape.
        :param stroke_color: The color used for the outline of the shape.
        """
        logging.info(f"Creating app {app_name}.")

        if app_name not in self.app_order:
            logging.error(f"App name {app_name} is not in the app order.")
            return

        id = app_name
        # Ensure that each ID is unique
        if id not in self.list_of_ids:
            self.list_of_ids.append(id)
            # Create an 'mxCell' XML element for the application shape
            mx_cell = ET.SubElement(self.root, 'mxCell', {'id': id, 'value': app_name, 'style': f'rounded=1;whiteSpace=wrap;html=1;fillColor={fill_color};strokeColor={stroke_color};verticalAlign=top;' , 'parent': '1', 'vertex': '1'})
            ET.SubElement(mx_cell, 'mxGeometry', { 'x': f'{APP_WIDTH * 2 * self.app_order[app_name]}', 'y': '0', 'width': f'{APP_WIDTH}', 'height': str(self.app_height), 'as': 'geometry' })


    def create_protocol(self, app_name:str, direction:str, row:int, format:str, position:int) -> None:
        """
        This method creates an protocol shape in the Draw.io diagram structure. 
        Each application shape is represented as an 'mxCell' XML element with specific attributes.
        
        :param app_name: The name of the application.
        :param direction: indicate an inbound or outbouind flow, reference from SAP system.
        :param row: The row to create the protocol
        :param format: the text to be added inside the protocol shape
        :param position: the position that the shape will be created on the diagram
        """
        logging.info(f'create_protocol({app_name, direction, row, format, position})')

        if app_name not in self.app_order:
            logging.error(f"App name {app_name} is not in the app order.")
            return

        id = f'{direction}_{app_name}_{row}'
        # Ensure that each ID is unique
        if id not in self.list_of_ids:
          self.list_of_ids.append(id)
          # Create an 'mxCell' XML element for the protocol shape
          mx_cell = ET.SubElement(self.root, 'mxCell', { 'id': id, 'value': format, 'style': 'shape=delay;whiteSpace=wrap;html=1;fillColor=#eeeeee;strokeColor=#36393d;rotation=0;fontSize=10;', 'parent': '1', 'vertex': '1' })
          ET.SubElement(mx_cell, 'mxGeometry', {'x': f'{position + (APP_WIDTH * 2 * self.app_order[app_name])}', 'y': f'{self.y_protocol}', 'width': f'{PROTOCOL_WIDTH}', 'height': f'{PROTOCOL_HEIGHT}', 'as': 'geometry' })


    def create_connection(self, source:str, target:str, row:int, direction:str) -> None:
        """
        This method creates an connections in the Draw.io diagram structure. 
        Each application shape is represented as an 'mxCell' XML element with specific attributes.
        
        :param source: The name of the source application
        :param target: The name of the target application
        :param row: The row to create the protocol
        :param direction: indicate an inbound or outbouind flow, reference from SAP system.
        """
        logging.info(f'create_protocol({source, target, row, direction})')

        id = f'conn_{source}_{target}_{row}'
        # Ensure that each ID is unique
        if id not in self.list_of_ids:
          self.list_of_ids.append(id)

          # Define parameters based on the direction (Outbound/Inbound)
          fill_color = CONNECTION_OUT_FILL_COLOR if direction == "Outbound" else CONNECTION_IN_FILL_COLOR
          stroke_color = CONNECTION_OUT_STROKE_COLOR if direction == "Outbound" else CONNECTION_IN_STROKE_COLOR
          source_connection = f'out_{source}_{row}' if direction == "Outbound" else f'in_{target}_{row}'
          target_connection = f'in_{target}_{row}' if direction == "Outbound" else f'out_{source}_{row}'

          # Create an 'mxCell' XML element for the connections
          mx_cell = ET.SubElement(self.root, 'mxCell', { 'id': id, 'value': '', 'invert':'true','style': f'edgeStyle=orthogonalEdgeStyle;rounded=0;fillColor={fill_color};strokeColor={stroke_color};orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=3', 'parent': '1', 'edge': '1', 'source': f'{source_connection}', 'target': f'{target_connection}'})
          ET.SubElement(mx_cell, 'mxGeometry', { 'relative': '1', 'as': 'geometry' })


    def create_detail(self, source:str, target:str, row:int, text:str, direction:str) -> None:
        """
        This method creates a label in the Draw.io diagram structure. 
        Each label is represented as an 'mxCell' XML element with specific attributes.

        :param source: The name of the source application
        :param target: The name of the target application
        :param row: The row to create the protocol
        :param text: the text to be added on the label
        :param direction: indicate an inbound or outbound flow, reference from SAP system.
        """
        logging.info(f'create_detail({source, target, row, text, direction})')

        id = f'detail_{source}_{target}_{row}'
        # Ensure that each ID is unique
        if id not in self.list_of_ids:
          self.list_of_ids.append(id)
          # Create an 'mxCell' XML element for the text shape related to the detail
          mx_cell = ET.SubElement(self.root, 'mxCell', { 'id': id, 'value': text, 'style': 'text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0', 'parent': '1', 'vertex': '1' })
          ET.SubElement(mx_cell, 'mxGeometry', {'x': f'{120 + (APP_WIDTH * 2) * self.app_order[source]}', 'y': f'{self.y_protocol - 20}', 'width': '120','height': '30','as': 'geometry'})
      
      
    def create_detail_links(self, source:str, target:str, row:int, text:str, url:str , direction:str) -> None:
        """
        This method creates an text shape with an URL link botton to the connection in the Draw.io diagram structure. 
        Each application shape is represented as an 'mxCell' XML element with specific attributes.
        
        :param source: The name of the source application
        :param target: The name of the target application
        :param row: The row to create the protocol
        :param text: the text to be added on the shape
        :param url: the url to be added as the weblink
        :param direction: indicate an inbound or outbouind flow, reference from SAP system.
        """
        logging.info(f'create_ricefw_url({source, target, row, text, url , direction})')

        id = f'ricefw_{source}_{target}_{row}'
        # Ensure that each ID is unique
        if id not in self.list_of_ids:
          self.list_of_ids.append(id)
          # Create an 'mxCell' XML element for the text shape related to the URL link of the RICEFW ID
          mx_cell = ET.SubElement(self.root, 'mxCell', { 'id': id, 'value': f'<a href={url}>{text}</a>', 'style': 'text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=9', 'vertex': '1', 'parent': '1' })
          ET.SubElement(mx_cell, 'mxGeometry', { 'x': f'{120 + (APP_WIDTH * 2) * self.app_order[source]}', 'y': f'{self.y_protocol + 10}', 'width': '120', 'height': '30', 'as': 'geometry' })


    def create_instancies(self) -> None:
        """
        Loop into the interfaces to find all the applications and protocols 
        that need to be created on the draw.io diagram
        
        Create the application shapes in the selected order 

        Create the inbound and outbound protocols for each interface/application
        
        The combination of an application and the inbound and outbound protocols 
        results in a instance
        """
        logging.info(f'create_structure_app_and_protocols()')

        for row, interface in enumerate(self.interfaces):
            self.y_protocol = self.y_protocol_start  + (PROTOCOL_HEIGHT + Y_OFFSET) * row

            for _, data in enumerate(interface['apps']):
                if 'sap_app' in data:
                    self.create_app(data['sap_app'], FIRST_FILL_COLOR, FIRST_STROKE_COLOR)
                    self.create_protocol(data["sap_app"], "out", row, data["format"], 70)

                elif 'middleware' in data:
                    self.create_app(data['middleware'], MIDDLE_FILL_COLOR, MIDDLE_STROKE_COLOR)
                    self.create_protocol(data['middleware'], "out", row, '', 70)
                    self.create_protocol(data['middleware'], "in", row,'', -10)

                elif 'gateway' in data:
                    self.create_app(data['gateway'], GATEWAY_FILL_COLOR, GATEWAY_STROKE_COLOR)
                    self.create_protocol(data['gateway'], "out", row, '', 70)
                    self.create_protocol(data['gateway'], "in", row,'', -10)

                elif 'other_middleware' in data:
                    self.create_app(data['other_middleware'], OTHER_FILL_COLOR, OTHER_STROKE_COLOR)
                    self.create_protocol(data['other_middleware'], "out", row, '', 70)
                    self.create_protocol(data['other_middleware'], "in", row,'', -10)

                elif 'connected_app' in data:
                    self.create_app(data['connected_app'], LAST_FILL_COLOR, LAST_STROKE_COLOR)
                    self.create_protocol(data['connected_app'], "in", row, data['format'], -10)


    def create_instancies_connections(self) -> None:
        """
        After creates the applicatoin and protocols shape, this function creates the connections and the labels.
        The connections connect the shouce and target protocol for each interface
        The labels are created above the connection and the ricefw url created down below to the connections arrows.
        the detail link generate a clickable link to an informed url.
        """
        logging.info(f'create_instancies_connections()')

        for row, interface in enumerate(self.interfaces):
            self.y_protocol = self.y_protocol_start  + (PROTOCOL_HEIGHT + Y_OFFSET) * row

            for _, data in enumerate(interface['apps']):
                if 'connection' in data:

                    for app_type in APP_TYPES:
                        if app_type in data:

                            app = data['connection']["app"]
                            app_data = data[app_type]
                            direction = interface["direction"]
                            self.create_connection(app, app_data, row, direction)

                            if 'detail' in data['connection']:
                                detail = data['connection']["detail"]
                                self.create_detail(app, app_data, row, detail, direction)

                            if 'interface' in data['connection']:
                                interface_id = data['connection']["interface"]["id"]
                                interface_url = data['connection']["interface"]["url"]
                                self.create_detail_links(app, app_data, row, interface_id, interface_url, direction)


    def build_xml_file(self) -> None:
        """
        Create the whole structure of the xml file readable by draw.io
        """
        logging.info(f'build_xml_file()')

        self.initialize_xml_structure()
        self.create_instancies()
        self.create_instancies_connections()


    def generate_diagram_url(self):
        """
        Build the XML file and generate a dinamical url to access the diagram
        :return: draw.io diagram exported in a url format
        """
        logging.info(f'generate_diagram_url()')

        self.build_xml_file()
        data = ET.tostring(self.mxfile)
        data = self.encoder.encode_diagram_data(data)
        return 'https://viewer.diagrams.net/?#R' + data
    