from ctypes import *
from functools import wraps

_libgdal = CDLL("libgdal.so")

_USE_EXCEPTIONS = False

def use_exceptions(value=True):
    global _USE_EXCEPTIONS
    _USE_EXCEPTIONS = value
    if _USE_EXCEPTIONS:
        CPLSetErrorHandler(CPLQuietErrorHandler)
    else:
        CPLSetErrorHandler(CPLDefaultErrorHandler)


CPLE_None = 0
CPLE_AppDefined = 1
CPLE_OutOfMemory = 2
CPLE_FileIO = 3
CPLE_OpenFailed = 4
CPLE_IllegalArg = 5
CPLE_NotSupported = 6
CPLE_AssertionFailed = 7
CPLE_NoWriteAccess = 8
CPLE_UserInterrupt = 9
CPLE_ObjectNull = 10


CPLE_TO_EXCEPTION = {
    CPLE_AppDefined: Exception,
    CPLE_OutOfMemory: MemoryError,
    CPLE_FileIO: IOError,
    CPLE_OpenFailed: IOError,
    CPLE_IllegalArg: ValueError,
    CPLE_NotSupported: NotImplementedError,
    CPLE_AssertionFailed: AssertionError,
    CPLE_NoWriteAccess: IOError,
    CPLE_UserInterrupt: KeyboardInterrupt,
    CPLE_ObjectNull: ValueError,
}

# utility funcs

def cplerr_errcheck(result, func, arguments):
    if _USE_EXCEPTIONS and result != CPLE_None:
        e_type = CPLE_TO_EXCEPTION.get(result, Exception)
        raise e_type(CPLGetLastErrorMsg())
    return result

def null_errcheck(result, func, arguments):
    if _USE_EXCEPTIONS and result == None:
        e_type = CPLE_TO_EXCEPTION.get(CPLGetLastErrorType(), Exception)
        raise e_type(CPLGetLastErrorMsg())
    return result

# type declarations

c_char_p_p = POINTER(c_char_p)

gdal_major_object_h = c_void_p
gdal_driver_h = c_void_p
gdal_dataset_h = c_void_p
gdal_rasterband_h = c_void_p
gdal_color_table_h = c_void_p

gdal_geotransform_type = c_double * 6

GDAL_PROGRESS_FUNC = CFUNCTYPE(c_int, c_double, c_char_p, c_void_p)

class GDAL_GCP(Structure):
    _fields_ = [
        ("id", c_char_p),
        ("info", c_char_p),
        ("pixel", c_double),
        ("line", c_double),
        ("x", c_double),
        ("y", c_double),
        ("z", c_double)
    ]

# CPL function wrappers

CPLGetLastErrorType = _libgdal.CPLGetLastErrorType
CPLGetLastErrorType.restype = c_int

CPLGetLastErrorMsg = _libgdal.CPLGetLastErrorMsg
CPLGetLastErrorMsg.restype = c_char_p

CPLQuietErrorHandler = _libgdal.CPLQuietErrorHandler
CPLDefaultErrorHandler = _libgdal.CPLDefaultErrorHandler

CPL_ERROR_HANDLER_TYPE = CFUNCTYPE(None, c_int, c_int, c_char_p)

CPLSetErrorHandler = _libgdal.CPLSetErrorHandler
#CPLSetErrorHandler.argtypes = [CPL_ERROR_HANDLER_TYPE]



# GDAL defines

GDT_Unknown = 0
GDT_Byte = 1
GDT_UInt16 = 2
GDT_Int16 = 3
GDT_UInt32 = 4
GDT_Int32 = 5
GDT_Float32 = 6
GDT_Float64 = 7
GDT_CInt16 = 8
GDT_CInt32 = 9
GDT_CFloat32 = 10
GDT_CFloat64 = 11

GA_ReadOnly = 0
GA_Update = 1

GF_Read = 0
GF_Write = 1

GCI_Undefined = 0
GCI_GrayIndex = 1
GCI_PaletteIndex = 2
GCI_RedBand = 3
GCI_GreenBand = 4
GCI_BlueBand = 5
GCI_AlphaBand = 6
GCI_HueBand = 7
GCI_SaturationBand = 8
GCI_LightnessBand = 9
GCI_CyanBand = 10
GCI_MagentaBand = 11
GCI_YellowBand = 12
GCI_BlackBand = 13
GCI_YCbCr_YBand = 14
GCI_YCbCr_CbBand = 15
GCI_YCbCr_CrBand = 16

# function wrappers

GDALGetDataTypeSize = _libgdal.GDALGetDataTypeSize
GDALGetDataTypeSize.restype = c_int
GDALGetDataTypeSize.argtypes = [c_int]

GDALDataTypeIsComplex = _libgdal.GDALDataTypeIsComplex
GDALDataTypeIsComplex.restype = c_int
GDALDataTypeIsComplex.argtypes = [c_int]

GDALGetDataTypeName = _libgdal.GDALGetDataTypeName
GDALGetDataTypeName.restype = c_char_p
GDALGetDataTypeName.argtypes = [c_int]

GDALGetDataTypeByName = _libgdal.GDALGetDataTypeByName
GDALGetDataTypeByName.restype = c_int
GDALGetDataTypeByName.argtypes = [c_char_p]

