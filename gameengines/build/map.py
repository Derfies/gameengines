import abc
import struct
from dataclasses import dataclass
from typing import BinaryIO


@dataclass(slots=True)
class Header:

    version: int
    posx: int
    posy: int
    posz: int
    ang: int
    cursectnum: int


@dataclass(slots=True)
class Sector:

    wallptr: int
    wallnum: int
    ceilingz: int
    floorz: int
    ceilingstat: int
    floorstat: int
    ceilingpicnum: int
    ceilingheinum: int
    ceilingshade: int
    ceilingpal: int
    ceilingxpanning: int
    ceilingypanning: int
    floorpicnum: int
    floorheinum: int
    floorshade: int
    floorpal: int
    floorxpanning: int
    floorypanning: int
    visibility: int
    filler: int
    lotag: int
    hitag: int
    extra: int


@dataclass(slots=True)
class Wall:

    x: int
    y: int
    point2: int
    nextwall: int
    nextsector: int
    cstat: int
    picnum: int
    overpicnum: int
    shade: int
    pal: int
    xrepeat: int
    yrepeat: int
    xpanning: int
    ypanning: int
    lotag: int
    hitag: int
    extra: int


@dataclass(slots=True)
class Sprite:

    x: int
    y: int
    z: int
    cstat: int
    picnum: int
    shade: int
    pal: int
    clipdist: int
    filler: int
    xrepeat: int
    yrepeat: int
    xoffset: int
    yoffset: int
    sectnum: int
    statnum: int
    ang: int
    owner: int
    xvel: int
    yvel: int
    zvel: int
    lotag: int
    hitag: int
    extra: int


class MapBase:#(metaclass=abc.ABCMeta):

    header_fmt = '<iiiihh'
    header_cls = Header
    sector_fmt = '<hhiihhhhbBBBhhbBBBBBhhh'
    sector_cls = Sector
    wall_fmt = '<iihhhhhbBhBBBBhhh'
    wall_cls = Wall
    sprite_fmt = '<iiihhbBBBBBbbhhhhhhhhhh'
    sprite_cls = Sprite

    def __init__(self, header=None, sectors=None, walls=None, sprites=None, version=7):
        self.header = header or self.header_cls(version, 0, 0, 0, 0, 0)
        self.sectors = sectors or []
        self.walls = walls or []
        self.sprites = sprites or []


class MapReaderBase(metaclass=abc.ABCMeta):

    """
    https://moddingwiki.shikadi.net/wiki/MAP_Format_(Build)
    https://fabiensanglard.net/duke3d/BUILDINF.TXT

    """

    @property
    def header_size(self):
        return struct.calcsize(self.map_cls.header_fmt)

    @property
    def sector_size(self):
        return struct.calcsize(self.map_cls.sector_fmt)

    @property
    def wall_size(self):
        return struct.calcsize(self.map_cls.wall_fmt)

    @property
    def sprite_size(self):
        return struct.calcsize(self.map_cls.sprite_fmt)

    @property
    @abc.abstractmethod
    def map_cls(cls):
        ...

    def __call__(self, file_path: str) -> MapBase:
        with open(file_path, 'rb') as file:
            header = self.get_header(file)
            numsectors = self.get_numsectors(file, header)
            sectors = self.get_sectors(file, numsectors, header)
            numwalls = self.get_numwalls(file, header)
            walls = self.get_walls(file, numwalls, header)
            numsprites = self.get_numsprites(file, header)
            sprites = self.get_sprites(file, numsprites, header)
        return self.map_cls(header, sectors, walls, sprites)

    @staticmethod
    def decrypt(data: bytearray, key: int | None) -> bytearray:
        return data

    def get_header(self, file: BinaryIO) -> Header:
        data = file.read(struct.calcsize(self.map_cls.header_fmt))
        unpacked = struct.unpack(self.map_cls.header_fmt, data)
        return self.map_cls.header_cls(*unpacked)

    def get_numsectors(self, file: BinaryIO, header: Header) -> int:
        return struct.unpack('<H', file.read(2))[0]

    def get_sectors(self, file: BinaryIO, numsectors: int, header: Header, decrypt_key: int | None = None) -> list[Sector]:
        sectors = []
        for _ in range(numsectors):
            data = bytearray(file.read(self.sector_size))
            unpacked = struct.unpack(self.map_cls.sector_fmt, self.decrypt(data, decrypt_key))
            sectors.append(Sector(*unpacked))
        return sectors

    def get_numwalls(self, file: BinaryIO, header: Header) -> int:
        return struct.unpack('<H', file.read(2))[0]

    def get_walls(self, file: BinaryIO, numwalls: int, header: Header, decrypt_key: int | None = None) -> list[Wall]:
        walls = []
        for _ in range(numwalls):
            data = bytearray(file.read(self.wall_size))
            unpacked = struct.unpack(self.map_cls.wall_fmt, self.decrypt(data, decrypt_key))
            walls.append(Wall(*unpacked))
        return walls

    def get_numsprites(self, file: BinaryIO, header: Header) -> int:
        return struct.unpack('<H', file.read(2))[0]

    def get_sprites(self, file: BinaryIO, numsprites: int, header: Header, decrypt_key: int | None = None) -> list[Sprite]:
        sprites = []
        for _ in range(numsprites):
            data = bytearray(file.read(self.sprite_size))
            unpacked = struct.unpack(self.map_cls.sprite_fmt, self.decrypt(data, decrypt_key))
            sprites.append(Sprite(*unpacked))
        return sprites
