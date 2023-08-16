"""
This module test the config.py file that contains a series of constants for InterfaceDiagram class
"""
import unittest
import re
from src.main import config

class TestConfigConstants(unittest.TestCase):
    """
    This class test the config.py file that contains a series of constants for
    InterfaceDiagram class
    """

    def test_constants_existence(self):
        """
        Test the existence of the contansts on the config file
        """
        # Check if certain constants are defined in the config module
        self.assertTrue(hasattr(config, 'FIRST_FILL_COLOR'))
        self.assertTrue(hasattr(config, 'MIDDLE_FILL_COLOR'))
        self.assertTrue(hasattr(config, 'PROTOCOL_HEIGHT'))
        self.assertTrue(hasattr(config, 'APP_WIDTH'))
        self.assertTrue(hasattr(config, 'APP_TYPES'))

    def test_valid_hex_color_codes(self):
        """
        Test the format of the contansts on the config file
        """
        # Regular expression pattern for a valid HEX color code
        pattern = re.compile('^#(?:[0-9a-fA-F]{3}){1,2}$')

        # Validate the format of color constants
        self.assertTrue(pattern.match(config.FIRST_FILL_COLOR))
        self.assertTrue(pattern.match(config.MIDDLE_FILL_COLOR))
        self.assertTrue(pattern.match(config.GATEWAY_FILL_COLOR))
        self.assertTrue(pattern.match(config.OTHER_FILL_COLOR))
        self.assertTrue(pattern.match(config.LAST_FILL_COLOR))
        self.assertTrue(pattern.match(config.CONNECTION_OUT_FILL_COLOR))
        self.assertTrue(pattern.match(config.CONNECTION_IN_FILL_COLOR))
        self.assertTrue(pattern.match(config.FIRST_STROKE_COLOR))
        self.assertTrue(pattern.match(config.MIDDLE_STROKE_COLOR))
        self.assertTrue(pattern.match(config.GATEWAY_STROKE_COLOR))
        self.assertTrue(pattern.match(config.OTHER_STROKE_COLOR))
        self.assertTrue(pattern.match(config.LAST_STROKE_COLOR))
        self.assertTrue(pattern.match(config.CONNECTION_OUT_STROKE_COLOR))
        self.assertTrue(pattern.match(config.CONNECTION_IN_STROKE_COLOR))

# Run the tests
if __name__ == '__main__':
    unittest.main()
