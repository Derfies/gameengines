import binascii
import struct
from dataclasses import asdict, dataclass
from typing import BinaryIO

from gameengines.build.map import MapBase, MapReaderBase, MapWriterBase, Sector, Sprite as SpriteBase, Wall


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

    # HAXXOR
    # Not sure what to do with this yet.
    pre_padding: bytes = None
    x_sprite_size: int = None
    x_wall_size: int = None
    x_sector_size: int = None
    post_padding: bytes = None


class Sprite(SpriteBase):

    # TODO: Make this the base class.

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.extra_data = None


class Map(MapBase):

    pre_header_fmt = '<4sh'
    header_fmt = '<iiihhhiiciHHH'
    header_cls = Header
    sprite_cls = Sprite




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

    def get_sprite(self, file: BinaryIO, header: Header, decrypt_key: int | None = None):
        sprite = super().get_sprite(file, header, decrypt_key)
        if sprite.extra > 0:
            sprite.extra_data = file.read(header.x_sprite_size)
        return sprite

    def get_sprites(self, file: BinaryIO, num_sprites: int, header: Header, decrypt_key: int | None = None) -> list[Sprite]:
        return super().get_sprites(file, num_sprites, header, decrypt_key=header.revision * self.sprite_size | MASTER_CRYPT_KEY)


class MapWriter(MapWriterBase):

    map_cls = Map

    def __call__(self, m: MapBase, file: BinaryIO):
        super().__call__(m, file)
        self.write_footer(m, file)

    @staticmethod
    def encrypt(data: bytearray, key: int | None) -> bytearray:
        """
        https://moddingwiki.shikadi.net/wiki/RFF_Format#:~:text=The%20RFF%20format%20is%20used,avoid%20extraction%20by%20ripping%20utilities.

        """
        if key is not None:
            key = key & 0xFF
            for i in range(len(data)):
                data[i] ^= key
                key += 1
        return data

    def write_header(self, m: MapBase, file: BinaryIO, encrypt_key: int | None = None):

        data = list(asdict(m.header).values())

        signature, version = data[:2]
        version <<= 8
        packed = bytearray(struct.pack(self.map_cls.pre_header_fmt, signature, version))
        file.write(packed)


        packed = bytearray(struct.pack(self.map_cls.header_fmt, *data[2:-5]))
        file.write(self.encrypt(packed, MASTER_CRYPT_KEY))


        foo = bytearray()
        foo.extend(m.header.pre_padding)
        sizes = struct.pack('<iii', m.header.x_sprite_size, m.header.x_wall_size, m.header.x_sector_size)
        foo.extend(sizes)
        foo.extend(m.header.post_padding)

        self.encrypt(foo, m.header.numwalls)

        file.write(foo)

    def write_num_sectors(self, m: MapBase, file: BinaryIO):
        pass

    def write_sectors(self, m: MapBase, file: BinaryIO, encrypt_key: int | None = None):
        super().write_sectors(m, file, encrypt_key=m.header.revision * self.sector_size)

    def write_num_walls(self, m: MapBase, file: BinaryIO):
        pass

    def write_walls(self, m: MapBase, file: BinaryIO, encrypt_key: int | None = None):
        super().write_walls(m, file, encrypt_key=m.header.revision * self.sector_size | MASTER_CRYPT_KEY)

    def write_num_sprites(self, m: MapBase, file: BinaryIO):
        pass

    def write_sprites(self, m: MapBase, file: BinaryIO, encrypt_key: int | None = None):
        super().write_sprites(m, file, encrypt_key=m.header.revision * self.sprite_size | MASTER_CRYPT_KEY)

    def write_footer(self, m: MapBase, file: BinaryIO):
        position = file.tell()
        file.seek(0)
        data = file.read()
        file.seek(position)
        crc = binascii.crc32(data)
        #self.hash = struct.pack('<I', crc)
        #self.data.extend(self.hash)
        file.write(struct.pack('<I', crc))
