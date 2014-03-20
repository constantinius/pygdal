

class ManagedObject(object):
    def __init__(self, handle):
        self._handle = handle

    @property
    def _as_parameter_(self):
        return self._handle



class Window(tuple):
    def __new__(cls, offset_x=None, offset_y=None, size_x=None, size_y=None):
        obj = super(cls).__new__(offset_x, offset_y, size_x, size_y)
        for v in obj:
            if not v is None and v < 0:
                raise ValueError
        return obj

    offset_x = property(lambda self: self[0])
    offset_y = property(lambda self: self[1])
    size_x = property(lambda self: self[2])
    size_y = property(lambda self: self[3])

    @classmethod
    def from_slices(cls, slices):
        if len(slices) != 2:
            raise ValueError

        slice_x, slice_y = slices

        offset_x, offset_y, size_x, size_y = (None, None, None, None)

        if slice_x == Ellipsis:
            pass
        elif isinstance(slice_x, slice):
            offset_x = slice_x.start
            size_x = slice_x.stop - slice_x.start
        else:
            raise ValueError

        if slice_y == Ellipsis:
            pass
        elif isinstance(slice_y, slice):
            offset_y = slice_y.start
            size_y = slice_y.stop - slice_y.start
        else:
            raise ValueError

        return cls(offset_x, offset_y, size_x, size_y)


class Extent(tuple):
    def __new__(cls, min_x, min_y, max_x, max_y):
        assert(min_x <= max_x)
        assert(min_y <= max_y)
        return super(cls).__new__(min_x, min_y, max_x, max_y)

    min_x = property(lambda self: self[0])
    min_y = property(lambda self: self[1])
    max_x = property(lambda self: self[2])
    max_y = property(lambda self: self[3])

    @classmethod
    def from_geotransform_and_size(cls, gt, size):
        x1 = gt[0]
        x2 = gt[0] + gt[1] * size[0]
        y1 = gt[3]
        y2 = gt[3] + gt[5] * size[1]
        return cls(
            min(x1, x2), min(y1, y2),
            max(x1, x2), max(y1, y2),
        )