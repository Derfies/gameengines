import abc
import struct
import sys
from dataclasses import dataclass


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


class MapBase(metaclass=abc.ABCMeta):

    @property
    @abc.abstractmethod
    def header_cls(cls):
        """"""

    @property
    @abc.abstractmethod
    def sector_cls(cls):
        """"""

    @property
    @abc.abstractmethod
    def wall_cls(cls):
        """"""

    @property
    @abc.abstractmethod
    def sprite_cls(cls):
        """"""


class Duke3dMap(MapBase):

    header_cls = Header
    sector_cls = Sector
    wall_cls = Wall
    sprite_cls = Sprite

    def __init__(self, header=None, sectors=None, walls=None, sprites=None):

        # TODO: This is probably a base class concern? All build maps have this
        # I assume.
        self.header = header or self.header_cls(7, 0, 0, 0, 0, 0)
        self.sectors = sectors or []
        self.walls = walls or []
        self.sprites = sprites or []


class MapReaderBase(metaclass=abc.ABCMeta):

    """
    https://moddingwiki.shikadi.net/wiki/MAP_Format_(Build)
    https://fabiensanglard.net/duke3d/BUILDINF.TXT

    """

    @property
    @abc.abstractmethod
    def header_size(cls):
        """"""

    @property
    @abc.abstractmethod
    def sector_size(cls):
        """"""

    @property
    @abc.abstractmethod
    def wall_size(cls):
        """"""

    @property
    @abc.abstractmethod
    def sprite_size(cls):
        """"""

    @property
    @abc.abstractmethod
    def map_cls(cls):
        """"""

    def __call__(self, file_path):
        with open(file_path, 'rb') as file:
            header = self.get_header(file)
            numsectors = self.get_numsectors(file)
            sectors = self.get_sectors(file, numsectors)
            numwalls = self.get_numwalls(file)
            walls = self.get_walls(file, numwalls)
            numsprites = self.get_numsprites(file)
            sprites = self.get_sprites(file, numsprites)
        return self.map_cls(header, sectors, walls, sprites)

    def get_header(self, file):
        data = file.read(self.header_size)
        unpacked = struct.unpack('<iiiihh', data)
        return Header(*unpacked)

    def get_numsectors(self, file):
        return struct.unpack('<H', file.read(2))[0]

    def get_sectors(self, file, numsectors):
        sectors = []
        for _ in range(numsectors):
            data = file.read(self.sector_size)
            unpacked = struct.unpack('<hhiihhhhbBBBhhbBBBBBhhh', data)
            sectors.append(Sector(*unpacked))
        return sectors

    def get_numwalls(self, file):
        return struct.unpack('<H', file.read(2))[0]

    def get_walls(self, file, numwalls):
        walls = []
        for _ in range(numwalls):
            data = file.read(self.wall_size)
            unpacked = struct.unpack('<iihhhhhbBhBBBBhhh', data)
            walls.append(Wall(*unpacked))
        return walls

    def get_numsprites(self, file):
        return struct.unpack('<H', file.read(2))[0]

    def get_sprites(self, file, numsprites):
        sprites = []
        for _ in range(numsprites):
            data = file.read(self.sprite_size)
            unpacked = struct.unpack('<iiihhbBBBBBbbhhhhhhhhhh', data)
            sprites.append(Sprite(*unpacked))
        return sprites


class Duke3dMapReader(MapReaderBase):

    map_cls = Duke3dMap
    header_size = 20
    sector_size = 40
    wall_size = 32
    sprite_size = 44


if __name__ == '__main__':

    import time

    start = time.time()
    for i in range(1000):
        m = Duke3dMapReader()(sys.argv[1])
        foo = m.sectors[0].wallptr
        m.sectors[0].wallptr = 0
    end = time.time()
    print('total', end - start)
