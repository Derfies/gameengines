import ctypes
import io
import logging
import struct

import numpy as np

from gameengines.build.structures import ArtHeader, StructureBase


logger = logging.getLogger(__name__)


class Grp:

    def __init__(self):
        self.arts = []
        self.textures = []
        self.maps = {}

    def load(self, file_path: str):
        with open(file_path, 'rb') as f:
            magic = f.read(12).rstrip(b'\0')
            if magic != b'KenSilverman':
                raise ValueError('Not a GRP file')

            numfiles = struct.unpack('<I', f.read(4))[0]
            entries = []
            for _ in range(numfiles):
                name = f.read(12).decode('ascii').rstrip('\0')
                size = struct.unpack('<I', f.read(4))[0]
                entries.append((name, size))

            for name_ext, size in entries:
                name = name_ext.split('.')[0]
                #print('FOUND:', name)
                data = f.read(size)
                if name_ext.lower().endswith('.art'):
                    self.textures.extend(self.load_art(data))
                elif name_ext.lower().endswith('.map'):
                    try:
                        self.maps[name] = self.load_map(data)
                    except:
                        print('FAILED:', name_ext)

    def load_art(self, data):

        textures = []
        stream = io.BytesIO(data)
        header = ArtHeader.from_stream(stream)

        numtiles = header.localtileend - header.localtilestart + 1

        class ArtHeader2(StructureBase):

            _fields_ = (
                ('tilesizx',    ctypes.c_int16 * numtiles),
                ('tilesizy',    ctypes.c_int16 * numtiles),
                ('picanm',      ctypes.c_int32 * numtiles),
            )

        header2 = ArtHeader2.from_stream(stream)

        for i in range(numtiles):
            w, h = header2.tilesizx[i], header2.tilesizy[i]
            indices = np.frombuffer(stream.read(w * h), dtype=np.uint8)
            textures.append(indices.reshape((w, h)).transpose())

        return textures
