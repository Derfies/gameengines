# TODO: Convert these to scripts.
'''
def test_duke3d_to_blood(self):
    #file_path = Path(__file__).parent.joinpath(r'data\duke3d.map')
    file_path = r'C:\Program Files (x86)\Steam\steamapps\common\Duke Nukem 3D\gameroot\maps\DX-EYEOFRA.MAP'
    with open(file_path, 'rb') as file:
        input = io.BytesIO(file.read())
        dm = Duke3dMapReader()(input)

   #  # Convert.
   #  bm = BloodMap()
   #  print('header before:', bm.header)
   # # print('data:', asdict(dm.header))
   #  bm.header = BloodMap.header_cls(**asdict(dm.header))
   #  print('header after:', bm.header)

    m = BloodMap.from_map(dm)

    output = io.BytesIO()
    BloodMapWriter()(m, output)

    # print(m.header)
    # for s in m.sectors:
    #     print(s)
    # for w in m.walls:
    #     print(w)
    # #for s in m.sprites:
    # #    print(s)
    # m.sprites = []


    with open(r'C:\Program Files (x86)\GOG Galaxy\Games\Blood - Fresh Supply\addons\out.map', 'wb') as f:
        f.write(output.getbuffer())

def test_blood_to_duke3d(self):
    file_path = Path(__file__).parent.joinpath(r'data\blood.map')
    with open(file_path, 'rb') as file:
        input = io.BytesIO(file.read())
        dm = BloodMapReader()(input)

    m = Duke3dMap.from_map(dm)

    # HAX
    m.header.cursectnum = 0
    print(m.header)
    for wall in m.walls:
        print(wall)
    for sector in m.sectors:
        print(sector)
    output = io.BytesIO()
    Duke3dMapWriter()(m, output)

    print(m.header)
    for s in m.sectors:
        print(s)
    for w in m.walls:
        print(w)
    for s in m.sprites:
       print(s)
    #m.sprites = []

    with open(r'C:\Program Files (x86)\Steam\steamapps\common\Duke Nukem 3D\gameroot\maps\out.map', 'wb') as f:
        f.write(output.getbuffer())
'''