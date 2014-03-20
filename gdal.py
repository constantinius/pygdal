

from weakref import proxy

from pygdal.util import ManagedObject
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
            self, identifier, size_x, size_y, num_bands, data_type, None
        )
        return Dataset(dataset_h)

    @classmethod
    def by_name(cls, name):
        return cls(GDALGetDriverByName(name))

    #@property
    #def creation_options(self):
    #    creation_options = GDALGetDriverCreationOptionList(self.handle)
    #    return creation_options.split(" ") # TODO: verify






class _BandsProxy(object):
    def __init__(self, dataset):
        self._dataset = dataset

    def __len__(self):
        return GDALGetRasterCount(self._dataset)

    def __getitem__(self, index):
        # TODO
        return self._dataset.get_band(self._dataset, index)


class Dataset(ManagedObject):

    def __init__(self, *args, **kwargs):
        super(Dataset, self).__init__(*args, **kwargs)
        self._bandsproxy = _BandsProxy(proxy(self))

    @property
    def metadata(self):
        "SUBDATASETS"
        #"SUBDATASET_%d_NAME", nSubdataset

    @property
    def projection(self):
        pass

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
        return self._bandproxy


    def get_band(self, index):
        # TODO convert to band
        return GDALGetRasterBand(self._dataset, index)


    @property
    def geotransform(self):
        gt_arr = gdal_geotransform_type()
        GDALGetGeoTransform(self, gt_arr)
        return arr

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


    def __del__(self):
        GDALClose(self)


    def copy_to(self, other):
        pass

class Band(ManagedObject):
    @property
    def index(self):
        pass

    @property
    def color_interpretation(self):
        pass

    @property
    def color_interpretation_name(self):
        pass

    @property
    def data_type(self):
        pass

    @property
    def data_type_name(self):
        pass

    @property
    def dtype(self):
        """ Numpy dtype.
        """
        pass

    @property
    def size(self):
        return (self.size_x, self.size_y)

    @property
    def size_x(self):
        return GDALGetRasterBandXSize(self)

    @property
    def size_y(self):
        return GDALGetRasterBandYSize(self)


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

    def copy_to(self, other):
        pass

