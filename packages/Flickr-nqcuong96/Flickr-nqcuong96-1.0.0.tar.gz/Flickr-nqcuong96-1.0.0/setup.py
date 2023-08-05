#usr/bin/env python3

import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="Flickr-nqcuong96",
    version="1.0.0",
    description="A tool to mirror Flickr photo",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/intek-training-jsc/flickr-mirroring-nqcuong96",
    author="nqcuong",
    author_email="cuong.nguyen@f4.intek.edu.vn",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["Flickr", "Flickr.model"],
    include_package_data=True,
    install_requires=["langdetect", "iso-639", "iso3166", "requests"],
    entry_points={
        "console_scripts": [
            "mirror_flickr=Flickr.__main__:main",
        ]
    },
)
