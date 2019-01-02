
from .riff_parser import parse_chunk, ListChunkDescriptor

class WavInfoChunkReader:

    def __init__(self, f, encoding):
        self.encoding = encoding

        f.seek(0)
        parsed_chunks = parse_chunk(f)

        list_chunks = [chunk for chunk in parsed_chunks.children \
                if type(chunk) is ListChunkDescriptor]

        self.info_chunk  = next((chunk for chunk in list_chunks \
                if chunk.signature == b'INFO'), None)

        self.copyright      = self._get_field(f,b'ICOP')
        self.product        = self._get_field(f,b'IPRD')
        self.genre          = self._get_field(f,b'IGNR')
        self.artist         = self._get_field(f,b'IART')
        self.comment        = self._get_field(f,b'ICMT')
        self.software       = self._get_field(f,b'ISFT')
        self.created_date   = self._get_field(f,b'ICRD')
        self.engineer       = self._get_field(f,b'IENG')
        self.keywords       = self._get_field(f,b'IKEY')
        self.title          = self._get_field(f,b'INAM')
        self.source         = self._get_field(f,b'ISRC')
        self.tape           = self._get_field(f,b'TAPE')


    def _get_field(self, f, field_ident):

        search = next( ( (chunk.start, chunk.length) for chunk in self.info_chunk.children \
                if chunk.ident == field_ident ), None)

        if search is not None:
            f.seek(search[0])
            data = f.read(search[1])
            return data.decode(self.encoding).rstrip('\0')
        else:
            return None


    def to_dict(self):
        return {'copyright':    self.copyright,
                'product':  self.product,
                'genre':    self.genre,
                'artist':   self.artist,
                'comment':  self.comment,
                'software': self.software,
                'created_date': self.created_date,
                'engineer': self.engineer,
                'keywords': self.keywords,
                'title':    self.title,
                'source':   self.source,
                'tape':     self.tape
                }






