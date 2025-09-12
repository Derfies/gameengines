from gameengines.build.map import Map, MapReaderBase, MapWriterBase


class MapReader(MapReaderBase):

    # TODO: Just set this in the base map reader class and be done with it?
    map_cls = Map


class MapWriter(MapWriterBase):

    # TODO: Just set this in the base map writer class and be done with it?
    map_cls = Map
