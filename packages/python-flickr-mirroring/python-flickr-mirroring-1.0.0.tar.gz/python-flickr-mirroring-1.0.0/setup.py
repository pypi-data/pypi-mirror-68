from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

__name__ = "python-flickr-mirroring"
__author__ = "Long Nguyen"
__copyright__ = "Copyright (C) 2020, Intek Institute"
__email__ = "long.nguyen@f4.intek.edu.com"
__description__ = "CLI for mirroring flickr photos of a specific user"
__long_description_content_type__ = "text/markdown"

__version__ = "1.0.0"
__github_url__ = "https://github.com/intek-training-jsc/flickr-mirroring-Long-Nguyen-96"

__language__ = "Programming Language :: Python :: 3"
__license__ = "License :: OSI Approved :: MIT License"
__os__ = "Operating System :: OS Independent"
__maintainer__ = "Long Nguyen"

__python_version__ = ">=3.6"


setup(
    install_requires=[
        "attrs==19.3.0",
        "certifi==2020.4.5.1",
        "chardet==3.0.4",
        "idna==2.9",
        "importlib-metadata==1.6.0; python_version < '3.8'",
        "langdetect==1.0.8",
        "more-itertools==8.2.0",
        "mpmath==1.1.0",
        "packaging==20.3",
        "pluggy==0.13.1",
        "py==1.8.1",
        "pyparsing==2.4.7",
        "pytest==5.4.2",
        "requests==2.23.0",
        "six==1.14.0",
        "sympy==1.5.1",
        "urllib3==1.25.9",
        "wcwidth==0.1.9",
        "zipp==3.1.0",
    ],
    name=__name__,
    version=__version__,
    author=__author__,
    author_email=__email__,
    description=__description__,
    long_description=long_description,
    long_description_content_type=__long_description_content_type__,
    url=__github_url__,
    packages=["flickr"],
    entry_points={"console_scripts": ["mirror_flickr=flickr.__main__:main"]},
    classifiers=[__language__, __license__, __os__],
    python_requires=__python_version__,
)
