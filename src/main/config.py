"""
This module provides the constants to be used in the InterfaceDiagram class.
"""

# Fill colors for various components
FIRST_FILL_COLOR = '#dae8fc'              # Main system color
MIDDLE_FILL_COLOR = '#d5e8d4'             # Middlewares color
GATEWAY_FILL_COLOR = '#ffe6cc'            # Gateway color
OTHER_FILL_COLOR = '#fff2cc'              # Other Middleware color
LAST_FILL_COLOR = '#f5f5f5'               # Connected App color
CONNECTION_OUT_FILL_COLOR = '#dae8fc'     # Outbound Connection color
CONNECTION_IN_FILL_COLOR = '#ffcd28'      # Inbound Connection color

# Stroke colors for various components
FIRST_STROKE_COLOR = '#6c8ebf'            # Main system color
MIDDLE_STROKE_COLOR = '#82b366'           # Middlewares color
GATEWAY_STROKE_COLOR = '#d79b00'          # Gateway color
OTHER_STROKE_COLOR = '#d6b656'            # Other Middleware color
LAST_STROKE_COLOR = '#666666'             # Connected App color
CONNECTION_OUT_STROKE_COLOR = '#7ea6e0'   # Outbound Connection color
CONNECTION_IN_STROKE_COLOR = '#d79b00'    # Inbound Connection color

# Size parameters for diagram elements
Y_OFFSET = 70                             # Additional space between each protocol
PROTOCOL_HEIGHT = 20                      # Protocol height
PROTOCOL_WIDTH = 60                       # Protocol width
APP_WIDTH = 120                           # Application width

# Types of applications relevant to the diagrams
APP_TYPES = ['sap_app',
             'middleware',
             'gateway',
             'other_middleware',
             'connected_app']
