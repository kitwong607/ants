from distutils.core import setup
from Cython.Build import cythonize
import numpy

#C:\Python35\python.exe setup.py build_ext --inplace

setup(
   #ext_modules=cythonize("cmath.pyx"), include_dirs=[numpy.get_include()]
   ext_modules = cythonize("cmath.pyx")
)