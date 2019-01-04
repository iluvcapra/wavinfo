.. wavinfo documentation master file, created by
   sphinx-quickstart on Thu Jan  3 17:09:28 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to wavinfo's documentation!
===================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

.. module:: wavinfo

.. autoclass:: WavInfoReader

   .. automethod:: __init__
   
   .. attribute:: fmt

      Audio format.

   .. attribute:: data

      Statistics on the audio data.

   .. attribute:: bext

      Broadcast-WAV metadata.

   .. attribute:: ixml
      
      iXML metadata.

   .. attribute:: info

      RIFF INFO metadata.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
