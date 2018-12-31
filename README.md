[![Build Status](https://travis-ci.com/iluvcapra/wavinfo.svg?branch=master)](https://travis-ci.com/iluvcapra/wavinfo)
[![Documentation Status](https://readthedocs.org/projects/wavinfo/badge/?version=latest)](https://wavinfo.readthedocs.io/en/latest/?badge=latest) ![](https://img.shields.io/github/license/iluvcapra/wavinfo.svg) ![](https://img.shields.io/pypi/pyversions/wavinfo.svg) [![](https://img.shields.io/pypi/v/wavinfo.svg)](https://pypi.org/project/wavinfo/) ![](https://img.shields.io/pypi/wheel/wavinfo.svg)


# wavinfo

The `wavinfo` package allows the client to probe WAVE files and extract extended metadata, with an emphasis on 
production metadata. 

`wavinfo` reads:

* Broadcast-WAVE metadata, compliant with EBU Tech 3285v2 (2011), though other versions are easy to implement. This includes the 
  SMPTE Universal Media Identifier (UMID) for the file, if it exists. 
* iXML production recorder metadata, including project, scene, and take tags, recorder notes and file family information.

This module is presently under construction and not sutiable for production at this time.
