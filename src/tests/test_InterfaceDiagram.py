import unittest
from unittest.mock import Mock, patch

import json
import requests
from bs4 import BeautifulSoup

from src.main.interface_diagram import InterfaceDiagram
from src.main.JSONParser import JSONParser
from src.main.EncodingHelper import EncodingHelper

import xml.etree.ElementTree as ET


class TestInterfaceDiagram(unittest.TestCase):
    def setUp(self):
        """
        This method will run before each test method. 
        You can set up common mock data or mock objects here.
        """
        
        file_name = 'src/tests/test_data/interfaces.json'
        
        with open(file_name, 'r') as f:
            data = json.load(f)  # Load JSON data from a file

        parser = JSONParser()
        self.interfaces = parser.json_to_object(data)
        pass

    def tearDown(self):
        """
        This method will run after each test method. 
        You can use it to clean up any resources if needed.
        """
        pass


    def test_populate_app_lists(self):
        """
        Test the function populate_app_lists comparing the self.app_list before and after running the function
        """
        diagram = InterfaceDiagram(self.interfaces, EncodingHelper())
        
        initial_app_lists = diagram.app_lists.copy()
        after_app_list = diagram.populate_app_lists(diagram.config['interfaces'])

        self.assertEqual(initial_app_lists, after_app_list)


    def test_create_app_order(self):
        diagram = InterfaceDiagram(self.interfaces, EncodingHelper())

        # Assuming that the method modifies self.app_order and self.app_count
        initial_app_order = diagram.app_order
        initial_app_count = diagram.app_count

        app_lists = diagram.app_lists.copy()
        app_order, app_count = diagram.create_app_order(app_lists)

        diagram.create_app_order(diagram.app_lists)
        
        self.assertEqual(initial_app_order, app_order)
        self.assertEqual(initial_app_count, app_count)


    def test_initialize_xml_structure(self):
        diagram = InterfaceDiagram(self.interfaces, EncodingHelper())
        
        initial_mxfile = diagram.xml_content['mxfile']
        initial_root = diagram.xml_content['root']
        mock_string_mxfile = f'<mxfile host="app.diagrams.net" modified="2023-07-25T12:42:08.179Z" agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.82" etag="70Szxm5LCrq_Rskbk8Uq" version="21.6.5" type="device"><diagram name="Page-1" id="xI1n7PUDQ-lDr-DjmP3Y"><mxGraphModel dx="1182" dy="916" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{diagram.size_parameters["page_width"]}" pageHeight="{diagram.size_parameters["app_height"]}" math="0" shadow="0"><root><mxCell id="0" /><mxCell id="1" parent="0" /></root></mxGraphModel></diagram></mxfile>'
        
        
        diagram.initialize_xml_structure()

        mxfile_string = ET.tostring(diagram.xml_content['mxfile'], encoding='utf-8').decode('utf-8')
        self.assertEqual(mxfile_string, mock_string_mxfile)

        self.assertIsNotNone(diagram.xml_content['mxfile'])
        self.assertIsNotNone(diagram.xml_content['root'])
        
        self.assertNotEqual(initial_mxfile, diagram.xml_content['mxfile'])
        self.assertNotEqual(initial_root, diagram.xml_content['root'])


    def test_generate_diagram_url(self):
        diagram = InterfaceDiagram(self.interfaces, EncodingHelper())
        url = diagram.generate_diagram_url()

        # Perform the GET request
        response = requests.get(url)
        
        # Verify the status code
        self.assertEqual(response.status_code, 200)
        
        # Use BeautifulSoup to parse the HTML and extract the title
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title.string
        
        # Verify the title (replace 'Expected Title' with the expected title value)
        self.assertEqual(title, 'Flowchart Maker & Online Diagram Software')


if __name__ == '__main__':
    unittest.main()
