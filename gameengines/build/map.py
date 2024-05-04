import abc
import struct
from dataclasses import asdict, dataclass, fields
from typing import BinaryIO


@dataclass
class Header:

    version: int = 7
    posx: int = 0
    posy: int = 0
    posz: int = 0
    ang: int = 0
    cursectnum: int = 0


@dataclass
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

    def __post_init__(self, *args, **kwargs):
        self.extra_data = None


@dataclass
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

    def __post_init__(self):
        self.extra_data = None


@dataclass
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

    def __post_init__(self):
        self.extra_data = None


class MapBase:

    header_fmt = '<iiiihh'
    header_cls = Header
    sector_fmt = '<hhiihhhhbBBBhhbBBBBBhhh'
    sector_cls = Sector
    wall_fmt = '<iihhhhhbBhBBBBhhh'
    wall_cls = Wall
    sprite_fmt = '<iiihhbBBBBBbbhhhhhhhhhh'
    sprite_cls = Sprite

    def __init__(self, header=None, sectors=None, walls=None, sprites=None):
        self.header = header or self.header_cls()
        self.sectors = sectors or []
        self.walls = walls or []
        self.sprites = sprites or []

    @classmethod
    def from_map(cls, m: 'MapBase'):
        new_header_field_names = [f.name for f in fields(cls.header_cls)]
        new_header_data = {key: value for key, value in asdict(m.header).items() if key in new_header_field_names}
        header = cls.header_cls(**new_header_data)
        sectors = [cls.sector_cls(**asdict(sector)) for sector in m.sectors]
        walls = [cls.wall_cls(**asdict(sector)) for sector in m.walls]
        sprites = [cls.sprite_cls(**asdict(sector)) for sector in m.sprites]
        return cls(header, sectors, walls, sprites)


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

    def __call__(self, file: BinaryIO) -> MapBase:

        # TODO: Convert all file vars to 'stream'
        # TODO: Maybe 'num_something' is actually a member on this class...
        # Would solve a slight artchitecture smell...
        header = self.get_header(file)
        num_sectors = self.get_num_sectors(file, header)
        sectors = self.get_sectors(file, num_sectors, header)
        num_walls = self.get_num_walls(file, header)
        walls = self.get_walls(file, num_walls, header)
        num_sprites = self.get_num_sprites(file, header)
        sprites = self.get_sprites(file, num_sprites, header)
        return self.map_cls(header, sectors, walls, sprites)

    @staticmethod
    def decrypt(data: bytearray, key: int | None) -> bytearray:
        return data

    def get_header(self, file: BinaryIO, decrypt_key: int | None = None) -> Header:
        data = bytearray(file.read(self.header_size))
        unpacked = struct.unpack(self.map_cls.header_fmt, self.decrypt(data, decrypt_key))
        return self.map_cls.header_cls(*unpacked)

    def get_num_sectors(self, file: BinaryIO, header: Header) -> int:
        return struct.unpack('<H', file.read(2))[0]

    def get_sectors(self, file: BinaryIO, num_sectors: int, header: Header, decrypt_key: int | None = None) -> list[Sector]:
        sectors = []
        for _ in range(num_sectors):
            data = bytearray(file.read(self.sector_size))
            unpacked = struct.unpack(self.map_cls.sector_fmt, self.decrypt(data, decrypt_key))
            sectors.append(self.map_cls.sector_cls(*unpacked))
        return sectors

    def get_num_walls(self, file: BinaryIO, header: Header) -> int:
        return struct.unpack('<H', file.read(2))[0]

    def get_walls(self, file: BinaryIO, num_walls: int, header: Header, decrypt_key: int | None = None) -> list[Wall]:
        walls = []
        for _ in range(num_walls):
            data = bytearray(file.read(self.wall_size))
            unpacked = struct.unpack(self.map_cls.wall_fmt, self.decrypt(data, decrypt_key))
            walls.append(self.map_cls.wall_cls(*unpacked))
        return walls

    def get_num_sprites(self, file: BinaryIO, header: Header) -> int:
        return struct.unpack('<H', file.read(2))[0]

    def get_sprites(self, file: BinaryIO, num_sprites: int, header: Header, decrypt_key: int | None = None) -> list[Sprite]:
        sprites = []
        for _ in range(num_sprites):
            data = bytearray(file.read(self.sprite_size))
            unpacked = struct.unpack(self.map_cls.sprite_fmt, self.decrypt(data, decrypt_key))
            sprite = self.map_cls.sprite_cls(*unpacked)
            if sprite.extra > 0:
                sprite.extra_data = file.read(header.x_sprite_size)
            sprites.append(sprite)
        return sprites


class MapWriterBase(metaclass=abc.ABCMeta):

    """
    https://moddingwiki.shikadi.net/wiki/mFormat_(Build)
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

    def __call__(self, m: MapBase, file: BinaryIO):
        self.write_header(m, file)
        self.write_num_sectors(m, file)
        self.write_sectors(m, file)
        self.write_num_walls(m, file)
        self.write_walls(m, file)
        self.write_num_sprites(m, file)
        self.write_sprites(m, file)

    @staticmethod
    def encrypt(data: bytes, key: int | None) -> bytes:
        return data

    def write_header(self, m: MapBase, file: BinaryIO, encrypt_key: int | None = None):
        data = asdict(m.header).values()
        packed = struct.pack(self.map_cls.header_fmt, *data)
        file.write(self.encrypt(packed, encrypt_key))

    def write_num_sectors(self, m: MapBase, file: BinaryIO):
        data = len(m.sectors)
        file.write(struct.pack('<H', data))

    def write_sectors(self, m: MapBase, file: BinaryIO, encrypt_key: int | None = None):
        for sector in m.sectors:
            data = asdict(sector).values()
            packed = struct.pack(self.map_cls.sector_fmt, *data)
            file.write(self.encrypt(packed, encrypt_key))
            if sector.extra > 0:
                file.write(sector.extra_data)

    def write_num_walls(self, m: MapBase, file: BinaryIO):
        data = len(m.walls)
        file.write(struct.pack('<H', data))

    def write_walls(self, m: MapBase, file: BinaryIO, encrypt_key: int | None = None):
        for wall in m.walls:
            data = asdict(wall).values()
            packed = struct.pack(self.map_cls.wall_fmt, *data)
            file.write(self.encrypt(packed, encrypt_key))
            if wall.extra > 0:
                file.write(wall.extra_data)

    def write_num_sprites(self, m: MapBase, file: BinaryIO):
        data = len(m.sprites)
        file.write(struct.pack('<H', data))

    def write_sprites(self, m: MapBase, file: BinaryIO, encrypt_key: int | None = None):
        for sprite in m.sprites:
            data = asdict(sprite).values()
            packed = struct.pack(self.map_cls.sprite_fmt, *data)
            file.write(self.encrypt(packed, encrypt_key))

            # TODO: Conversion breaks here.
            if sprite.extra > 0 and sprite.extra_data is not None:
                file.write(sprite.extra_data)
