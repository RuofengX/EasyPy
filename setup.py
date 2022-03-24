from setuptools import setup
from setuptools import find_packages


VERSION = '0.0.0'

setup(
    name='Aisle',  # package name
    version=VERSION,  # package version
    description='Some usageful log utils',  # package description
    packages=find_packages(),
    zip_safe=False,
)