GDALDataTypeUnion = _libgdal.GDALDataTypeUnion
GDALDataTypeUnion.restype = c_int
GDALDataTypeUnion.argtypes = [c_int, c_int]

GDALGetAsyncStatusTypeName = _libgdal.GDALGetAsyncStatusTypeName
GDALGetAsyncStatusTypeName.restype = c_char_p
GDALGetAsyncStatusTypeName.argtypes = [c_int]

GDALGetAsyncStatusTypeByName = _libgdal.GDALGetAsyncStatusTypeByName
GDALGetAsyncStatusTypeByName.restype = c_int
GDALGetAsyncStatusTypeByName.argtypes = [c_char_p]

GDALGetColorInterpretationName = _libgdal.GDALGetColorInterpretationName
GDALGetColorInterpretationName.restype = c_char_p
GDALGetColorInterpretationName.argtypes = [c_int]

GDALGetColorInterpretationByName = _libgdal.GDALGetColorInterpretationByName
GDALGetColorInterpretationByName.restype = c_int
GDALGetColorInterpretationByName.argtypes = [c_char_p]

GDALGetPaletteInterpretationName = _libgdal.GDALGetPaletteInterpretationName
GDALGetPaletteInterpretationName.restype = c_char_p
GDALGetPaletteInterpretationName.argtypes = [c_int]

GDALAllRegister = _libgdal.GDALAllRegister

GDALCreate = _libgdal.GDALCreate
GDALCreate.restype = gdal_dataset_h
GDALCreate.argtypes = [gdal_driver_h, c_char_p, c_int, c_int, c_int, c_int, c_char_p_p]
GDALCreate.errcheck = null_errcheck

GDALCreateCopy = _libgdal.GDALCreateCopy
GDALCreateCopy.restype = gdal_dataset_h
GDALCreateCopy.argtypes = [gdal_driver_h, c_char_p, gdal_dataset_h, c_int, c_char_p_p, GDAL_PROGRESS_FUNC, c_void_p]
GDALCreateCopy.errcheck = null_errcheck

GDALIdentifyDriver = _libgdal.GDALIdentifyDriver
GDALIdentifyDriver.restype = gdal_driver_h
GDALIdentifyDriver.argtypes = [c_char_p, c_char_p_p]
GDALIdentifyDriver.errcheck = null_errcheck

GDALOpen = _libgdal.GDALOpen
GDALOpen.restype = gdal_dataset_h
GDALOpen.argtypes = [c_char_p, c_int]
GDALOpen.errcheck = null_errcheck

GDALOpenShared = _libgdal.GDALOpenShared
GDALOpenShared.restype = gdal_dataset_h
GDALOpenShared.argtypes = [c_char_p, c_int]
GDALOpenShared.errcheck = null_errcheck

#int     GDALDumpOpenDatasets (FILE *)
#    List open datasets.

GDALGetDriverByName = _libgdal.GDALGetDriverByName
GDALGetDriverByName.restype = gdal_driver_h
GDALGetDriverByName.argtypes = [c_char_p]
GDALGetDriverByName.errcheck = null_errcheck

GDALGetDriverCount = _libgdal.GDALGetDriverCount
GDALGetDriverCount.restype = c_int

GDALGetDriver = _libgdal.GDALGetDriver
GDALGetDriver.restype = gdal_driver_h
GDALGetDriver.argtypes = [c_int]
GDALGetDriver.errcheck = null_errcheck

GDALDestroyDriver = _libgdal.GDALDestroyDriver
GDALDestroyDriver.argtypes = [gdal_driver_h]

GDALRegisterDriver = _libgdal.GDALRegisterDriver
GDALRegisterDriver.restype = c_int
GDALRegisterDriver.argtypes = [gdal_driver_h]
GDALRegisterDriver.errcheck = cplerr_errcheck

GDALDeregisterDriver = _libgdal.GDALDeregisterDriver
GDALDeregisterDriver.argtypes = [gdal_driver_h]

GDALDestroyDriverManager = _libgdal.GDALDestroyDriverManager

GDALDeleteDataset = _libgdal.GDALDeleteDataset
GDALDeleteDataset.restype = c_int
GDALDeleteDataset.argtypes = [gdal_driver_h, c_char_p]
GDALDeleteDataset.errcheck = cplerr_errcheck

GDALRenameDataset = _libgdal.GDALRenameDataset
GDALRenameDataset.restype = c_int
GDALRenameDataset.argtypes = [gdal_driver_h, c_char_p, c_char_p]
GDALRenameDataset.errcheck = cplerr_errcheck

GDALCopyDatasetFiles = _libgdal.GDALCopyDatasetFiles
GDALCopyDatasetFiles.restype = c_int
GDALCopyDatasetFiles.argtypes = [gdal_driver_h, c_char_p, c_char_p]
GDALCopyDatasetFiles.errcheck = cplerr_errcheck

GDALValidateCreationOptions = _libgdal.GDALValidateCreationOptions
GDALValidateCreationOptions.restype = c_int
GDALValidateCreationOptions.argtypes = [gdal_driver_h, c_char_p_p]

GDALGetDriverShortName = _libgdal.GDALGetDriverShortName
GDALGetDriverShortName.restype = c_char_p
GDALGetDriverShortName.argtypes = [gdal_driver_h]

