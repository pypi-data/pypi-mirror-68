import setuptools
from os import path
this_directory = path.abspath(path.dirname(__file__))
setuptools.setup(
    name='syyDlib',
    version='0.0.6',
    author='Jay',
    description='for test',
    packages=setuptools.find_packages()
)
