from distutils.core import setup

#Define the version of clearplot
cp_version = '1.0.2'

setup(
  name = 'clearplot',
  packages = ['clearplot'], # this must be the same as the name above
  version = cp_version,
  description = 'Clearplot creates publication quality plots using matplotlib',
  author = 'Benjamin Reedlunn',
  author_email = 'breedlun@gmail.com',
  url = 'http://clearplot.readthedocs.org',
  download_url = 'https://github.com/breedlun/clearplot/tarball/' + cp_version,
  keywords = ['matplotlib', 'plotting'],
  classifiers = [],
)