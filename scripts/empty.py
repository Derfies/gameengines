import io

from gameengines.build.blood import Map, MapWriter as BloodMapWriter
from gameengines.build.duke3d import MapWriter as Duke3dMapWriter
from gameengines.build.map import Sector, Sprite, Wall, MapWriterBase, MapBase


map_cls = MapBase


DEFAULT_MAP_SIZE = 2048


m = map_cls()

new_sector = Sector()
new_sector.floor_z = DEFAULT_MAP_SIZE * 16
new_sector.ceiling_z = -DEFAULT_MAP_SIZE * 16
new_sector.wallptr = 0
new_sector.wallnum = 4
# new_sector.tags[2] = -1
m.sectors.append(new_sector)

wall_1 = Wall()
wall_1.x = -DEFAULT_MAP_SIZE
wall_1.y = -DEFAULT_MAP_SIZE
wall_1.xrepeat = 32
wall_1.yrepeat = 8
wall_1.point2 = 1
wall_1.nextsector = -1
wall_1.nextwall = -1
m.walls.append(wall_1)

wall_2 = Wall()
wall_2.x = DEFAULT_MAP_SIZE
wall_2.y = -DEFAULT_MAP_SIZE
wall_2.xrepeat = 32
wall_2.yrepeat = 8
wall_2.point2 = 2
wall_2.nextsector = -1
wall_2.nextwall = -1
m.walls.append(wall_2)

wall_3 = Wall()
wall_3.x = DEFAULT_MAP_SIZE
wall_3.y = DEFAULT_MAP_SIZE
wall_3.xrepeat = 32
wall_3.yrepeat = 8
wall_3.point2 = 3
wall_3.nextsector = -1
wall_3.nextwall = -1
m.walls.append(wall_3)

wall_4 = Wall()
wall_4.x = -DEFAULT_MAP_SIZE
wall_4.y = DEFAULT_MAP_SIZE
wall_4.xrepeat = 32
wall_4.yrepeat = 8
wall_4.point2 = 0
wall_4.nextsector = -1
wall_4.nextwall = -1
m.walls.append(wall_4)

start_sprite = Sprite()
start_sprite.z = DEFAULT_MAP_SIZE * 16
# start_sprite.tags[0] = 1
# start_sprite.stat.centring = 1
start_sprite.picnum = 2522
start_sprite.sectnum = 0
m.sprites.append(start_sprite)

m.header.cursectnum = 0


output = io.BytesIO()
# BloodMapWriter()(m, output)
# with open(r'C:\Program Files (x86)\GOG Galaxy\Games\Blood - Fresh Supply\addons\test.map', 'wb') as f:
#     f.write(output.getbuffer())
Duke3dMapWriter()(m, output)
with open(r'C:\Program Files (x86)\Steam\steamapps\common\Duke Nukem 3D\gameroot\maps\test.map', 'wb') as f:
    f.write(output.getbuffer())
