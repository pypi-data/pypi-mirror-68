from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy

ext_modules = [ 
    Extension('pymt64',
               libraries = ['m'],
              depends  = ['mt64mp.h', 'pymt64lib.h'],
               sources   = ['pymt64.pyx','pymt64lib.c','mt19937-64mp.c'], 
               include_dirs=[numpy.get_include()] )
    ]


setup(name = 'PyMT64',
      version = '1.9',
      description = 'Python version of the Mersenne Twister 64-bit pseudorandom number generator',
      author = 'R. Samadi',
      author_email = 'reza.samadi@obspm.fr',
      url =  'http://lesia.obspm.fr/',
      long_description = open('README.txt').read(),
      long_description_content_type='text/markdown',
      ext_modules =  cythonize(ext_modules)
      )
