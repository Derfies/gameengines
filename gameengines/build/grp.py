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
        self.maps = []

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

            for name, size in entries:
                print('FOUND:', name)
                data = f.read(size)
                if name.lower().endswith('.art'):
                    self.textures.extend(self.load_art(data))
                #     print('FOUND:', name)
                #     data = f.read(size)
                #     #art_files.append(data)
                #     # return data
                # else:
                #     f.seek(size, 1)


                #entries.append(GRPEntry(name=name, size=size, data=data))

        #     numfiles = struct.unpack('<I', f.read(4))[0]
        #     entries = []
        #     for _ in range(numfiles):
        #         name = f.read(12).decode('ascii').rstrip('\0')
        #         size = struct.unpack('<I', f.read(4))[0]
        #         entries.append((name, size))
        #
        #     for name, size in entries:
        #         data = f.read(size)
        #         if name.lower().endswith('.art'):
        #             logger.debug(f'Loading art: {name}')
        #             self.load_art(data)
        #
        #         #print(name, size)
        #         # if name.lower() == target_filename.lower():
        #         #     #data = f.read(size)
        #         #     #return data
        #         # else:
        #         f.seek(size, 1)
        # #raise FileNotFoundError(f'{target_filename} not found in GRP')


    # def get_art_files(grp_path):
    #
    #     art_files = []
    #
    #     # TODO: Move to duke tools.
    #     with open(grp_path, 'rb') as f:
    #         magic = f.read(12).rstrip(b'\0')
    #         if magic != b'KenSilverman':
    #             raise ValueError('Not a GRP file')
    #
    #         numfiles = struct.unpack('<I', f.read(4))[0]
    #         entries = []
    #         for _ in range(numfiles):
    #             name = f.read(12).decode('ascii').rstrip('\0')
    #             size = struct.unpack('<I', f.read(4))[0]
    #             entries.append((name, size))
    #
    #         for name, size in entries:
    #             if name.lower().endswith('.art'):
    #                 print('FOUND:', name)
    #                 data = f.read(size)
    #                 art_files.append(data)
    #                 #return data
    #             else:
    #                 f.seek(size, 1)
    #
    #     return art_files
    #     #raise FileNotFoundError(f'{target_filename} not found in GRP')

    def load_art(self, data):

        textures = []
        #palette = load_palette(palette_path)

        # TODO: Scan grp file and extract all tiles.
        #art_datas = get_art_files(grp_path)
        #for art_data in art_datas:#[0:2]:
        stream = io.BytesIO(data)
        header = ArtHeader.from_stream(stream)

        numtiles = header.localtileend - header.localtilestart

        class ArtHeader2(StructureBase):

            _fields_ = (
                ('tilesizx',    ctypes.c_int16 * (numtiles + 1)),
                ('tilesizy',    ctypes.c_int16 * (numtiles + 1)),
                ('picanm',      ctypes.c_int32 * (numtiles + 1)),
            )

        header2 = ArtHeader2.from_stream(stream)


        for i in range(numtiles):
            w, h = header2.tilesizx[i], header2.tilesizy[i]
            #print(i, '->', w, h)
            indices = np.frombuffer(stream.read(w * h), dtype=np.uint8)
            # try:
            #     #array = indices.reshape((w , h))
            #     #textures.append(palette[array])
            # except Exception as e:
            #     print(e)
            #     pass
            textures.append(indices.reshape((w, h)))

        return textures
