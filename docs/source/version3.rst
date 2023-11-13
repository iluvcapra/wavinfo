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
* Scope data types have been renamed and all parsing logic has been moved into 
  correspdonding ``read()`` functions defined in the module scope. In almost 
  all cases these data objects will have the same properties and methods as 
  in Version 2. Deviations from Version 2 will be noted below.


Renamed Parameters in ``WavInfoReader``
----------------------------------------

* The ``path`` parameter has been renamed ``f`` to more accurately reflect
  it's function as both a ``PathLike`` and a ``IO``


``INFO`` metadata
-----------------

* Removed non-standard ``tape`` field
* Removed ``album`` field that was alias for ``product``


``cue`` metadata
----------------

* The ``cues`` property of the ``CueList`` object is now a dictionary instead 
  of a list that indexes cue entries by their ``name``.
