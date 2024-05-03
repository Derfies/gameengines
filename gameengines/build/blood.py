import struct
from dataclasses import dataclass

from gameengines.build.map import MapBase, Sector, Wall, Sprite, MapReaderBase


@dataclass(slots=True)
class Header:

    signature: str
    version: int
    posx: int
    posy: int
    posz: int
    ang: int
    cursectnum: int
    skybits: int
    visibility: int
    songid: int
    parallaxtype: int
    revision: int
    num_sectors: int
    num_walls: int
    num_sprites: int


class Map(MapBase):

    pre_header_fmt = '<4sh'
    header_fmt = '<iiihhhiiciHHH'
    header_cls = Header
    sector_fmt = '<iiihhhiiciHHH'
    sector_cls = Sector
    wall_fmt = '<iiihhhiiciHHH'
    wall_cls = Wall
    sprite_fmt = '<iiihhhiiciHHH'
    sprite_cls = Sprite

    def __init__(self, header=None, sectors=None, walls=None, sprites=None):
        self.header = header or self.header_cls(7, 0, 0, 0, 0, 0)
        self.sectors = sectors or []
        self.walls = walls or []
        self.sprites = sprites or []


class MapReader(MapReaderBase):

    """
    https://blood.sourceforge.net/rebuild.php

    """

    map_cls = Map

    @staticmethod
    def decrypt(data: bytearray, key: int) -> bytearray:
        """
        https://moddingwiki.shikadi.net/wiki/RFF_Format#:~:text=The%20RFF%20format%20is%20used,avoid%20extraction%20by%20ripping%20utilities.

        """
        key = key & 0xFF
        for i in range(len(data)):
            data[i] ^= key
            key += 1
        return data

    @property
    def pre_header_size(self):
        return struct.calcsize(self.map_cls.pre_header_fmt)

    def get_header(self, file):
        data = file.read(self.pre_header_size)
        signature, version = struct.unpack(self.map_cls.pre_header_fmt, data)
        version >>= 8
        data = file.read(self.header_size)
        unpacked = struct.unpack(self.map_cls.header_fmt, self.decrypt(bytearray(data), 0x7474614d))
        return self.map_cls.header_cls(signature, version, *unpacked)
