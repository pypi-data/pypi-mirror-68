"""
Description of project with title, state and further constants
"""
import os
__all__ = [
    "__version__",
    "__title__",
    "__summary__",
    "__keywords__",
    "__uri__",
    "__author__",
    "__email__",
    "__license__",
    "__copyright__",
    "__python_requires__",
    "__dependencies__",
    "__classifiers__",
]
__version__ = '0.1.3'
__title__ = os.path.basename(os.path.abspath('.'))
__summary__ = ("Convenience methods for magnetic field "
               "evaluations evolved around the stellarator Wendelstein 7-X."),
__keywords__ = "Wendelstein 7-X magnetic field field line diffusion VMEC EXTENDER",
__uri__ = 'https://gitlab.mpcdf.mpg.de/dboe/w7x'
__author__ = "Daniel Boeckenhoff"
__email__ = "daniel.boeckenhoff@ipp.mpg.de"
__license__ = "Apache Software License"
__copyright__ = "2018 %s" % __author__
__python_requires__ = '>=2.7'
__dependencies__ = [
    'pathlib2;python_version<"3.0"',
    'pathlib;python_version>="3.0"',
    'osa',
    'symfit',
    'joblib',
    'argparse',
    'transcoding',
    'tfields',  # includes many other dependencies
]
__classifiers__ = [
    # find the full list of possible classifiers at https://pypi.org/classifiers/
    'Development Status :: 3 - Alpha',
    'License :: OSI Approved :: {0}'.format(__license__),
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
]