GDALGetDriverLongName = _libgdal.GDALGetDriverLongName
GDALGetDriverLongName.restype = c_char_p
GDALGetDriverLongName.argtypes = [gdal_driver_h]

GDALGetDriverHelpTopic = _libgdal.GDALGetDriverHelpTopic
GDALGetDriverHelpTopic.restype = c_char_p
GDALGetDriverHelpTopic.argtypes = [gdal_driver_h]

GDALGetDriverCreationOptionList = _libgdal.GDALGetDriverCreationOptionList
GDALGetDriverCreationOptionList.restype = c_char_p
GDALGetDriverCreationOptionList.argtypes = [gdal_driver_h]

#void    GDALInitGCPs (int, GDAL_GCP *)
#void    GDALDeinitGCPs (int, GDAL_GCP *)
#GDAL_GCP *  GDALDuplicateGCPs (int, const GDAL_GCP *)
#int     GDALGCPsToGeoTransform (int nGCPCount, const GDAL_GCP *pasGCPs, double *padfGeoTransform, int bApproxOK) CPL_WARN_UNUSED_RESULT
#    Generate Geotransform from GCPs. 
#int     GDALInvGeoTransform (double *padfGeoTransformIn, double *padfInvGeoTransformOut) CPL_WARN_UNUSED_RESULT
#    Invert Geotransform. 


GDALApplyGeoTransform = _libgdal.GDALApplyGeoTransform
GDALApplyGeoTransform.argtypes = [gdal_geotransform_type, c_double, c_double, POINTER(c_double), POINTER(c_double)]


"""
void    GDALComposeGeoTransforms (const double *padfGeoTransform1, const double *padfGeoTransform2, double *padfGeoTransformOut)
    Compose two geotransforms. 
"""


"""
char **     GDALGetMetadataDomainList (GDALMajorObjectH hObject)
    Fetch list of metadata domains. 
char **     GDALGetMetadata (GDALMajorObjectH, const char *)
    Fetch metadata. 
CPLErr  GDALSetMetadata (GDALMajorObjectH, char **, const char *)
    Set metadata. 
const char *    GDALGetMetadataItem (GDALMajorObjectH, const char *, const char *)
    Fetch single metadata item. 
CPLErr  GDALSetMetadataItem (GDALMajorObjectH, const char *, const char *, const char *)
    Set single metadata item. 
"""

GDALGetDescription = _libgdal.GDALGetDescription
GDALGetDescription.restype = c_char_p
GDALGetDescription.argtypes = [gdal_major_object_h]

GDALSetDescription = _libgdal.GDALSetDescription
GDALSetDescription.argtypes = [gdal_major_object_h, c_char_p]

GDALGetDatasetDriver = _libgdal.GDALGetDatasetDriver
GDALGetDatasetDriver.restype = gdal_driver_h
GDALGetDatasetDriver.argtypes = [gdal_dataset_h]

"""
char **     GDALGetFileList (GDALDatasetH)
    Fetch files forming dataset. 
"""

GDALClose = _libgdal.GDALClose
GDALClose.argtypes = [gdal_dataset_h]

GDALGetRasterXSize = _libgdal.GDALGetRasterXSize
GDALGetRasterXSize.restype = c_int
GDALGetRasterXSize.argtypes = [gdal_dataset_h]

GDALGetRasterYSize = _libgdal.GDALGetRasterYSize
GDALGetRasterYSize.restype = c_int
GDALGetRasterYSize.argtypes = [gdal_dataset_h]

GDALGetRasterCount = _libgdal.GDALGetRasterCount
GDALGetRasterCount.restype = c_int
GDALGetRasterCount.argtypes = [gdal_dataset_h]

GDALGetRasterBand = _libgdal.GDALGetRasterBand
GDALGetRasterBand.restype = gdal_rasterband_h
GDALGetRasterBand.argtypes = [gdal_dataset_h, c_int]
GDALGetRasterBand.errcheck = null_errcheck

GDALAddBand = _libgdal.GDALAddBand
GDALAddBand.restype = c_int
GDALAddBand.argtypes = [gdal_dataset_h, c_int, c_char_p_p]
GDALAddBand.errcheck = cplerr_errcheck

"""
GDALAsyncReaderH    GDALBeginAsyncReader (GDALDatasetH hDS, int nXOff, int nYOff, int nXSize, int nYSize, void *pBuf, int nBufXSize, int nBufYSize, GDALDataType eBufType, int nBandCount, int *panBandMap, int nPixelSpace, int nLineSpace, int nBandSpace, char **papszOptions)
void    GDALEndAsyncReader (GDALDatasetH hDS, GDALAsyncReaderH hAsynchReaderH)
CPLErr  GDALDatasetRasterIO (GDALDatasetH hDS, GDALRWFlag eRWFlag, int nDSXOff, int nDSYOff, int nDSXSize, int nDSYSize, void *pBuffer, int nBXSize, int nBYSize, GDALDataType eBDataType, int nBandCount, int *panBandCount, int nPixelSpace, int nLineSpace, int nBandSpace)
    Read/write a region of image data from multiple bands. 
"""

GDALDatasetAdviseRead = _libgdal.GDALDatasetAdviseRead
GDALDatasetAdviseRead.restype = c_int
GDALDatasetAdviseRead.argtypes = [gdal_dataset_h, c_int, c_int, c_int, c_int, c_int, c_int, POINTER(c_int), c_char_p_p]
GDALDatasetAdviseRead.errcheck = cplerr_errcheck

