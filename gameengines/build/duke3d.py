from dataclasses import dataclass

from gameengines.build.map import MapBase, Sector, Wall, Sprite, MapReaderBase


@dataclass(slots=True)
class Header:

    version: int
    posx: int
    posy: int
    posz: int
    ang: int
    cursectnum: int


class Map(MapBase):

    header_fmt = '<iiiihh'
    header_cls = Header
    sector_fmt = '<hhiihhhhbBBBhhbBBBBBhhh'
    sector_cls = Sector
    wall_fmt = '<iihhhhhbBhBBBBhhh'
    wall_cls = Wall
    sprite_fmt = '<iiihhbBBBBBbbhhhhhhhhhh'
    sprite_cls = Sprite

    def __init__(self, header=None, sectors=None, walls=None, sprites=None):

        # TODO: This might belong in base class.
        self.header = header or self.header_cls(7, 0, 0, 0, 0, 0)
        self.sectors = sectors or []
        self.walls = walls or []
        self.sprites = sprites or []


class MapReader(MapReaderBase):

    map_cls = Map
