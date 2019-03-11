from distutils.core import setup
from Cython.Build import cythonize

#python setup.py build_ext --inplace
#E:\Python36-64\python.exe setup.py build_ext --inplace
#E:\Python36-64\Lib\ant\cmath
setup(
   #ext_modules = cythonize("helloworld.pyx")
   ext_modules = cythonize("cmath.pyx")
)