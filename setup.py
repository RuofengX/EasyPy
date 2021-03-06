from setuptools import setup
from setuptools import find_packages


VERSION = '0.6.2'
project_urls={
    "Documentation": "https://github.com/RuofengX/EasyPy",
    "Issue tracker": "https://github.com/RuofengX/EasyPy/issues"
}
setup(
    name='Aisle',  # package name
    version=VERSION,  # package version
    description='Some useful log utils',  # package description
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        'rich'
    ]
)