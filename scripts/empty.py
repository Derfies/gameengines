import io

from gameengines.build.blood import Map, MapWriter as BloodMapWriter
from gameengines.build.duke3d import MapWriter as Duke3dMapWriter
from gameengines.build.map import Sector, Sprite, Wall, MapWriterBase, Map



writer_cls = Duke3dMapWriter
#writer_cls = BloodMapWriter
map_cls = Map


METER = 512
HEIGHT = 2 * METER
MAP_EXPORT_DIR_PATH = 'C:/Program Files (x86)/Steam/steamapps/common/Duke Nukem 3D/gameroot/maps/' #'
#MAP_EXPORT_DIR_PATH = 'C:/Program Files (x86)/GOG Galaxy/Games/Blood - Fresh Supply/'



for i in (1, 2, 4):

    map_size = i * METER

    m = map_cls()

    new_sector = Sector()
    new_sector.floorz = 0
    new_sector.ceilingz = -HEIGHT * 16
    new_sector.wallptr = 0
    new_sector.wallnum = 4
    m.sectors.append(new_sector)

    # Top left (top edge).
    wall_1 = Wall()
    wall_1.x = -map_size
    wall_1.y = -map_size
    wall_1.xrepeat = 32
    wall_1.yrepeat = 8
    wall_1.point2 = 1
    m.walls.append(wall_1)

    # Joining boundary, left side
    wall_2 = Wall()
    wall_2.x = map_size
    wall_2.y = -map_size
    wall_2.xrepeat = 32
    wall_2.yrepeat = 8
    wall_2.point2 = 2

    wall_2.nextwall = 7
    wall_2.nextsector = 1

    m.walls.append(wall_2)

    wall_3 = Wall()
    wall_3.x = map_size
    wall_3.y = map_size
    wall_3.xrepeat = 32
    wall_3.yrepeat = 8
    wall_3.point2 = 3
    m.walls.append(wall_3)

    wall_4 = Wall()
    wall_4.x = -map_size
    wall_4.y = map_size
    wall_4.xrepeat = 32
    wall_4.yrepeat = 8
    wall_4.point2 = 0
    m.walls.append(wall_4)

    ####### One to the right

    new_sector = Sector()
    new_sector.floorz = 0
    new_sector.ceilingz = -HEIGHT * 16
    new_sector.wallptr = 4
    new_sector.wallnum = 4
    m.sectors.append(new_sector)

    wall_1 = Wall()
    wall_1.x = -map_size + map_size * 2
    wall_1.y = -map_size
    wall_1.xrepeat = 32
    wall_1.yrepeat = 8
    wall_1.point2 = 5
    m.walls.append(wall_1)

    wall_2 = Wall()
    wall_2.x = map_size + map_size * 2
    wall_2.y = -map_size
    wall_2.xrepeat = 32
    wall_2.yrepeat = 8
    wall_2.point2 = 6
    m.walls.append(wall_2)

    wall_3 = Wall()
    wall_3.x = map_size + map_size * 2
    wall_3.y = map_size
    wall_3.xrepeat = 32
    wall_3.yrepeat = 8
    wall_3.point2 = 7
    m.walls.append(wall_3)

    wall_4 = Wall()
    wall_4.x = -map_size + map_size * 2
    wall_4.y = map_size
    wall_4.xrepeat = 32
    wall_4.yrepeat = 8
    wall_4.point2 = 4

    wall_4.nextwall = 1
    wall_4.nextsector = 0

    m.walls.append(wall_4)


    m.cursectnum = 0


    output = io.BytesIO()
    writer_cls()(m, output)
    with open(rf'{MAP_EXPORT_DIR_PATH}{i}.map', 'wb') as f:
        print(MAP_EXPORT_DIR_PATH)
        f.write(output.getbuffer())
