from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='wavinfo',
      version='0.1',
      author='Jamie Hardt',
      author_email='jamiehardt@me.com',
      description='WAVE sound file metadata parser.',
      long_description_content_type="text/markdown",
      long_description=long_description,
      url='https://github.com/iluvcapra/wavinfo',
      classifiers=['Development Status :: 2 - Pre-Alpha',
          'License :: OSI Approved :: MIT License',
          'Topic :: Multimedia',
	  'Topic :: Multimedia :: Sound/Audio'],
      packages=['wavinfo'])
