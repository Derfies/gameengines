import binascii
import struct
from dataclasses import asdict, dataclass
from typing import BinaryIO

from gameengines.build.map import Map as MapBase, MapReaderBase, MapWriterBase, Sector, Sprite, Wall


MASTER_CRYPT_KEY = 0x7474614d


@dataclass(slots=True)
class Header:

    signature: bytes = b'BLM\x1a'
    version: int = 7
    posx: int = 0
    posy: int = 0
    posz: int = 0
    ang: int = 0
    cursectnum: int = 0
    skybits: int = 0
    visibility: int = 0
    songid: int = 0
    parallaxtype: bytes = b'\x02'
    revision: int = 0
    numsectors: int = 0
    numwalls: int = 0
    numsprites: int = 0

    # HAXXOR
    # Not sure what to do with this yet.
    pre_padding: bytes = b'Copyright 1997 Monolith Productions.  All Rights Reserved\x00\x00\x00\x00\x00\x00\x00'
    x_sprite_size: int = 56
    x_wall_size: int = 24
    x_sector_size: int = 60
    post_padding: bytes = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x86\x86'


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
    def decrypt(data: bytearray, key: int | None) -> bytearray:
        """
        https://moddingwiki.shikadi.net/wiki/RFF_Format#:~:text=The%20RFF%20format%20is%20used,avoid%20extraction%20by%20ripping%20utilities.

        """
        if key is not None:
            data = bytearray(data)
            for index in range(len(data)):
                data[index] ^= (key + index) & 0xFF
            return bytes(data)
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

        header = self.map_cls.header_cls(signature, version, *unpacked)


        data = self.decrypt(bytearray(file.read(130)), header.numwalls)
        header.x_sprite_size, header.x_wall_size, header.x_sector_size = struct.unpack('<iii', data[64:76])

        # TODO: Parse remaining data.
        header.pre_padding = bytearray(data[:64])   # Copyright
        header.post_padding = bytearray(data[76:])  # Null bytes
        return header

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

    def __call__(self, m: Map, file: BinaryIO):
        super().__call__(m, file)
        self.write_crc(m, file)

    @staticmethod
    def encrypt(data: bytes, key: int | None) -> bytes:
        """
        https://moddingwiki.shikadi.net/wiki/RFF_Format#:~:text=The%20RFF%20format%20is%20used,avoid%20extraction%20by%20ripping%20utilities.

        """
        if key is not None:
            data = bytearray(data)
            for index in range(len(data)):
                data[index] ^= (key + index) & 0xFF
            return bytes(data)
        return data

    def write_header(self, m: Map, file: BinaryIO, encrypt_key: int | None = None):

        # HAXXOR
        # Need to set the head numbers.
        m.header.numsectors = len(m.sectors)
        m.header.numwalls = len(m.walls)
        m.header.numsprites = len(m.sprites)

        data = list(asdict(m.header).values())

        signature, version = data[:2]
        version <<= 8
        packed = bytearray(struct.pack(self.map_cls.pre_header_fmt, signature, version))
        file.write(packed)

        # TODO: This isn't currently picking up new num_ values.
        packed = bytearray(struct.pack(self.map_cls.header_fmt, *data[2:-5]))
        file.write(self.encrypt(packed, MASTER_CRYPT_KEY))


        foo = bytearray()
        foo.extend(m.header.pre_padding)
        sizes = struct.pack('<iii', m.header.x_sprite_size, m.header.x_wall_size, m.header.x_sector_size)
        foo.extend(sizes)
        foo.extend(m.header.post_padding)



        file.write(self.encrypt(foo, m.header.numwalls))

    def write_num_sectors(self, m: Map, file: BinaryIO):
        pass

    def write_sectors(self, m: Map, file: BinaryIO, encrypt_key: int | None = None):
        super().write_sectors(m, file, encrypt_key=m.header.revision * self.sector_size)

    def write_num_walls(self, m: Map, file: BinaryIO):
        pass

    def write_walls(self, m: Map, file: BinaryIO, encrypt_key: int | None = None):
        super().write_walls(m, file, encrypt_key=m.header.revision * self.sector_size | MASTER_CRYPT_KEY)

    def write_num_sprites(self, m: Map, file: BinaryIO):
        pass

    def write_sprites(self, m: Map, file: BinaryIO, encrypt_key: int | None = None):
        super().write_sprites(m, file, encrypt_key=m.header.revision * self.sprite_size | MASTER_CRYPT_KEY)

    def write_crc(self, m: Map, file: BinaryIO):
        crc = binascii.crc32(file.getbuffer())
        file.write(struct.pack('<I', crc))
