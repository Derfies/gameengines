import struct
from dataclasses import dataclass
from typing import BinaryIO

from gameengines.build.map import MapBase, MapReaderBase, Sector, Sprite, Wall


MASTER_DECRYPT_KEY = 0x7474614d


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
    numsectors: int
    numwalls: int
    numsprites: int


class Map(MapBase):

    pre_header_fmt = '<4sh'
    header_fmt = '<iiihhhiiciHHH'
    header_cls = Header


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
    def pre_header_size(self) -> int:
        return struct.calcsize(self.map_cls.pre_header_fmt)

    def get_header(self, file: BinaryIO) -> Header:
        data = file.read(self.pre_header_size)
        signature, version = struct.unpack(self.map_cls.pre_header_fmt, data)
        version >>= 8
        data = file.read(self.header_size)
        unpacked = struct.unpack(self.map_cls.header_fmt, self.decrypt(bytearray(data), MASTER_DECRYPT_KEY))

        # TODO: Parse remaining data.
        file.seek(173)

        return self.map_cls.header_cls(signature, version, *unpacked)

    def get_numsectors(self, file: BinaryIO, header: Header) -> int:
        return header.numsectors

    def get_sectors(self, file: BinaryIO, numsectors: int, header: Header, decrypt_key: int | None = None) -> list[Sector]:
        return super().get_sectors(file, numsectors, header, decrypt_key=header.revision * self.sector_size)

    def get_numwalls(self, file: BinaryIO, header: Header) -> int:
        return header.numwalls

    def get_walls(self, file: BinaryIO, numwalls: int, header: Header, decrypt_key: int | None = None) -> list[Wall]:
        return super().get_walls(file, numwalls, header, decrypt_key=header.revision * self.sector_size | MASTER_DECRYPT_KEY)

    def get_numsprites(self, file: BinaryIO, header: Header) -> int:
        return header.numsprites

    def get_sprites(self, file: BinaryIO, numsprites: int, header: Header, decrypt_key: int | None = None) -> list[Sprite]:
        return super().get_sprites(file, numsprites, header, decrypt_key=header.revision * self.sprite_size | MASTER_DECRYPT_KEY)
