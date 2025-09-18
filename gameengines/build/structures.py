import ctypes


class Metacls(type(ctypes.LittleEndianStructure)):

    def __new__(metacls, name, bases, namespace):
        cls = super().__new__(metacls, name, bases, namespace)

        # Add a nice string representation for print().
        def __str__(self):
            fields = getattr(cls, '_fields_')
            values = ', '.join(f'{f_name}={getattr(self, f_name)!r}' for f_name, _ in fields)
            return f'{name}({values})'
        cls.__str__ = __str__

        return cls


class StructureBase(ctypes.LittleEndianStructure, metaclass=Metacls):

    _pack_ = 1

    @classmethod
    def from_stream(cls, stream):
        buf = stream.read(ctypes.sizeof(cls))
        if len(buf) < ctypes.sizeof(cls):
            raise EOFError('Not enough bytes to fill structure')
        return cls.from_buffer_copy(buf)


class ArtHeader(StructureBase):

    _fields_ = (
        ('artversion',      ctypes.c_int32),
        ('numtiles',        ctypes.c_int32),
        ('localtilestart',  ctypes.c_int32),
        ('localtileend',    ctypes.c_int32),
    )
