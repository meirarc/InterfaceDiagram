"""
This module is used to provide encode functions on file conversion
"""
import base64
import zlib
from urllib.parse import quote

from src.main.logging_utils import debug_logging


class EncodingHelper:
    """
    This class is used to provide encoding functions on file conversion
    """

    @debug_logging
    def js_btoa(self, data: bytes) -> bytes:
        """
        Simulates the JavaScript btoa function.
        Takes binary data and returns a base64-encoded string.

        Args:
            data (bytes): Binary data to encode.

        Returns:
            bytes: Base64-encoded data.
        """
        return base64.b64encode(data)

    @debug_logging
    def pako_deflate_raw(self, data: bytes) -> bytes:
        """
        Compresses data using zlib with specific parameters.

        Args:
            data (bytes): Binary data to compress.

        Returns:
            bytes: Compressed binary data.
        """
        compress = zlib.compressobj(zlib.Z_DEFAULT_COMPRESSION, zlib.DEFLATED, -15, memLevel=8,
                                    strategy=zlib.Z_DEFAULT_STRATEGY)

        compressed_data = compress.compress(data)
        compressed_data += compress.flush()
        return compressed_data

    @debug_logging
    def encode_diagram_data(self, data: str) -> str:
        """
        Applies a series of encoding steps to the data, which is expected to be a string.
        URL-encodes the data, compresses it, base64-encodes it, 
        and then URL-encodes the result again.

        Args:
            data (str): String data to encode.

        Returns:
            str: Encoded string data.
        """
        data = quote(data, safe='~()*!.\'')
        data = data.encode()
        data = self.pako_deflate_raw(data)
        data = self.js_btoa(data)
        return quote(data)
