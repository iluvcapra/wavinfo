from setuptools import setup
from metadata import __author__, __license__, __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='wavinfo',
      version=__version__,
      author=__author__,
      author_email='jamiehardt@me.com',
      description='Probe WAVE Files for iXML, Broadcast-WAVE and other metadata.',
      long_description_content_type="text/markdown",
      long_description=long_description,
      license=__license__,
      url='https://github.com/iluvcapra/wavinfo',
      project_urls={
          'Source':
              'https://github.com/iluvcapra/wavinfo',
          'Documentation':
              'https://wavinfo.readthedocs.io/',
          'Issues':
              'https://github.com/iluvcapra/wavinfo/issues',
      },
      packages=['wavinfo'],
      classifiers=['Development Status :: 5 - Production/Stable',
          'License :: OSI Approved :: MIT License',
          'Topic :: Multimedia',
          'Topic :: Multimedia :: Sound/Audio',
          "Programming Language :: Python :: 3.8",
          "Programming Language :: Python :: 3.9",
          "Programming Language :: Python :: 3.10"],
      keywords='waveform metadata audio ebu smpte avi library film tv editing editorial',
      install_requires=['lxml'],
      entry_points={
          'console_scripts': [
              'wavinfo = wavinfo.__main__:main'
          ]
      }
      )