GDALGetProjectionRef = _libgdal.GDALGetProjectionRef
GDALGetProjectionRef.restype = c_char_p
GDALGetProjectionRef.argtypes = [gdal_dataset_h]

GDALSetProjection = _libgdal.GDALSetProjection
GDALSetProjection.restype = c_int
GDALSetProjection.argtypes = [gdal_dataset_h, c_char_p]
GDALSetProjection.errcheck = cplerr_errcheck

GDALGetGeoTransform = _libgdal.GDALGetGeoTransform
GDALGetGeoTransform.restype = c_int
GDALGetGeoTransform.argtypes = [gdal_dataset_h, gdal_geotransform_type]
#GDALGetGeoTransform.errcheck = cplerr_errcheck # TODO not working here...

GDALSetGeoTransform = _libgdal.GDALSetGeoTransform
GDALSetGeoTransform.restype = c_int
GDALSetGeoTransform.argtypes = [gdal_dataset_h, gdal_geotransform_type]
GDALSetGeoTransform.errcheck = cplerr_errcheck

GDALGetGCPCount = _libgdal.GDALGetGCPCount
GDALGetGCPCount.restype = c_int
GDALGetGCPCount.argtypes = [gdal_dataset_h]

GDALGetGCPProjection = _libgdal.GDALGetGCPProjection
GDALGetGCPProjection.restype = c_char_p
GDALGetGCPProjection.argtypes = [gdal_dataset_h]

GDALGetGCPs = _libgdal.GDALGetGCPs
GDALGetGCPs.restype = POINTER(GDAL_GCP)
GDALGetGCPs.argtypes = [gdal_dataset_h]

GDALSetGCPs = _libgdal.GDALSetGCPs
GDALSetGCPs.restype = c_int
GDALSetGCPs.argtypes = [gdal_dataset_h, c_int, POINTER(GDAL_GCP), c_char_p]
GDALSetGCPs.errcheck = cplerr_errcheck



"""
void *  GDALGetInternalHandle (GDALDatasetH, const char *)
    Fetch a format specific internally meaningful handle.
int     GDALReferenceDataset (GDALDatasetH)
    Add one to dataset reference count. 
int     GDALDereferenceDataset (GDALDatasetH)
    Subtract one from dataset reference count. 

"""




""" 
CPLErr  GDALBuildOverviews (GDALDatasetH, const char *, int, int *, int, int *, GDALProgressFunc, void *)
    Build raster overview(s). 
void    GDALGetOpenDatasets (GDALDatasetH **hDS, int *pnCount)
    Fetch all open GDAL dataset handles. 
int     GDALGetAccess (GDALDatasetH hDS)
    Return access flag. 
void    GDALFlushCache (GDALDatasetH hDS)
    Flush all write cached data to disk. 
CPLErr  GDALCreateDatasetMaskBand (GDALDatasetH hDS, int nFlags)
    Adds a mask band to the dataset.
"""

GDALDatasetCopyWholeRaster = _libgdal.GDALDatasetCopyWholeRaster
GDALDatasetCopyWholeRaster.restype = c_int
GDALDatasetCopyWholeRaster.argtypes = [gdal_dataset_h, gdal_dataset_h, c_char_p_p, GDAL_PROGRESS_FUNC, c_void_p]
GDALDatasetCopyWholeRaster.errcheck = cplerr_errcheck


"""
CPLErr  GDALDatasetCopyWholeRaster (GDALDatasetH hSrcDS, GDALDatasetH hDstDS, char **papszOptions, GDALProgressFunc pfnProgress, void *pProgressData)
    Copy all dataset raster data. 
CPLErr  GDALRasterBandCopyWholeRaster (GDALRasterBandH hSrcBand, GDALRasterBandH hDstBand, char **papszOptions, GDALProgressFunc pfnProgress, void *pProgressData)
    Copy all raster band raster data. 
CPLErr  GDALRegenerateOverviews (GDALRasterBandH hSrcBand, int nOverviewCount, GDALRasterBandH *pahOverviewBands, const char *pszResampling, GDALProgressFunc pfnProgress, void *pProgressData)
    Generate downsampled overviews. 
"""

GDALGetRasterDataType = _libgdal.GDALGetRasterDataType
GDALGetRasterDataType.restype = c_int
GDALGetRasterDataType.argtypes = [gdal_rasterband_h]

GDALGetBlockSize = _libgdal.GDALGetBlockSize
GDALGetBlockSize.argtypes = [gdal_rasterband_h, POINTER(c_int), POINTER(c_int)]


""" 
CPLErr  GDALRasterAdviseRead (GDALRasterBandH hRB, int nDSXOff, int nDSYOff, int nDSXSize, int nDSYSize, int nBXSize, int nBYSize, GDALDataType eBDataType, char **papszOptions)
    Advise driver of upcoming read requests. 
"""

GDALRasterIO = _libgdal.GDALRasterIO
GDALRasterIO.restype = c_int
GDALRasterIO.argtypes = [gdal_rasterband_h, c_int, c_int, c_int, c_int, c_int, c_void_p, c_int, c_int, c_int, c_int, c_int]
GDALRasterIO.errcheck = cplerr_errcheck

