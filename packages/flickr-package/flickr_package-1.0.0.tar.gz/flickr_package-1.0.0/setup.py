from setuptools import setup, find_packages
import os

__author__ = "Khoi Vo"
__email__ = "khoi.vo@f4.intek.edu.vn"
__copyright__ = "Copyright (C) 2019, Intek Institute"
__version = "1.0.0"
__credits__ = "Daniel CAUNE"
__license__ = "MIT"
__maintainer__ = "Khoi Vo"

with open("README.md", "r") as f:
    long_description = f.read()

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
            "typed-ast==1.4.1",
            "typing==3.7.4.1",
            "urllib3==1.25.9",
            "vistir==0.5.0",
            "wheel==0.34.2",
            "zipp==3.1.0",
        ]
    },
    install_requires=[
        "bleach==3.1.5",
        "certifi==2020.4.5.1",
        "cffi==1.14.0",
        "chardet==3.0.4",
        "cryptography==2.9.2",
        "docutils==0.16",
        "idna==2.9",
        "importlib-metadata==1.6.0; python_version < '3.8'",
        "jeepney==0.4.3; sys_platform == 'linux'",
        "keyring==21.2.1",
        "langdetect==1.0.8",
        "packaging==20.3",
        "pkginfo==1.5.0.1",
        "pycountry==19.8.18",
        "pycparser==2.20",
        "pygments==2.6.1",
        "pyparsing==2.4.7",
        "readme-renderer==26.0",
        "requests==2.23.0",
        "requests-toolbelt==0.9.1",
        "secretstorage==3.1.2; sys_platform == 'linux'",
        "six==1.14.0",
        "tqdm==4.46.0",
        "twine==3.1.1",
        "urllib3==1.25.9",
        "webencodings==0.5.1",
        "wheel==0.34.2",
        "zipp==3.1.0",
    ],
    name="flickr_package",
    version="1.0.0",
    author=__author__,
    author_email=__email__,
    description="flickr_package use to batch download photos from user Flickr",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/intek-training-jsc/flickr-mirroring-KV16",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",
)
