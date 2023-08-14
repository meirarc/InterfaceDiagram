import base64, zlib
from urllib.parse import quote

class EncodingHelper:
    def __init__(self) -> None:
        pass
    
    def js_btoa(self, data):
        return base64.b64encode(data)
    
    def pako_deflate_raw(self, data):
        compress = zlib.compressobj(zlib.Z_DEFAULT_COMPRESSION, zlib.DEFLATED, -15, memLevel=8,strategy=zlib.Z_DEFAULT_STRATEGY)
        compressed_data = compress.compress(data)
        compressed_data += compress.flush()
        return compressed_data
    
    def encode_diagram_data(self, data):
        data = quote(data, safe='~()*!.\'')
        data = data.encode()
        data = self.pako_deflate_raw(data)
        data = self.js_btoa(data)
        return quote(data)