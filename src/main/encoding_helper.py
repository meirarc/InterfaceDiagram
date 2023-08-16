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
        This method simulates the btoa function in JavaScript.
        It takes a binary data argument and returns a base64-encoded string of data.
        """
        return base64.b64encode(data)

    def pako_deflate_raw(self, data):
        """
        This method compress data using zlib (with specific parameters).
        It takes binary data and returns compressed binary data.
        """
        compress = zlib.compressobj(zlib.Z_DEFAULT_COMPRESSION, zlib.DEFLATED, -15, memLevel=8,
                                    strategy=zlib.Z_DEFAULT_STRATEGY)

        compressed_data = compress.compress(data)
        compressed_data += compress.flush()
        return compressed_data

    def encode_diagram_data(self, data):
        """
        This method applies a series of encoding steps to data, which is expected to be a string.
        It URL-encodes data, compresses it using pako_deflate_raw, base64-encodes it using js_btoa,
        and then URL-encodes the result again.
        """
        data = quote(data, safe='~()*!.\'')
        data = data.encode()
        data = self.pako_deflate_raw(data)
        data = self.js_btoa(data)
        return quote(data)
    