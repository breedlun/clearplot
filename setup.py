from setuptools import setup
#from pkg_resources import require, DistributionNotFound
from setuptools.command.install import install
import warnings

#Define the version of clearplot
cp_version = '1.0.7'

#Comment out this code in case we switch back to the Qt4Agg backend.
##For now we are using the Qt4Agg backend, which requires PyQt4 or PySide, but 
##PyQt4 is prefered 
#try:
#    require('PyQt4')
#    Qt_pkg = 'PyQt4' 
#except DistributionNotFound:
#    Qt_pkg = 'PySide'

#Set up the machinery to install custom fonts.
#Note: I originally tried to use the data_files keyword in distutil.setup() to 
#install the font files, but this turned into a mess.  Wheels do not support 
#absolute file paths, and the pip project is basically forcing people to use 
#wheels.  Also, in order to find where matplotlib stores its true type fonts 
#and fontList.cache, I had to import matplotlib before setup() had a chance to 
#install matplotlib first.  For more information see this stackoverflow post 
#http://stackoverflow.com/questions/34193900/how-do-i-distribute-fonts-with-my-python-package/34204582
#and the contained links.  Fortunately, we can subclass the setuptools install 
#class in order to run custom commands during installation.  See 
#http://blog.niteoweb.com/setuptools-run-custom-code-in-setup-py/ for more
#information.
class move_ttf(install):
    def run(self):
        """
        Performs the usual install process and then copies the True Type fonts 
        that come with clearplot into matplotlib's True Type font directory, 
        and deletes the matplotlib fontList.cache 
        """
        #Perform the usual install process
        install.run(self)
        #Try to install custom fonts
        try:
            import os, shutil
            import matplotlib as mpl
            import clearplot as cp
            
            #Find where matplotlib stores its True Type fonts
            mpl_data_dir = os.path.dirname(mpl.matplotlib_fname())
            mpl_ttf_dir = os.path.join(mpl_data_dir, 'fonts', 'ttf')
            
            #Copy the font files to matplotlib's True Type font directory
            #(I originally tried to move the font files instead of copy them,
            #but it did not seem to work, so I gave up.)
            cp_ttf_dir = os.path.join(os.path.dirname(cp.__file__), 'true_type_fonts')
            for file_name in os.listdir(cp_ttf_dir):
                if file_name[-4:] == '.ttf':
                    old_path = os.path.join(cp_ttf_dir, file_name)
                    new_path = os.path.join(mpl_ttf_dir, file_name)
                    shutil.copyfile(old_path, new_path)
                    print "Copying " + old_path + " -> " + new_path
            
            #Try to delete matplotlib's fontList cache
            mpl_cache_dir = mpl.get_cachedir()
            mpl_cache_dir_ls = os.listdir(mpl_cache_dir)
            if 'fontList.cache' in mpl_cache_dir_ls:
                fontList_path = os.path.join(mpl_cache_dir, 'fontList.cache')
                os.remove(fontList_path)
                print "Deleted the matplotlib fontList.cache"
        except:
            warnings.warn("WARNING: An issue occured while installing the custom fonts for clearplot.")

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
    #Specify the dependencies and versions
    install_requires = ['matplotlib >= 1.4.0, !=1.4.3', 'numpy >= 1.6'],
    #Specify any non-python files to be distributed with the package
    package_data = {'' : ['color_maps/*.csv', 'true_type_fonts/*.ttf']},
    #Specify the custom install class
    cmdclass={'install' : move_ttf}
)