GDALReadBlock = _libgdal.GDALReadBlock
GDALReadBlock.restype = c_int
GDALReadBlock.argtypes = [gdal_rasterband_h, c_int, c_int, c_void_p]
GDALReadBlock.errcheck = cplerr_errcheck

GDALWriteBlock = _libgdal.GDALWriteBlock
GDALWriteBlock.restype = c_int
GDALWriteBlock.argtypes = [gdal_rasterband_h, c_int, c_int, c_void_p]
GDALWriteBlock.errcheck = cplerr_errcheck

GDALGetRasterBandXSize = _libgdal.GDALGetRasterBandXSize
GDALGetRasterBandXSize.restype = c_int
GDALGetRasterBandXSize.argtypes = [gdal_rasterband_h]

GDALGetRasterBandYSize = _libgdal.GDALGetRasterBandYSize
GDALGetRasterBandYSize.restype = c_int
GDALGetRasterBandYSize.argtypes = [gdal_rasterband_h]

GDALGetRasterAccess = _libgdal.GDALGetRasterAccess
GDALGetRasterAccess.restype = c_int
GDALGetRasterAccess.argtypes = [gdal_rasterband_h]

GDALGetBandNumber = _libgdal.GDALGetBandNumber
GDALGetBandNumber.restype = c_int
GDALGetBandNumber.argtypes = [gdal_rasterband_h]

GDALGetBandDataset = _libgdal.GDALGetBandDataset
GDALGetBandDataset.restype = gdal_dataset_h
GDALGetBandDataset.argtypes = [gdal_rasterband_h]

GDALGetRasterColorInterpretation = _libgdal.GDALGetRasterColorInterpretation
GDALGetRasterColorInterpretation.restype = c_int
GDALGetRasterColorInterpretation.argtypes = [gdal_rasterband_h]

GDALSetRasterColorInterpretation = _libgdal.GDALSetRasterColorInterpretation
GDALSetRasterColorInterpretation.restype = c_int
GDALSetRasterColorInterpretation.argtypes = [gdal_rasterband_h, c_int]
GDALSetRasterColorInterpretation.errcheck = cplerr_errcheck

GDALGetRasterColorTable = _libgdal.GDALGetRasterColorTable
GDALGetRasterColorTable.restype = gdal_color_table_h
GDALGetRasterColorTable.argtypes = [gdal_rasterband_h]

GDALSetRasterColorTable = _libgdal.GDALSetRasterColorTable
GDALSetRasterColorTable.restype = c_int
GDALSetRasterColorTable.argtypes = [gdal_rasterband_h, gdal_color_table_h]
GDALSetRasterColorTable.errcheck = cplerr_errcheck

GDALHasArbitraryOverviews = _libgdal.GDALHasArbitraryOverviews
GDALHasArbitraryOverviews.restype = c_int
GDALHasArbitraryOverviews.argtypes = [gdal_rasterband_h]

GDALGetOverviewCount = _libgdal.GDALGetOverviewCount
GDALGetOverviewCount.restype = c_int
GDALGetOverviewCount.argtypes = [gdal_rasterband_h]

GDALGetOverview = _libgdal.GDALGetOverview
GDALGetOverview.restype = gdal_rasterband_h
GDALGetOverview.argtypes = [gdal_rasterband_h, c_int]

GDALGetRasterNoDataValue = _libgdal.GDALGetRasterNoDataValue
GDALGetRasterNoDataValue.restype = c_double
GDALGetRasterNoDataValue.argtypes = [gdal_rasterband_h, POINTER(c_int)]

GDALSetRasterNoDataValue = _libgdal.GDALSetRasterNoDataValue
GDALSetRasterNoDataValue.restype = c_int
GDALSetRasterNoDataValue.argtypes = [gdal_rasterband_h, c_double]
GDALSetRasterNoDataValue.errcheck = cplerr_errcheck


"""
char **     GDALGetRasterCategoryNames (GDALRasterBandH)
    Fetch the list of category names for this raster. 
CPLErr  GDALSetRasterCategoryNames (GDALRasterBandH, char **)
    Set the category names for this band.
"""

GDALGetRasterMinimum = _libgdal.GDALGetRasterMinimum
GDALGetRasterMinimum.restype = c_double
GDALGetRasterMinimum.argtypes = [gdal_rasterband_h, POINTER(c_int)]

GDALGetRasterMaximum = _libgdal.GDALGetRasterMaximum
GDALGetRasterMaximum.restype = c_double
GDALGetRasterMaximum.argtypes = [gdal_rasterband_h, POINTER(c_int)]

"""
CPLErr  GDALGetRasterStatistics (GDALRasterBandH, int bApproxOK, int bForce, double *pdfMin, double *pdfMax, double *pdfMean, double *pdfStdDev)
    Fetch image statistics. 
CPLErr  GDALComputeRasterStatistics (GDALRasterBandH, int bApproxOK, double *pdfMin, double *pdfMax, double *pdfMean, double *pdfStdDev, GDALProgressFunc pfnProgress, void *pProgressData)
    Compute image statistics. 
CPLErr  GDALSetRasterStatistics (GDALRasterBandH hBand, double dfMin, double dfMax, double dfMean, double dfStdDev)
    Set statistics on band. 
"""

