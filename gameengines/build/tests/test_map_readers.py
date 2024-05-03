import unittest
from pathlib import Path

from gameengines.build.blood import MapReader as BloodMapReader
from gameengines.build.duke3d import MapReader as Duke3dMapReader


class TestMapReaders(unittest.TestCase):

    def test_blood(self):
        path = Path(__file__).parent.joinpath(r'data\blood.map')
        m = BloodMapReader()(path)
        self.assertEqual(1, m.header.numsectors)
        self.assertEqual(1, len(m.sectors))
        self.assertEqual(4, m.header.numwalls)
        self.assertEqual(4, len(m.walls))
        self.assertEqual(1, m.header.numsprites)
        self.assertEqual(1, len(m.sprites))

        print('Blood')
        for sprite in m.sprites:
            print(sprite)

    def test_duke3d(self):
        path = Path(__file__).parent.joinpath(r'data\duke3d.map')
        m = Duke3dMapReader()(path)
        self.assertEqual(1, len(m.sectors))
        self.assertEqual(4, len(m.walls))
        self.assertEqual(0, len(m.sprites))

        print('Duke3d')
        for sprite in m.sprites:
            print(sprite)