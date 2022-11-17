from .riff_parser import parse_chunk, ListChunkDescriptor

from typing import Optional

class WavInfoChunkReader:

    def __init__(self, f, encoding):
        self.encoding = encoding

        f.seek(0)
        parsed_chunks = parse_chunk(f)

        list_chunks = [chunk for chunk in parsed_chunks.children if type(chunk) is ListChunkDescriptor]

        self.info_chunk = next((chunk for chunk in list_chunks if chunk.signature == b'INFO'), None)

        #: 'ICOP' Copyright
        self.copyright : Optional[str] = self._get_field(f, b'ICOP')
        #: 'IPRD' Product
        self.product : Optional[str]= self._get_field(f, b'IPRD')
        self.album : Optional[str] = self.product
        #: 'IGNR' Genre
        self.genre : Optional[str] = self._get_field(f, b'IGNR')
        #: 'ISBJ' Supject
        self.subject : Optional[str] = self._get_field(f, b'ISBJ')
        #: 'IART' Artist, composer, author
        self.artist : Optional[str] = self._get_field(f, b'IART')
        #: 'ICMT' Comment
        self.comment : Optional[str] = self._get_field(f, b'ICMT')
        #: 'ISFT' Software, encoding application
        self.software : Optional[str] = self._get_field(f, b'ISFT')
        #: 'ICRD' Created date
        self.created_date : Optional[str] = self._get_field(f, b'ICRD')
        #: 'IENG' Engineer
        self.engineer : Optional[str] = self._get_field(f, b'IENG')
        #: 'ITCH' Technician
        self.technician : Optional[str] = self._get_field(f, b'ITCH')
        #: 'IKEY' Keywords, keyword list
        self.keywords : Optional[str] = self._get_field(f, b'IKEY')
        #: 'INAM' Name, title
        self.title : Optional[str] = self._get_field(f, b'INAM')
        #: 'ISRC' Source
        self.source : Optional[str] = self._get_field(f, b'ISRC')
        #: 'TAPE' Tape
        self.tape : Optional[str] = self._get_field(f, b'TAPE')
        #: 'IARL' Archival Location
        self.archival_location : Optional[str] = self._get_field(f, b'IARL')
        #: 'ICSM' Commissioned
        self.commissioned : Optional[str] = self._get_field(f, b'ICMS')

    def _get_field(self, f, field_ident) -> Optional[str]:
        search = next(((chunk.start, chunk.length) for chunk in self.info_chunk.children if chunk.ident == field_ident),
                      None)

        if search is not None:
            f.seek(search[0])
            data = f.read(search[1])
            return data.decode(self.encoding).rstrip('\0')
        else:
            return None

    def to_dict(self):
        """
        A dictionary with all of the key/values read from the INFO scope.
        """
        return {'copyright': self.copyright,
                'product': self.product,
                'album': self.album,
                'genre': self.genre,
                'artist': self.artist,
                'comment': self.comment,
                'software': self.software,
                'created_date': self.created_date,
                'engineer': self.engineer,
                'keywords': self.keywords,
                'title': self.title,
                'source': self.source,
                'tape': self.tape,
                'commissioned': self.commissioned,
                'archival_location': self.archival_location,
                'subject': self.subject,
                'technician': self.technician
                }

    def __repr__(self):
        return_val = self.to_dict()
        return_val.update({'encoding': self.encoding})
        return str(return_val)