GDALGetRasterUnitType = _libgdal.GDALGetRasterUnitType
GDALGetRasterUnitType.restype = c_char_p
GDALGetRasterUnitType.argtypes = [gdal_rasterband_h]

GDALSetRasterUnitType = _libgdal.GDALSetRasterUnitType
GDALSetRasterUnitType.restype = c_int
GDALSetRasterUnitType.argtypes = [gdal_rasterband_h, c_char_p]
GDALSetRasterUnitType.errcheck = cplerr_errcheck

GDALGetRasterOffset = _libgdal.GDALGetRasterOffset
GDALGetRasterOffset.restype = c_char_p
GDALGetRasterOffset.argtypes = [gdal_rasterband_h, POINTER(c_int)]

GDALSetRasterOffset = _libgdal.GDALSetRasterOffset
GDALSetRasterOffset.restype = c_int
GDALSetRasterOffset.argtypes = [gdal_rasterband_h, c_double]
GDALSetRasterOffset.errcheck = cplerr_errcheck

GDALGetRasterScale = _libgdal.GDALGetRasterScale
GDALGetRasterScale.restype = c_char_p
GDALGetRasterScale.argtypes = [gdal_rasterband_h, POINTER(c_int)]

GDALSetRasterScale = _libgdal.GDALSetRasterScale
GDALSetRasterScale.restype = c_int
GDALSetRasterScale.argtypes = [gdal_rasterband_h, c_double]
GDALSetRasterScale.errcheck = cplerr_errcheck

"""
void    GDALComputeRasterMinMax (GDALRasterBandH hBand, int bApproxOK, double adfMinMax[2])
    Compute the min/max values for a band. 
CPLErr  GDALFlushRasterCache (GDALRasterBandH hBand)
    Flush raster data cache. 
CPLErr  GDALGetRasterHistogram (GDALRasterBandH hBand, double dfMin, double dfMax, int nBuckets, int *panHistogram, int bIncludeOutOfRange, int bApproxOK, GDALProgressFunc pfnProgress, void *pProgressData)
    Compute raster histogram. 
CPLErr  GDALGetDefaultHistogram (GDALRasterBandH hBand, double *pdfMin, double *pdfMax, int *pnBuckets, int **ppanHistogram, int bForce, GDALProgressFunc pfnProgress, void *pProgressData)
    Fetch default raster histogram. 
CPLErr  GDALSetDefaultHistogram (GDALRasterBandH hBand, double dfMin, double dfMax, int nBuckets, int *panHistogram)
    Set default histogram. 
int     GDALGetRandomRasterSample (GDALRasterBandH, int, float *)
GDALRasterBandH     GDALGetRasterSampleOverview (GDALRasterBandH, int)
    Fetch best sampling overview. 
"""

GDALFillRaster = _libgdal.GDALFillRaster
GDALFillRaster.restype = c_int
GDALFillRaster.argtypes = [gdal_rasterband_h, c_double, c_double]
GDALFillRaster.errcheck = cplerr_errcheck

"""
CPLErr  GDALComputeBandStats (GDALRasterBandH hBand, int nSampleStep, double *pdfMean, double *pdfStdDev, GDALProgressFunc pfnProgress, void *pProgressData)
CPLErr  GDALOverviewMagnitudeCorrection (GDALRasterBandH hBaseBand, int nOverviewCount, GDALRasterBandH *pahOverviews, GDALProgressFunc pfnProgress, void *pProgressData)
GDALRasterAttributeTableH   GDALGetDefaultRAT (GDALRasterBandH hBand)
    Fetch default Raster Attribute Table. 
CPLErr  GDALSetDefaultRAT (GDALRasterBandH, GDALRasterAttributeTableH)
    Set default Raster Attribute Table. 
CPLErr  GDALAddDerivedBandPixelFunc (const char *pszName, GDALDerivedPixelFunc pfnPixelFunc)
    This adds a pixel function to the global list of available pixel functions for derived bands. 
"""

GDALGetMaskBand = _libgdal.GDALGetMaskBand
GDALGetMaskBand.restype = gdal_rasterband_h
GDALGetMaskBand.argtypes = [gdal_rasterband_h]

GDALGetMaskFlags = _libgdal.GDALGetMaskFlags
GDALGetMaskFlags.restype = c_int
GDALGetMaskFlags.argtypes = [gdal_rasterband_h]

GDALCreateMaskBand = _libgdal.GDALCreateMaskBand
GDALCreateMaskBand.restype = c_int
GDALCreateMaskBand.argtypes = [gdal_rasterband_h, c_int]
GDALCreateMaskBand.errcheck = cplerr_errcheck

