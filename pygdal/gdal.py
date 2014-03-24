

from weakref import ref

import numpy as np

from pygdal.util import ManagedObject, Extent, Window
from pygdal.libgdal import *


class Driver(ManagedObject):
    @property
    def short_name(self):
        return GDALGetDriverShortName(self.handle)

    @property
    def long_name(self):
        return GDALGetDriverLongName(self.handle)

    @property
    def help(self):
        return GDALGetDriverHelpTopic(self.handle)


    def open(self, identifier):
        # not supported?
        pass

    def create(self, identifier, size_x, size_y, num_bands=1, data_type=GDT_Byte, options=None):
        # TODO: creation options
        dataset_h = GDALCreate(
            self, identifier, size_x, size_y, num_bands, data_type, to_char_p_p(options)
        )
        return Dataset(dataset_h)

    def deregister(self):
        GDALDeregisterDriver(self)


    @classmethod
    def by_name(cls, name):
        return cls(GDALGetDriverByName(name))

    #@property
    #def creation_options(self):
    #    creation_options = GDALGetDriverCreationOptionList(self.handle)
    #    return creation_options.split(" ") # TODO: verify



class _BandsProxy(object):
    def __init__(self, dataset_ref):
        self._dataset_ref = dataset_ref
        self._band_cache = {}

    def __len__(self):
        return GDALGetRasterCount(self._dataset_ref())

    def __getitem__(self, index):
        try:
            return self._band_cache[index]
        except KeyError:
            band = Band(GDALGetRasterBand(self._dataset_ref(), index))
            self._band_cache[index] = band
            return band


class Dataset(ManagedObject):
    """ Pythonic wrapper for Dataset related GDAL stuff.
    """

    def __init__(self, *args, **kwargs):
        super(Dataset, self).__init__(*args, **kwargs)
        self._bandsproxy = _BandsProxy(ref(self))

    @property
    def metadata(self):
        #"SUBDATASETS"
        #"SUBDATASET_%d_NAME", nSubdataset
        pass

    @property
    def projection(self):
        return GDALGetProjectionRef(self)
    @projection.setter
    def projection(self, value):
        GDALSetProjection(self, value)
    

    @property
    def size(self):
        return (self.size_x, self.size_y)

    @property
    def size_x(self):
        return GDALGetRasterXSize(self)

    @property
    def size_y(self):
        return GDALGetRasterYSize(self)

    @property
    def bands(self):
        return self._bandsproxy

    def get_band(self, index):
        return self._bandsproxy[index]

    @property
    def geotransform(self):
        gt_arr = gdal_geotransform_type()
        GDALGetGeoTransform(self, gt_arr)
        return tuple(gt_arr)
    @geotransform.setter
    def geotransform(self, value):
        gt_arr = gdal_geotransform_type(*value)
        GDALSetGeoTransform(self, gt_arr)
    
    def transform_point(self, x, y):
        out_x = c_double()
        out_y = c_double()
        GDALApplyGeoTransform(self.geotransform, x, y, byref(out_x), byref(out_y))
        return out_x.value, out_y.value

    @property
    def extent(self):
        return Extent.from_geotransform_and_size(self.geotransform, self.size)

    def to_window(self, minx, miny, maxx, maxy):
        """ Transforms a geospatial extent to a image window.
        """

    def to_extent(self, offset_x, offset_y, size_x=None, size_y=None):
        """ Transforms the image window coordinates to a geospatial extent.
        """

    @property
    def gcps(self):
        gcps = GDALGetGCPs(self)
        if not gcps:
            return tuple()
        return tuple(gcps)
    @gcps.setter
    def gcps(self, value):
        self._gcps = value


    def read(self, offset_x=0, offset_y=0, size_x=None, size_y=None, mask=False):
        """ Read the data from the given window. The data is returned as a 
            numpy array.
        """
        pass

    def write(self, data, offset_x=0, offset_y=0, size_x=None, size_y=None):
        """ Write the data from the given array into the dataset. Expected is
            a numpy array.
        """
        pass

    def __getitem__(self, accessor):
        band_index = None
        try:
            slice_x, slice_y = accessor
            return self.read(*Window.from_slices((slice_x, slice_y)))
        except ValueError:
            pass

        try:
            slice_x, slice_y, band_index = accessor
            self.bands[band_index].read(*Window.from_slices((slice_x, slice_y)))
        except ValueError:
            pass

        raise ValueError

    def __setitem__(self, accessor, data):
        band_index = None
        try:
            slice_x, slice_y = accessor
            return self.write(data, *Window.from_slices((slice_x, slice_y)))
        except ValueError:
            pass

        try:
            slice_x, slice_y, band_index = accessor
            self.bands[band_index].write(data, *Window.from_slices((slice_x, slice_y)))
        except ValueError:
            pass

        raise ValueError

    def copy_to(self, other):
        pass

    def _close(self):
        if self._handle:
            GDALClose(self)
            self._handle = None

    def __del__(self):
        self._close()

    # contextmanager API

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self._close()

    # opening

    @classmethod
    def open(cls, name, mode=GA_ReadOnly, shared=True):
        if shared:
            handle = GDALOpenShared(name, mode)
        else:
            handle = GDALOpen(name, mode)
        return cls(handle)


