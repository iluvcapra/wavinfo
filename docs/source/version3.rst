Breaking Changes in Version 3 from Version2
=============================================

Library and Module Reorganization
----------------------------------

* All reader modules, including ``wave_reader`` the module that implements
  ``WavInfoReader`` have been moved into a ``readers`` folder. ``WavInfoReader``
  is itself still imported by the top-level ``__init__.py`` so is still 
  accessible there.
* All implementation code for specific metadata scopes has been moved into a 
  ``scopes`` folder and the names of the modules have been shortened to 
  reflect these modules now implement reader and writer methods.

Renamed Parameters in ``WavInfoReader``
----------------------------------------

* The ``path`` parameter has been renamed ``f`` to more accurately reflect
  it's function as both a ``PathLike`` and a ``IO``
