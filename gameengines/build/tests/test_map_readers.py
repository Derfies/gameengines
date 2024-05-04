import io
import unittest
from pathlib import Path

from gameengines.build.blood import MapReader as BloodMapReader, MapWriter as BloodMapWriter
from gameengines.build.duke3d import MapReader as Duke3dMapReader, MapWriter as Duke3dMapWriter
from gameengines.build.map import MapWriterBase


class TestMapReaders(unittest.TestCase):

    # def test_blood_read(self):
    #     file_path = Path(__file__).parent.joinpath(r'data\blood.map')
    #     with open(file_path, 'rb') as file:
    #         m = BloodMapReader()(file)
    #     self.assertEqual(1, m.header.numsectors)
    #     self.assertEqual(1, len(m.sectors))
    #     self.assertEqual(4, m.header.numwalls)
    #     self.assertEqual(4, len(m.walls))
    #     self.assertEqual(1, m.header.numsprites)
    #     self.assertEqual(1, len(m.sprites))
    #
    #     print('Blood')
    #     for sprite in m.sprites:
    #         print(sprite)
    #
    # def test_duke3d_read(self):
    #     file_path = Path(__file__).parent.joinpath(r'data\duke3d.map')
    #     with open(file_path, 'rb') as file:
    #         m = Duke3dMapReader()(file)
    #     self.assertEqual(1, len(m.sectors))
    #     self.assertEqual(4, len(m.walls))
    #     self.assertEqual(0, len(m.sprites))
    #
    #     print('Duke3d')
    #     for sprite in m.sprites:
    #         print(sprite)

    def test_blood_round_trip(self):
        file_path = Path(__file__).parent.joinpath(r'data\blood.map')
        with open(file_path, 'rb') as file:
            input = io.BytesIO(file.read())
            m = BloodMapReader()(input)

        # for s in m.sectors:
        #     print(s)
        #
        # for s in m.walls:
        #     print(s)
        #
        # for s in m.sprites:
        #     print(s)

        output = io.BytesIO()
        BloodMapWriter()(m, output)
        input.seek(0)
        output.seek(0)
        stop = 200
        print('input:', input.read()[:stop])
        print('output:', output.read()[:stop])
        input.seek(0)
        output.seek(0)
        self.assertEqual(input.read()[:stop], output.read()[:stop])

    # def test_duke3d_round_trip(self):
    #     file_path = Path(__file__).parent.joinpath(r'data\duke3d.map')
    #     with open(file_path, 'rb') as file:
    #         input = io.BytesIO(file.read())
    #         m = Duke3dMapReader()(input)
    #     output = io.BytesIO()
    #     Duke3dMapWriter()(m, output)
    #     input.seek(0)
    #     output.seek(0)
    #     self.assertEqual(input.read(), output.read())