open = Dataset.open


class Band(ManagedObject):
    """ Python wrapper for GDAl Raster Band related functions and data.
    """

    def __init__(self, handle, dataset_ref=None):
        super(Band, self).__init__(handle)
        self._dataset_ref = dataset_ref

    @property
    def dataset(self):
        if self._dataset_ref and self._dataset_ref():
            return self._dataset_ref()
        dataset_handle = GDALGetBandDataset(self)
        if dataset_handle: 
            return Dataset(dataset_handle)

    @property
    def index(self):
        return GDALGetBandNumber(self)

    @property
    def color_interpretation(self):
        return GDALGetRasterColorInterpretation(self)

    @property
    def color_interpretation_name(self):
        return GDALGetColorInterpretationName(self.color_interpretation)

    @property
    def data_type(self):
        return GDALGetRasterDataType(self)

    @property
    def data_type_name(self):
        return GDALGetDataTypeName(self.data_type)

    @property
    def dtype(self):
        """ Numpy dtype.
        """
        return GDT_TO_DTYPE.get(self.data_type, np.uint8)

    @property
    def size(self):
        return (self.size_x, self.size_y)

    @property
    def size_x(self):
        return GDALGetRasterBandXSize(self)

    @property
    def size_y(self):
        return GDALGetRasterBandYSize(self)

    
    @property
    def unit(self):
        return GDALGetRasterUnitType(self)
    @unit.setter
    def unit(self, value):
        GDALSetRasterUnitType(self, value)

    @property
    def offset(self):
        success = c_int()
        value = GDALGetRasterOffset(self, byref(success))
        if not success:
            return None
        return value
    @offset.setter
    def offset(self, value):
        GDALGetRasterOffset(self, value)

    @property
    def scale(self):
        success = c_int()
        value = GDALGetRasterScale(self, byref(success))
        if not success:
            return None
        return value
    @scale.setter
    def scale(self, value):
        GDALGetRasterScale(self, value)    

    # Raster access

    def _get_numpy_array(self, offset_x=0, offset_y=0, size_x=None, size_y=None):
        if not size_x:
            size_x = self.size_x - offset_x

        if not size_y:
            size_y = self.size_y - offset_y

        assert((size_x + offset_x) <= self.size_x)
        assert((size_y + offset_y) <= self.size_y)

        return np.empty((size_y, size_x), dtype=self.dtype)

    def read(self, offset_x=0, offset_y=0, size_x=None, size_y=None, mask=False, array=None):
        """ Read the data from the given window. The data is returned as a 
            numpy array.
        """
        array = array or self._get_numpy_array(offset_x, offset_y, size_x, size_y)

        size_x = size_x or self.size_x
        size_y = size_y or self.size_y

        assert(array.ndim == 2)

        GDALRasterIO(
            self, GF_Read, offset_x, offset_y, size_x, size_y,
            array.ctypes.data_as(c_void_p), size_x, size_y, self.data_type, 
            0, 0 # TODO: ??
        )

        return array

    def write(self, data, offset_x=0, offset_y=0, size_x=None, size_y=None):
        """ Write the data from the given array into the dataset. Expected is
            a numpy array.
        """
        buf_size_x, buf_size_y = data.shape
        GDALRasterIO(
            self, GF_Write, offset_x, offset_y, size_x, size_y,
            data.ctypes.data_as(c_void_p), buf_size_x, buf_size_y, self.data_type, 
            0, 0 # TODO: ??
        )

    def __getitem__(self, accessor):
        try:
            slice_x, slice_y = accessor
            return self.read(*Window.from_slices((slice_x, slice_y)))
        except ValueError:
            pass

    def __setitem__(self, accessor, data):
        try:
            slice_x, slice_y = accessor
            return self.write(data, *Window.from_slices((slice_x, slice_y)))
        except ValueError:
            pass


        raise ValueError


    def fill(self, value, ivalue=0.0):
        GDALFillRaster(self, value, ivalue)

    def copy_to(self, other):
        pass





GDT_TO_DTYPE = {
    #GDT_Unknown: np.uint8,
    GDT_Byte: np.uint8,
    GDT_UInt16: np.uint16,
    GDT_Int16: np.int16,
    GDT_UInt32: np.uint32,
    GDT_Int32: np.int32,
    GDT_Float32: np.float32,
    GDT_Float64: np.float64,
    #GDT_CInt16: np.c,
    #GDT_CInt32: np.,
    GDT_CFloat32: np.complex64,
    GDT_CFloat64: np.complex128
}

DTYPE_TO_GDT = dict(
    (value, key) for key, value in GDT_TO_DTYPE.items()
)


# setup stuff

use_exceptions()
GDALAllRegister()


def to_char_p_p(values):
    # converts a dict or a list of arguments to a ctypes compliant char** array
    if values is None:
        return None
    try:
        items = values.items()
    except AttributeError:
        items = values

    array = (c_char_p * len(items))()
    for i, (key, value) in enumerate(items):
        array[i] = "%s=%s" % (key, value)

    return array
