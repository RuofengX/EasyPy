from setuptools import setup
from setuptools import find_packages


VERSION = '0.5.0'
project_urls={
    "Documentation": "https://github.com/RuofengX/EasyPy",
    "Issue tracker": "https://github.com/RuofengX/EasyPy/issues"
}
setup(
    name='Aisle',  # package name
    version=VERSION,  # package version
    description='Some usageful log utils',  # package description
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
    ]
)