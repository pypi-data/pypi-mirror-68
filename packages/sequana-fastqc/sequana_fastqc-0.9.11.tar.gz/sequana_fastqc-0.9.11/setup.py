__revision__ = "$Id: $" # for the SVN Id
from setuptools import setup, find_namespace_packages

_MAJOR               = 0
_MINOR               = 9
_MICRO               = 11
version              = '%d.%d.%d' % (_MAJOR, _MINOR, _MICRO)
release              = '%d.%d' % (_MAJOR, _MINOR)

metainfo = {
    'authors': {"main": ("thomas cokelaer", "thomas.cokelaer@pasteur.fr")},
    'version': version,
    'license' : 'new BSD',
    'url' : "https://github.com/sequana/",
    'description': "A fastqc pipeline from sequana project." ,
    'platforms' : ['Linux', 'Unix', 'MacOsX', 'Windows'],
    'keywords' : ['fastqc', 'NGS', 'snakemake', 'multiqc', 'sequana'],
    'classifiers' : [
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Education',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Scientific/Engineering :: Bio-Informatics',
          'Topic :: Scientific/Engineering :: Information Analysis',
          'Topic :: Scientific/Engineering :: Mathematics',
          'Topic :: Scientific/Engineering :: Physics']
    }


setup(
    name             = "sequana_fastqc",
    version          = version,
    maintainer       = metainfo['authors']['main'][0],
    maintainer_email = metainfo['authors']['main'][1],
    author           = metainfo['authors']['main'][0],
    author_email     = metainfo['authors']['main'][1],
    long_description = open("README.rst").read(),
    keywords         = metainfo['keywords'],
    description      = metainfo['description'],
    license          = metainfo['license'],
    platforms        = metainfo['platforms'],
    url              = metainfo['url'],
    classifiers      = metainfo['classifiers'],

    # package installation
    packages = ["sequana_pipelines.fastqc",
        'sequana_pipelines.fastqc.data' ],

    install_requires = ["sequana_pipetools>=0.2", "sequana>=0.8.0"],

    # This is recursive include of data files
    exclude_package_data = {"": ["__pycache__"]},
    package_data = {
        '': ['*.yaml', "*.rules", "*.json", "requirements.txt", "*png"],
        'sequana_pipelines.fastqc.data' : ['*.*'], 
        },

    zip_safe=False,

    entry_points = {'console_scripts':[
        'sequana_pipelines_fastqc=sequana_pipelines.fastqc.main:main',
        'sequana_fastqc=sequana_pipelines.fastqc.main:main']
    }

)
