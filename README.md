pygdal
======

Pythonic and full control GDAL.


Why?
----

The GDAL Python bindings are disputed and do not offer the full functionality 
compared to the C or C++ API. Also it is not quite "pythonic", in the sense 
that it does not really make advantage of Python language features.

How?
----

pygdal is split into a lower and a higher level API:

 - The lower level API is a direct interface to the GDAL C API, with few 
   adaptions like proper exception translation.
 - The higher level API Enables a "pythonic" and natural approach, very much 
   like the former GDAL Python API, but with additional features. This layer 
   will also integrate numpy for reading and writing data.

GDAL will be interfaced via ctypes, thus no compilation is necessary. Only 
numpy will be an additional dependency.


