"""
This module provide the contants to be used on the InterfaceDiagram class
"""
# Constant fill colors
FIRST_FILL_COLOR = '#dae8fc'              # Main system (that drives the interface direction) color
MIDDLE_FILL_COLOR = '#d5e8d4'             # Middlewares colors
GATEWAY_FILL_COLOR = '#ffe6cc'            # Gateway Colors
OTHER_FILL_COLOR = '#fff2cc'              # Other Middleware colors
LAST_FILL_COLOR = '#f5f5f5'               # Connected App colors
CONNECTION_OUT_FILL_COLOR = '#dae8fc'     # Outbound Connection colors
CONNECTION_IN_FILL_COLOR = '#ffcd28'      # Inbound Connection colors

# Constant stroke colors
FIRST_STROKE_COLOR  = '#6c8ebf'           # Main system (that drives the interface direction) color
MIDDLE_STROKE_COLOR = '#82b366'           # Middlewares colors
GATEWAY_STROKE_COLOR = '#d79b00'          # Gateway Colors
OTHER_STROKE_COLOR = '#d6b656'            # Other Middleware colors
LAST_STROKE_COLOR = '#666666'             # Connected App colors
CONNECTION_OUT_STROKE_COLOR = '#7ea6e0'   # Outbound Connection colors
CONNECTION_IN_STROKE_COLOR = '#d79b00'    # Inbound Connection colors

# Constant size parameters
Y_OFFSET = 70           # additional space between each protocol
PROTOCOL_HEIGHT = 20    # protocol height
PROTOCOL_WIDTH = 60     # protocol width
APP_WIDTH = 120         # application width

# Constant for the app sequencing
# Types of applications in scope to the diagrams
APP_TYPES = ['sap_app', 'middleware', 'gateway', 'other_middleware', 'connected_app']
