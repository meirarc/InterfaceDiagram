"""
This module is used to provide encode functions on file conversion
"""
import base64
import zlib
from urllib.parse import quote

class EncodingHelper:
    """
    This class is used to provide encoding functions on file conversion
    """
    def __init__(self) -> None:
        pass

    def js_btoa(self, data):
        """
        run similar funciton of JS BTOA in Javascrip
        """
        return base64.b64encode(data)

    def pako_deflate_raw(self, data):
        """
        run a file compression for zlib
        """
        compress = zlib.compressobj(zlib.Z_DEFAULT_COMPRESSION, zlib.DEFLATED, -15, memLevel=8,
                                    strategy=zlib.Z_DEFAULT_STRATEGY)

        compressed_data = compress.compress(data)
        compressed_data += compress.flush()
        return compressed_data

    def encode_diagram_data(self, data):
        """
        encoding the parameter data
        """
        data = quote(data, safe='~()*!.\'')
        data = data.encode()
        data = self.pako_deflate_raw(data)
        data = self.js_btoa(data)
        return quote(data)
    