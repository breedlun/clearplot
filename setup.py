from distutils.core import setup
import os, sys
import matplotlib as mpl

#Define the version of clearplot
cp_version = '1.0.3'

#Find where matplotlib stores its True Type fonts
mpl_data_dir = os.path.dirname(mpl.matplotlib_fname())
mpl_ttf_dir = os.path.join(mpl_data_dir, 'fonts', 'ttf')

#Wheels do not support absolute paths for `data_files`.  (pip 7.0 (I think) and later 
#automatically downloads PiPI packages as a wheel, even if it was uploaded as a sdist.  
#See discussion at: https://bitbucket.org/pypa/wheel/issues/92 for further information.)
if 'bdist_wheel' in sys.argv:
    raise RuntimeError("This setup.py does not support wheels")

setup(
    name = 'clearplot',
    packages = ['clearplot'], # this must be the same as the name above
    version = cp_version,
    description = 'Clearplot creates publication quality plots using matplotlib',
    author = 'Benjamin Reedlunn',
    author_email = 'breedlun@gmail.com',
    license = 'MIT',
    url = 'http://clearplot.readthedocs.org',
    download_url = 'https://github.com/breedlun/clearplot/tarball/' + cp_version,
    keywords = ['matplotlib', 'plotting'],
    classifiers = [
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',
        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',
	    # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2 :: Only',
        'Programming Language :: Python :: 2.7',
        # Indicate who your project is intended for
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Visualization'],
    install_requires = ['matplotlib >= 1.4.0, !=1.4.3', 'numpy >= 1.6'],
    data_files = [
        (mpl_ttf_dir, ['./font_files/TeXGyreHeros-txfonts/TeXGyreHerosTXfonts-Regular.ttf']),
        (mpl_ttf_dir, ['./font_files/TeXGyreHeros-txfonts/TeXGyreHerosTXfonts-Italic.ttf'])]
)

#Try to delete matplotlib's fontList cache
mpl_cache_dir = mpl.get_cachedir()
mpl_cache_dir_ls = os.listdir(mpl_cache_dir)
if 'fontList.cache' in mpl_cache_dir_ls:
    fontList_path = os.path.join(mpl_cache_dir, 'fontList.cache')
    os.remove(fontList_path)
