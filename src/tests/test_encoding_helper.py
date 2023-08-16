"""
This module is used to test the EncodingHelper class and functions
"""
import unittest
import base64
import zlib
from urllib.parse import quote

from src.main.encoding_helper import EncodingHelper

class TestEncodingHelper(unittest.TestCase):
    """
    This class is used to test the EncodingHelper class and functions
    """
    def test_js_btoa(self):
        """
        Test the result of the js_btoa function
        """
        # Sample binary data
        data = b'Hello, World!'

        # Expected base64-encoded string
        expected_output = base64.b64encode(data)

        # Create an instance of EncodingHelper
        helper = EncodingHelper()

        # Call the js_btoa method
        actual_output = helper.js_btoa(data)

        # Assert that the actual output is equal to the expected output
        self.assertEqual(actual_output, expected_output)

    def test_pako_deflate_raw(self):
        """
        Test the result of the pako_deflate_raw function
        """
        # Sample binary data
        data = b'Hello, World!'

        # Expected compressed data
        compress = zlib.compressobj(zlib.Z_DEFAULT_COMPRESSION, zlib.DEFLATED, -15, memLevel=8,
                                    strategy=zlib.Z_DEFAULT_STRATEGY)
        expected_output = compress.compress(data)
        expected_output += compress.flush()

        # Create an instance of EncodingHelper
        helper = EncodingHelper()

        # Call the pako_deflate_raw method
        actual_output = helper.pako_deflate_raw(data)

        # Assert that the actual output is equal to the expected output
        self.assertEqual(actual_output, expected_output)

    def test_encode_diagram_data(self):
        """
        Test the result of the encode_diagram_dat function
        """
        # Sample string data
        data = 'Hello, World!'

        # Expected encoded string
        quoted_data = quote(data, safe='~()*!.\'')
        quoted_data = quoted_data.encode()
        compress = zlib.compressobj(zlib.Z_DEFAULT_COMPRESSION, zlib.DEFLATED, -15, memLevel=8,
                                    strategy=zlib.Z_DEFAULT_STRATEGY)
        compressed_data = compress.compress(quoted_data)
        compressed_data += compress.flush()
        base64_data = base64.b64encode(compressed_data)
        expected_output = quote(base64_data)

        # Create an instance of EncodingHelper
        helper = EncodingHelper()

        # Call the encode_diagram_data method
        actual_output = helper.encode_diagram_data(data)

        # Assert that the actual output is equal to the expected output
        self.assertEqual(actual_output, expected_output)

# Run the tests
if __name__ == '__main__':
    unittest.main()
