=======
History
=======

0.3.2 (2020-05-08)
------------------

* Suppressed another warning coming from pyresample.


0.3.1 (2020-05-08)
------------------

* Fixed a warning coming from pyresample.


0.3.0 (2020-05-08)
------------------

* Converted all type hints to Python 3.6 style. Dropped Python 3.5 support. Fixed code duplicate.
* Split sensormapgeo module into transformer_2d and transformer_3d.
* SensorMapGeometryTransformer.compute_areadefinition_sensor2map() now directly uses pyresample instead of GDAL if the
  target resolution is given.
* SensorMapGeometryTransformer3D.to_map_geometry() now computes a common area definition only ONCE which saves
  computation time and increases stability.
* The computation of the common extent in 3D geolayers now works properly if target projection is not set to LonLat.
* Added paramter tgt_coordgrid to to_map_geometry methods to automatically move the output extent to a given coordinate
  grid.
* compute_areadefinition_sensor2map() now also adds 1 pixel around the output extent in the pyresample version just
  like in the GDAL version.
* Added some input validation.


0.2.2 (2020-03-10)
------------------

* Fix for always returning 0.1.0 when calling sensormapgeo.__version__.


0.2.1 (2020-03-10)
------------------

* Fix for always returning returning float64 output data type in case of bilinear resampling.
* Added output data type verification to tests.
* Fix for an exception if the output of get_proj4info() contains trailing white spaces
  (fixed by an update of py_tools_ds).
* Improved tests.
* Set channel priority to strict.
* Force libgdal to be installed from conda-forge.
* Fixed broken documentation link


0.2.0 (2020-01-06)
------------------

* Added continous integration.
* Updated readme file.
* Added PyPI release.


0.1.0 (2020-01-06)
------------------

* First release on GitLab.
