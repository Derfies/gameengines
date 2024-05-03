import abc
import struct
from dataclasses import dataclass


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

    def __init_subclass__(cls, **kwargs):

        # TODO: Turn into decorator.
        missing = [
            required
            for required in (
                'header_fmt',
                'header_cls',
                'sector_fmt',
                'sector_cls',
                'wall_fmt',
                'wall_cls',
                'sprite_fmt',
                'sprite_cls',
            )
            if not hasattr(cls, required)
        ]
        if missing:
            raise TypeError(f"Can't instantiate abstract class {cls.__name__} without {', '.join(missing)} attributes")
        return super().__init_subclass__(**kwargs)


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
        raise
        return struct.calcsize(self.map_cls.header_fmt)

    @property
    def wall_size(self):
        raise
        return struct.calcsize(self.map_cls.header_fmt)

    @property
    def sprite_size(self):
        raise
        return struct.calcsize(self.map_cls.header_fmt)

    @property
    @abc.abstractmethod
    def map_cls(cls):
        ...

    def __call__(self, file_path: str):
        with open(file_path, 'rb') as file:
            header = self.get_header(file)
            print('header:', header)
            numsectors = self.get_numsectors(file)
            sectors = self.get_sectors(file, numsectors)
            numwalls = self.get_numwalls(file)
            walls = self.get_walls(file, numwalls)
            numsprites = self.get_numsprites(file)
            sprites = self.get_sprites(file, numsprites)
        return self.map_cls(header, sectors, walls, sprites)

    def get_header(self, file):
        data = file.read(struct.calcsize(self.map_cls.header_fmt))
        unpacked = struct.unpack(self.map_cls.header_fmt, data)
        return self.map_cls.header_cls(*unpacked)

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


if __name__ == '__main__':
    class Foo(MapBase): pass
    Foo()
    #
    # import time
    #
    # start = time.time()
    # for i in range(1000):
    #     m = Duke3dMapReader()(sys.argv[1])
    #     foo = m.sectors[0].wallptr
    #     m.sectors[0].wallptr = 0
    # end = time.time()
    # print('total', end - start)

    # with open(r'/gameengines/build/tests/data\maps\blood_map.MAP', 'rb') as f:
    #     data = f.read()
    #
    # print(data[:4])