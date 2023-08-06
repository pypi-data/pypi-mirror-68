from setuptools import setup, find_packages

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = 'siar',
    packages = ['siar'],       
    include_package_data=False,
    version = '0.6',
    description = 'Python client for Siar API (Agroclimatic Information for Spain)',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Rafael Arellano',
    author_email="rarellano-dev@riseup.net",
    license="AGPLv3",
    url="https://github.com/rarelano/python-siar",
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Intended Audience :: Developers",
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent"
    ],
)

