import unittest
from pathlib import Path

from gameengines.build.blood import MapReader as BloodMapReader
from gameengines.build.duke3d import MapReader as Duke3dMapReader


class TestMapReaders(unittest.TestCase):

    def test_blood(self):
        path = Path(__file__).parent.joinpath(r'data\blood.map')
        BloodMapReader()(path)

    def test_duke3d(self):
        path = Path(__file__).parent.joinpath(r'data\duke3d.map')
        Duke3dMapReader()(path)
