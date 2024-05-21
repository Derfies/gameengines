import io

from gameengines.build.blood import Map, MapWriter as BloodMapWriter
from gameengines.build.duke3d import MapWriter as Duke3dMapWriter
from gameengines.build.map import Sector, Sprite, Wall, MapWriterBase, MapBase


map_cls = Map


DEFAULT_MAP_SIZE = 2048


m = map_cls()

new_sector = Sector()
new_sector.floorz = DEFAULT_MAP_SIZE * 16
new_sector.ceilingz = -DEFAULT_MAP_SIZE * 16
new_sector.wallptr = 0
new_sector.wallnum = 4
m.sectors.append(new_sector)

wall_1 = Wall()
wall_1.x = -DEFAULT_MAP_SIZE
wall_1.y = -DEFAULT_MAP_SIZE
wall_1.xrepeat = 32
wall_1.yrepeat = 8
wall_1.point2 = 1
m.walls.append(wall_1)

wall_2 = Wall()
wall_2.x = DEFAULT_MAP_SIZE
wall_2.y = -DEFAULT_MAP_SIZE
wall_2.xrepeat = 32
wall_2.yrepeat = 8
wall_2.point2 = 2
m.walls.append(wall_2)

wall_3 = Wall()
wall_3.x = DEFAULT_MAP_SIZE
wall_3.y = DEFAULT_MAP_SIZE
wall_3.xrepeat = 32
wall_3.yrepeat = 8
wall_3.point2 = 3
m.walls.append(wall_3)

wall_4 = Wall()
wall_4.x = -DEFAULT_MAP_SIZE
wall_4.y = DEFAULT_MAP_SIZE
wall_4.xrepeat = 32
wall_4.yrepeat = 8
wall_4.point2 = 0
m.walls.append(wall_4)


m.cursectnum = 0


output = io.BytesIO()
BloodMapWriter()(m, output)
with open(r'C:\Program Files (x86)\GOG Galaxy\Games\Blood - Fresh Supply\out.map', 'wb') as f:
    f.write(output.getbuffer())
