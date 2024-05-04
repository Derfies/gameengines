from gameengines.build.map import MapBase, MapReaderBase, MapWriterBase


class MapReader(MapReaderBase):

    # TODO: Just set this in the base map reader class and be done with it?
    map_cls = MapBase


class MapWriter(MapWriterBase):

    # TODO: Just set this in the base map writer class and be done with it?
    map_cls = MapBase
