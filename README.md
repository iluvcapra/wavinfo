[![Build Status](https://travis-ci.com/iluvcapra/wavinfo.svg?branch=master)](https://travis-ci.com/iluvcapra/wavinfo)
[![Documentation Status](https://readthedocs.org/projects/wavinfo/badge/?version=latest)](https://wavinfo.readthedocs.io/en/latest/?badge=latest) ![](https://img.shields.io/github/license/iluvcapra/wavinfo.svg) ![](https://img.shields.io/pypi/pyversions/wavinfo.svg) [![](https://img.shields.io/pypi/v/wavinfo.svg)](https://pypi.org/project/wavinfo/) ![](https://img.shields.io/pypi/wheel/wavinfo.svg)


# wavinfo

The `wavinfo` package allows you to probe WAVE files and extract extended metadata, with an emphasis on 
production metadata. 

`wavinfo` reads:

* Broadcast-WAVE metadata, compliant with [EBU Tech 3285v2 (2011)][ebu], though other versions are easy to implement. This includes the [SMPTE 330M:2011 Unique Material Identifier (UMID)][smpte_330m2011] for the file, if it exists. 
* [iXML production recorder metadata][ixml], including project, scene, and take tags, recorder notes and file family information.
* The format chunk is also parsed, so you can access the basic sample rate and channel count information.

This module is presently under construction and not sutiable for production at this time.

[ebu]:https://tech.ebu.ch/docs/tech/tech3285.pdf
[smpte_330m2011]:http://standards.smpte.org/content/978-1-61482-678-1/st-330-2011/SEC1.abstract
[ixml]:http://www.ixml.info