"""
GDALAsyncStatusType     GDALARGetNextUpdatedRegion (GDALAsyncReaderH hARIO, double dfTimeout, int *pnXBufOff, int *pnYBufOff, int *pnXBufSize, int *pnYBufSize)
int     GDALARLockBuffer (GDALAsyncReaderH hARIO, double dfTimeout)
void    GDALARUnlockBuffer (GDALAsyncReaderH hARIO)
int     GDALGeneralCmdLineProcessor (int nArgc, char ***ppapszArgv, int nOptions)
    General utility option processing. 
void    GDALSwapWords (void *pData, int nWordSize, int nWordCount, int nWordSkip)
    Byte swap words in-place. 
void    GDALCopyWords (void *pSrcData, GDALDataType eSrcType, int nSrcPixelOffset, void *pDstData, GDALDataType eDstType, int nDstPixelOffset, int nWordCount)
    Copy pixel words from buffer to buffer. 
void    GDALCopyBits (const GByte *pabySrcData, int nSrcOffset, int nSrcStep, GByte *pabyDstData, int nDstOffset, int nDstStep, int nBitCount, int nStepCount)
    Bitwise word copying. 
int     GDALLoadWorldFile (const char *, double *)
    Read ESRI world file. 
int     GDALReadWorldFile (const char *, const char *, double *)
    Read ESRI world file. 
int     GDALWriteWorldFile (const char *, const char *, double *)
    Write ESRI world file. 
int     GDALLoadTabFile (const char *, double *, char **, int *, GDAL_GCP **)
int     GDALReadTabFile (const char *, double *, char **, int *, GDAL_GCP **)
int     GDALLoadOziMapFile (const char *, double *, char **, int *, GDAL_GCP **)
int     GDALReadOziMapFile (const char *, double *, char **, int *, GDAL_GCP **)
char **     GDALLoadRPBFile (const char *pszFilename, char **papszSiblingFiles)
char **     GDALLoadRPCFile (const char *pszFilename, char **papszSiblingFiles)
CPLErr  GDALWriteRPBFile (const char *pszFilename, char **papszMD)
char **     GDALLoadIMDFile (const char *pszFilename, char **papszSiblingFiles)
CPLErr  GDALWriteIMDFile (const char *pszFilename, char **papszMD)
"""

GDALDecToDMS = _libgdal.GDALDecToDMS
GDALDecToDMS.restype = c_char_p
GDALDecToDMS.argtypes = [c_double, c_char_p, c_int]

GDALPackedDMSToDec = _libgdal.GDALPackedDMSToDec
GDALPackedDMSToDec.restype = c_double
GDALPackedDMSToDec.argtypes = [c_double]

GDALDecToPackedDMS = _libgdal.GDALDecToPackedDMS
GDALDecToPackedDMS.restype = c_double
GDALDecToPackedDMS.argtypes = [c_double]

GDALVersionInfo = _libgdal.GDALVersionInfo
GDALVersionInfo.restype = c_char_p
GDALVersionInfo.argtypes = [c_char_p]




