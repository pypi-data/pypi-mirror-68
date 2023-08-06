# Time Series Pattern Finding

The TSPatternFinding package is a collection of Python scripts aimed
at finding reoccuring patterns of various types in time series data.

This package is aimed at time series data extracted from network logs and
packet captures.  However, most functions are generic enough to be applied
to any time series data.  Though results are presented with a network event
focus.

## Approaches

### Stomp

STOMP is a highly efficient approach to "time motifs" discovery in time
series data and one of several of USR's Matrix Profile data mining approaches
(SCRIMP).  Time motifs are repeating patterns which indicate an underlying
common cause.  Details on these approaches can be [found here][scrimp paper].

### Haar

The Haar approach is based on a full decomposition of the time series using
haar wavelets. A detailed description of this approach can be 
[found here.][low-rate periodicity paper].

Most of the configuration for a Python project is done in the `setup.py` file,
an example of which is included in this project. You should edit this file
accordingly to adapt this sample project to your needs.

----
[scrimp paper]: https://www.cs.ucr.edu/~eamonn/SCRIMP_ICDM_camera_ready_updated.pdf
[low-rate periodicity paper]: https://www.isi.edu/~johnh/PAPERS/Bartlett11a.pdf
