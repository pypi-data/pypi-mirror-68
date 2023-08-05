#!/usr/bin/env python3
from setuptools import setup, find_packages
from os import path

with open("readme_new.md", encoding="utf-8") as file_description:
    long_description = file_description.read()

__author__ = "Dang Duc Ngoc"
__email__ = "ngoc.dang@f4.intek.edu.vn"
__version__ = "1.0.1"
__copyright__ = "Copyright (C) 2019, Intek Institute"
__credits__ = "Daniel CAUNE"
__license__ = "MIT"
__maintainer__ = "Dang Duc Ngoc"
__url__ = "https://github.com/intek-training-jsc/flickr-mirroring-Friendlyngoc"
__description__ = "A mirror Flickr photostream tool"
__python_version__ = ">=3.6"
__programm_name__ = "Flickr_Mirror_Ngoc_Dang"

setup(
    extras_require={
        "dev": [
            "appdirs==1.4.3",
            "attrs==19.3.0",
            "black==19.10b0; python_version >= '3.6'",
            "cached-property==1.5.1",
            "cerberus==1.3.2",
            "certifi==2020.4.5.1",
            "chardet==3.0.4",
            "click==7.1.2",
            "colorama==0.4.3",
            "distlib==0.3.0",
            "idna==2.9",
            "importlib-metadata==1.6.0; python_version < '3.8'",
            "orderedmultidict==1.0.1",
            "packaging==20.3",
            "pathspec==0.8.0",
            "pep517==0.8.2",
            "pip-shims==0.5.2",
            "pipenv-setup==3.0.1",
            "pipfile==0.0.2",
            "plette[validation]==0.2.3",
            "pyparsing==2.4.7",
            "python-dateutil==2.8.1",
            "regex==2020.5.7",
            "requests==2.23.0",
            "requirementslib==1.5.7",
            "six==1.14.0",
            "toml==0.10.0",
            "tomlkit==0.6.0",
            "typed-ast==1.4.1; implementation_name == 'cpython' and python_version < '3.8'",
            "typing==3.7.4.1",
            "urllib3==1.25.9",
            "vistir==0.5.0",
            "wheel==0.34.2",
            "zipp==3.1.0",
        ]
    },
    install_requires=[
        "astroid==2.4.1",
        "certifi==2020.4.5.1",
        "chardet==3.0.4",
        "idna==2.9",
        "isort==4.3.21",
        "langdetect==1.0.8",
        "lazy-object-proxy==1.4.3",
        "mccabe==0.6.1",
        "pylint==2.5.2",
        "requests==2.23.0",
        "six==1.14.0",
        "toml==0.10.0",
        "typed-ast==1.4.1; implementation_name == 'cpython' and python_version < '3.8'",
        "urllib3==1.25.9",
        "wrapt==1.12.1",
    ],
    entry_points={
        'console_scripts': ['mirror_flickr=mirroring_flickr.flickr:main'],
    },
    packages=find_packages(),
    name=__programm_name__,
    version=__version__,
    description=__description__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=__url__,
    author=__author__,
    author_email=__email__,
    license=__license__,
    maintainer=__maintainer__,
    python_requires=__python_version__
)
