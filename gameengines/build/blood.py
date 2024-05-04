import struct
from dataclasses import asdict, dataclass
from typing import BinaryIO

from gameengines.build.map import MapBase, MapReaderBase, MapWriterBase, Sector, Sprite, Wall


MASTER_CRYPT_KEY = 0x7474614d


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

    def get_header(self, file: BinaryIO, decrypt_key: int | None = None) -> Header:
        data = file.read(self.pre_header_size)
        signature, version = struct.unpack(self.map_cls.pre_header_fmt, data)
        version >>= 8
        data = bytearray(file.read(self.header_size))
        unpacked = struct.unpack(self.map_cls.header_fmt, self.decrypt(data, MASTER_CRYPT_KEY))

        # TODO: Parse remaining data.
        file.seek(173)

        return self.map_cls.header_cls(signature, version, *unpacked)

    def get_num_sectors(self, file: BinaryIO, header: Header) -> int:
        return header.numsectors

    def get_sectors(self, file: BinaryIO, num_sectors: int, header: Header, decrypt_key: int | None = None) -> list[Sector]:
        return super().get_sectors(file, num_sectors, header, decrypt_key=header.revision * self.sector_size)

    def get_num_walls(self, file: BinaryIO, header: Header) -> int:
        return header.numwalls

    def get_walls(self, file: BinaryIO, num_walls: int, header: Header, decrypt_key: int | None = None) -> list[Wall]:
        return super().get_walls(file, num_walls, header, decrypt_key=header.revision * self.sector_size | MASTER_CRYPT_KEY)

    def get_num_sprites(self, file: BinaryIO, header: Header) -> int:
        return header.numsprites

    def get_sprites(self, file: BinaryIO, num_sprites: int, header: Header, decrypt_key: int | None = None) -> list[Sprite]:
        return super().get_sprites(file, num_sprites, header, decrypt_key=header.revision * self.sprite_size | MASTER_CRYPT_KEY)


class MapWriter(MapWriterBase):

    map_cls = Map

    def write_header(self, m: MapBase, file: BinaryIO, encrypt_key: int | None = None):
        data = list(asdict(m.header).values())
        signature, version = data[:2]
        version <<= 8
        packed = bytearray(struct.pack(self.map_cls.pre_header_fmt, signature, version))
        file.write(packed)
        data = data[:-3] + [m.header.numsectors, m.header.numwalls, m.header.numsprites]
        packed = bytearray(struct.pack(self.map_cls.header_fmt, *data[2:]))
        file.write(self.encrypt(packed, MASTER_CRYPT_KEY))

    def write_num_sectors(self, m: MapBase, file: BinaryIO):
        pass

    def write_num_walls(self, m: MapBase, file: BinaryIO):
        pass

    def write_num_sprites(self, m: MapBase, file: BinaryIO):
        pass
