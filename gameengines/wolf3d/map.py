import abc
import struct
import sys
from dataclasses import dataclass


@dataclass(slots=True)
class Header:

    name: str
    width: int
    height: int


class Wolf3dMap:

    header_cls = Header

    def __init__(self, header=None):
        self.header = header or self.header_cls('New Map', 64, 64)


class MapReaderBase(metaclass=abc.ABCMeta):

    @property
    @abc.abstractmethod
    def map_cls(cls):
        """"""


class HavokMapReader(MapReaderBase):

    map_cls = Wolf3dMap

    def __call__(self, file_path):
        with open(file_path, 'rb') as file:

            # These first bits are more to do with the reader than the map itself.
            format = struct.unpack('<6s', file.read(6))[0]
            unknown1 = struct.unpack('<H', file.read(2))[0]
            unknown2 = struct.unpack('<H', file.read(2))[0]
            num_planes = struct.unpack('<H', file.read(2))[0]
            num_name_chars = struct.unpack('<H', file.read(2))[0]
            header = self.get_header(file, num_name_chars)
        return self.map_cls(header)

    def get_header(self, file, num_name_chars):
        name_bytes = struct.unpack(f'<{num_name_chars}s', file.read(num_name_chars))[0]
        name = bytes([byte for byte in name_bytes if byte]).decode()
        unpacked = struct.unpack('<HH', file.read(4))
        return Header(name, *unpacked)


if __name__ == '__main__':
    m = HavokMapReader()(sys.argv[1])
    print(m)
    print(m.header)
