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

PROTOCOL_FILL_COLOR = '#eeeeee'           # Protocol Fill color
PROTOCOL_STROKE_COLOR = '#36393d'         # Protocol Stroke color

APP_DEFAULT_FILL_COLOR = '#FFFFFF'        # Standard app fill color
APP_DEFAULT_STROKE_COLOR = '#000000'      # Standard app stroke color

# Size parameters for diagram elements
Y_OFFSET = 70                             # Additional space between each protocol
APP_WIDTH = 120                           # Application width
APP_MIN_HEIGHT = 80                       # Minimum height for the application shape
APP_SIZE_SPACE = 2                        # The times of app_width

PROTOCOL_HEIGHT = 20                      # Protocol height
PROTOCOL_WIDTH = 60                       # Protocol width
Y_PROTOCOL_STARTS = 0                     # Initial value for the Y_PROTOCOL
Y_PROTOCOL_STARTED_POSITION = 40          # Start position for protocols
PROTOCOL_OUT_POSITION = 70                # Position for out protocol
PROTOCOL_IN_POSITION = -10                 # Position for in protocol

X_DETAIL_INITIAL = 120                    # Initial position for the Detail
DETAIL_WIDTH = 120                        # Width for the Detail
DETAIL_HEIGHT = 30                        # Height for the Detail
DETAIL_SUB_SPACING = 20                   # Sub spacing for the detail vs app


# XML Parameters
MXFILE_PARAMETERS = {
    'host': 'app.diagrams.net',
    'modified': '2023-07-25T12:42:08.179Z',
    'agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
              'AppleWebKit/537.36 (KHTML, like Gecko) '
              'Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.82'),
    'etag': '70Szxm5LCrq_Rskbk8Uq',
    'version': '21.6.5',
    'type': 'device'
}

DIAGRAM_PARAMETERS = {'name': 'Page-1', 'id': 'xI1n7PUDQ-lDr-DjmP3Y'}

DEFAULT_PARENT_ID = '1'
DEFAULT_VERTEX = '1'
APP_GEOMETRY = 'geometry'
DEFAULT_EDGE = '1'

OUTBOUND = "Outbound"
INBOUND = "Inbound"

COLOR_MAP = {
    'sap_app': (FIRST_FILL_COLOR, FIRST_STROKE_COLOR),
    'middleware': (MIDDLE_FILL_COLOR, MIDDLE_STROKE_COLOR),
    'gateway': (GATEWAY_FILL_COLOR, GATEWAY_STROKE_COLOR),
    'other_middleware': (OTHER_FILL_COLOR, OTHER_STROKE_COLOR),
    'connected_app': (LAST_FILL_COLOR, LAST_STROKE_COLOR)
}
