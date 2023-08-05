from setuptools import setup, find_packages

setup(
    name = 'siar',
    packages = ['siar'],       
    include_package_data=False,
    version = '0.3',
    description = 'Python client for Siar API (Agroclimatic Information for Spain)',
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

