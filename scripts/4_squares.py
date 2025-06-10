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
    wall_0 = Wall()
    wall_0.x = -map_size
    wall_0.y = -map_size
    wall_0.xrepeat = 32
    wall_0.yrepeat = 8
    wall_0.point2 = 1
    m.walls.append(wall_0)

    # Joining boundary, left side
    wall_1 = Wall()
    wall_1.x = map_size
    wall_1.y = -map_size
    wall_1.xrepeat = 32
    wall_1.yrepeat = 8
    wall_1.point2 = 2

    wall_1.nextwall = 7
    wall_1.nextsector = 1

    m.walls.append(wall_1)

    wall_2 = Wall()
    wall_2.x = map_size
    wall_2.y = map_size
    wall_2.xrepeat = 32
    wall_2.yrepeat = 8
    wall_2.point2 = 3

    wall_2.nextwall = 8
    wall_2.nextsector = 2

    m.walls.append(wall_2)

    wall_3 = Wall()
    wall_3.x = -map_size
    wall_3.y = map_size
    wall_3.xrepeat = 32
    wall_3.yrepeat = 8
    wall_3.point2 = 0
    m.walls.append(wall_3)

    ####### One to the right

    new_sector = Sector()
    new_sector.floorz = 0
    new_sector.ceilingz = -HEIGHT * 16
    new_sector.wallptr = 4
    new_sector.wallnum = 4
    m.sectors.append(new_sector)

    wall_4 = Wall()
    wall_4.x = -map_size + map_size * 2
    wall_4.y = -map_size
    wall_4.xrepeat = 32
    wall_4.yrepeat = 8
    wall_4.point2 = 5
    m.walls.append(wall_4)

    wall_5 = Wall()
    wall_5.x = map_size + map_size * 2
    wall_5.y = -map_size
    wall_5.xrepeat = 32
    wall_5.yrepeat = 8
    wall_5.point2 = 6
    m.walls.append(wall_5)

    wall_6 = Wall()
    wall_6.x = map_size + map_size * 2
    wall_6.y = map_size
    wall_6.xrepeat = 32
    wall_6.yrepeat = 8
    wall_6.point2 = 7
    m.walls.append(wall_6)

    wall_7 = Wall()
    wall_7.x = -map_size + map_size * 2
    wall_7.y = map_size
    wall_7.xrepeat = 32
    wall_7.yrepeat = 8
    wall_7.point2 = 4

    wall_7.nextwall = 1
    wall_7.nextsector = 0

    m.walls.append(wall_7)

    ####### One below

    new_sector = Sector()
    new_sector.floorz = 0
    new_sector.ceilingz = -HEIGHT * 16
    new_sector.wallptr = 8
    new_sector.wallnum = 4
    m.sectors.append(new_sector)

    wall_8 = Wall()
    wall_8.x = -map_size
    wall_8.y = -map_size + map_size * 2
    wall_8.xrepeat = 32
    wall_8.yrepeat = 8
    wall_8.point2 = 9

    wall_8.nextwall = 2
    wall_8.nextsector = 0

    m.walls.append(wall_8)

    wall_9 = Wall()
    wall_9.x = map_size
    wall_9.y = -map_size + map_size * 2
    wall_9.xrepeat = 32
    wall_9.yrepeat = 8
    wall_9.point2 = 10
    m.walls.append(wall_9)

    wall_10 = Wall()
    wall_10.x = map_size
    wall_10.y = map_size + map_size * 2
    wall_10.xrepeat = 32
    wall_10.yrepeat = 8
    wall_10.point2 = 11
    m.walls.append(wall_10)

    wall_11 = Wall()
    wall_11.x = -map_size
    wall_11.y = map_size + map_size * 2
    wall_11.xrepeat = 32
    wall_11.yrepeat = 8
    wall_11.point2 = 8


    m.walls.append(wall_11)

    ####### One below right

    new_sector = Sector()
    new_sector.floorz = 0
    new_sector.ceilingz = -HEIGHT * 16
    new_sector.wallptr = 12
    new_sector.wallnum = 4
    m.sectors.append(new_sector)

    wall_12 = Wall()
    wall_12.x = map_size
    wall_12.y = -map_size + map_size * 2
    wall_12.xrepeat = 32
    wall_12.yrepeat = 8
    wall_12.point2 = 13

    wall_12.nextwall = 6
    wall_12.nextsector = 1

    m.walls.append(wall_12)

    wall_13 = Wall()
    wall_13.x = map_size * 3
    wall_13.y = -map_size + map_size * 2
    wall_13.xrepeat = 32
    wall_13.yrepeat = 8
    wall_13.point2 = 14
    m.walls.append(wall_13)

    wall_14 = Wall()
    wall_14.x = map_size * 3
    wall_14.y = map_size + map_size * 2
    wall_14.xrepeat = 32
    wall_14.yrepeat = 8
    wall_14.point2 = 15
    m.walls.append(wall_14)

    wall_15 = Wall()
    wall_15.x = map_size
    wall_15.y = map_size + map_size * 2
    wall_15.xrepeat = 32
    wall_15.yrepeat = 8
    wall_15.point2 = 12

    m.walls.append(wall_15)


    m.cursectnum = 0


    output = io.BytesIO()
    writer_cls()(m, output)
    with open(rf'{MAP_EXPORT_DIR_PATH}_4_{i}.map', 'wb') as f:
        print(MAP_EXPORT_DIR_PATH)
        f.write(output.getbuffer())
