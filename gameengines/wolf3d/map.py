import struct
import sys

import numpy as np


HAVOC_MAP_FORMAT = 'HWE1.0'


class Wolf3dMap:

    def __init__(self, name='New Map', width=64, height=64, num_planes=3):
        self.name = name
        self.tiles = np.zeros((width, height, num_planes), dtype='<i2')


class HavocMapReader:

    def __call__(self, file_path: str):
        with open(file_path, 'rb') as file:

            # These first bytes are more to do with the reader than the map itself.
            format = struct.unpack('<6s', file.read(6))[0].decode()
            assert format == HAVOC_MAP_FORMAT, f'Not a valid Havoc map format: {format}'
            unknown1 = struct.unpack('<H', file.read(2))[0]
            unknown2 = struct.unpack('<H', file.read(2))[0]

            num_planes = self.get_num_planes(file)
            num_chars = self.get_num_chars(file)
            name = self.get_name(file, num_chars)
            width, height = self.get_dimensions(file)
            tiles = self.get_tiles(file, num_planes, width, height)
        map_ = Wolf3dMap(name, width, height, num_planes)
        map_.tiles[:] = tiles
        return map_
    
    def get_num_planes(self, file):
        return struct.unpack('<H', file.read(2))[0]

    def get_num_chars(self, file):
        return struct.unpack('<H', file.read(2))[0]

    def get_name(self, file, num_chars):
        name_bytes = struct.unpack(f'<{num_chars}s', file.read(num_chars))[0]
        name = bytes([byte for byte in name_bytes if byte]).decode()
        return name
    
    def get_dimensions(self, file):
        return struct.unpack('<HH', file.read(4))

    def get_tiles(self, file, num_planes, width, height):
        data = np.frombuffer(file.read(), dtype='<i2')
        reshaped = data.reshape((num_planes, width, height))
        transposed = reshaped.transpose(2, 1, 0)
        return np.array(transposed)


class HavocMapWriter:

    def __call__(self, map_: Wolf3dMap, file_path: str):
        with open(file_path, 'wb') as file:

            # These first bytes are more to do with the reader than the map itself.
            file.write(struct.pack('<6s', HAVOC_MAP_FORMAT.encode('ascii')))
            file.write(struct.pack('<H', 1))
            file.write(struct.pack('<H', 0))

            file.write(self.get_num_planes(map_))
            file.write(self.get_num_chars(map_))
            file.write(self.get_name(map_))
            file.write(self.get_dimensions(map_))
            file.write(self.get_tiles(map_))

    def get_num_planes(self, map_: Wolf3dMap):
        return struct.pack('<H', map_.tiles.shape[2])

    def get_num_chars(self, map_: Wolf3dMap):
        return struct.pack('<H', 16 if len(map_.name) < 16 else 32)

    def get_name(self, map_: Wolf3dMap):
        max_chars = 16 if len(map_.name) < 16 else 32
        name = struct.pack(f'<{len(map_.name)}s', map_.name.encode('ascii'))
        return name.ljust(max_chars, b'\x00')

    def get_dimensions(self, map_: Wolf3dMap):
        width, height = map_.tiles.shape[0:2]
        return struct.pack('<HH', width, height)

    def get_tiles(self, map_: Wolf3dMap):
        transposed = map_.tiles.transpose(2, 1, 0)
        return transposed.reshape(-1)


if __name__ == '__main__':
    m1 = HavocMapReader()(sys.argv[1])
    # HavocMapWriter()(m1, sys.argv[2])
    # m2 = HavocMapReader()(sys.argv[2])
    #
    # print('name:', m1.name, m2.name)
    # print('tiles:', m1.tiles.shape, m2.tiles.shape)

    m = Wolf3dMap('test', width=32, height=64)
    # print(m.name)
    # print(m.tiles)

    for x in range(10):
        for y in range(20):
            m.tiles[x][y][0] = 1

    HavocMapWriter()(m, sys.argv[2])