"""
const char *    GDALVersionInfo (const char *)
    Get runtime version information. 
int     GDALCheckVersion (int nVersionMajor, int nVersionMinor, const char *pszCallingComponentName)
    Return TRUE if GDAL library version at runtime matches nVersionMajor.nVersionMinor. 
int     GDALExtractRPCInfo (char **, GDALRPCInfo *)
GDALColorTableH     GDALCreateColorTable (GDALPaletteInterp)
    Construct a new color table. 
void    GDALDestroyColorTable (GDALColorTableH)
    Destroys a color table. 
GDALColorTableH     GDALCloneColorTable (GDALColorTableH)
    Make a copy of a color table. 
GDALPaletteInterp   GDALGetPaletteInterpretation (GDALColorTableH)
    Fetch palette interpretation. 
int     GDALGetColorEntryCount (GDALColorTableH)
    Get number of color entries in table. 
const GDALColorEntry *  GDALGetColorEntry (GDALColorTableH, int)
    Fetch a color entry from table. 
int     GDALGetColorEntryAsRGB (GDALColorTableH, int, GDALColorEntry *)
    Fetch a table entry in RGB format. 
void    GDALSetColorEntry (GDALColorTableH, int, const GDALColorEntry *)
    Set entry in color table. 
void    GDALCreateColorRamp (GDALColorTableH hTable, int nStartIndex, const GDALColorEntry *psStartColor, int nEndIndex, const GDALColorEntry *psEndColor)
    Create color ramp. 
GDALRasterAttributeTableH   GDALCreateRasterAttributeTable (void)
    Construct empty table. 
void    GDALDestroyRasterAttributeTable (GDALRasterAttributeTableH)
    Destroys a RAT. 
int     GDALRATGetColumnCount (GDALRasterAttributeTableH)
    Fetch table column count. 
const char *    GDALRATGetNameOfCol (GDALRasterAttributeTableH, int)
    Fetch name of indicated column. 
GDALRATFieldUsage   GDALRATGetUsageOfCol (GDALRasterAttributeTableH, int)
    Fetch column usage value. 
GDALRATFieldType    GDALRATGetTypeOfCol (GDALRasterAttributeTableH, int)
    Fetch column type. 
int     GDALRATGetColOfUsage (GDALRasterAttributeTableH, GDALRATFieldUsage)
    Fetch column index for given usage. 
int     GDALRATGetRowCount (GDALRasterAttributeTableH)
    Fetch row count. 
const char *    GDALRATGetValueAsString (GDALRasterAttributeTableH, int, int)
    Fetch field value as a string. 
int     GDALRATGetValueAsInt (GDALRasterAttributeTableH, int, int)
    Fetch field value as a integer. 
double  GDALRATGetValueAsDouble (GDALRasterAttributeTableH, int, int)
    Fetch field value as a double. 
void    GDALRATSetValueAsString (GDALRasterAttributeTableH, int, int, const char *)
    Set field value from string. 
void    GDALRATSetValueAsInt (GDALRasterAttributeTableH, int, int, int)
    Set field value from integer. 
void    GDALRATSetValueAsDouble (GDALRasterAttributeTableH, int, int, double)
    Set field value from double. 
int     GDALRATChangesAreWrittenToFile (GDALRasterAttributeTableH hRAT)
    Determine whether changes made to this RAT are reflected directly in the dataset. 
CPLErr  GDALRATValuesIOAsDouble (GDALRasterAttributeTableH hRAT, GDALRWFlag eRWFlag, int iField, int iStartRow, int iLength, double *pdfData)
    Read or Write a block of doubles to/from the Attribute Table. 
CPLErr  GDALRATValuesIOAsInteger (GDALRasterAttributeTableH hRAT, GDALRWFlag eRWFlag, int iField, int iStartRow, int iLength, int *pnData)
    Read or Write a block of ints to/from the Attribute Table. 
CPLErr  GDALRATValuesIOAsString (GDALRasterAttributeTableH hRAT, GDALRWFlag eRWFlag, int iField, int iStartRow, int iLength, char **papszStrList)
    Read or Write a block of strings to/from the Attribute Table. 
void    GDALRATSetRowCount (GDALRasterAttributeTableH, int)
    Set row count. 
CPLErr  GDALRATCreateColumn (GDALRasterAttributeTableH, const char *, GDALRATFieldType, GDALRATFieldUsage)
    Create new column. 
CPLErr  GDALRATSetLinearBinning (GDALRasterAttributeTableH, double, double)
    Set linear binning information. 
int     GDALRATGetLinearBinning (GDALRasterAttributeTableH, double *, double *)
    Get linear binning information. 
CPLErr  GDALRATInitializeFromColorTable (GDALRasterAttributeTableH, GDALColorTableH)
    Initialize from color table. 
GDALColorTableH     GDALRATTranslateToColorTable (GDALRasterAttributeTableH, int nEntryCount)
    Translate to a color table. 
void    GDALRATDumpReadable (GDALRasterAttributeTableH, FILE *)
    Dump RAT in readable form. 
GDALRasterAttributeTableH   GDALRATClone (GDALRasterAttributeTableH)
    Copy Raster Attribute Table. 
int     GDALRATGetRowOfValue (GDALRasterAttributeTableH, double)
    Get row for pixel value. 
void    GDALSetCacheMax (int nBytes)
    Set maximum cache memory. 
int     GDALGetCacheMax (void)
    Get maximum cache memory. 
int     GDALGetCacheUsed (void)
    Get cache memory used. 
void    GDALSetCacheMax64 (GIntBig nBytes)
    Set maximum cache memory. 
GIntBig     GDALGetCacheMax64 (void)
    Get maximum cache memory. 
GIntBig     GDALGetCacheUsed64 (void)
    Get cache memory used. 
int     GDALFlushCacheBlock (void)
    Try to flush one cached raster block. 
CPLVirtualMem *     GDALDatasetGetVirtualMem (GDALDatasetH hDS, GDALRWFlag eRWFlag, int nXOff, int nYOff, int nXSize, int nYSize, int nBufXSize, int nBufYSize, GDALDataType eBufType, int nBandCount, int *panBandMap, int nPixelSpace, GIntBig nLineSpace, GIntBig nBandSpace, size_t nCacheSize, size_t nPageSizeHint, int bSingleThreadUsage, char **papszOptions)
    Create a CPLVirtualMem object from a GDAL dataset object. 
CPLVirtualMem *     GDALRasterBandGetVirtualMem (GDALRasterBandH hBand, GDALRWFlag eRWFlag, int nXOff, int nYOff, int nXSize, int nYSize, int nBufXSize, int nBufYSize, GDALDataType eBufType, int nPixelSpace, GIntBig nLineSpace, size_t nCacheSize, size_t nPageSizeHint, int bSingleThreadUsage, char **papszOptions)
    Create a CPLVirtualMem object from a GDAL raster band object. 
CPLVirtualMem *     GDALGetVirtualMemAuto (GDALRasterBandH hBand, GDALRWFlag eRWFlag, int *pnPixelSpace, GIntBig *pnLineSpace, char **papszOptions)
    Create a CPLVirtualMem object from a GDAL raster band object. 
CPLVirtualMem *     GDALDatasetGetTiledVirtualMem (GDALDatasetH hDS, GDALRWFlag eRWFlag, int nXOff, int nYOff, int nXSize, int nYSize, int nTileXSize, int nTileYSize, GDALDataType eBufType, int nBandCount, int *panBandMap, GDALTileOrganization eTileOrganization, size_t nCacheSize, int bSingleThreadUsage, char **papszOptions)
    Create a CPLVirtualMem object from a GDAL dataset object, with tiling organization. 
CPLVirtualMem *     GDALRasterBandGetTiledVirtualMem (GDALRasterBandH hBand, GDALRWFlag eRWFlag, int nXOff, int nYOff, int nXSize, int nYSize, int nTileXSize, int nTileYSize, GDALDataType eBufType, size_t nCacheSize, int bSingleThreadUsage, char **papszOptions)
    Create a CPLVirtualMem object from a GDAL rasterband object, with tiling organization. 
"""


