"""Setup script for vennam master"""

import os.path
from setuptools import setup

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

# This call to setup() does all the work
setup(
    name="vennam",
    version="1.1",
    description="This package will helps to convert DataFrame to Dictionary and provide Exploratory Data Analysis.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/deva567/vennam_dftodict",
    author="Vennam",
    author_email="vennamdevendhar@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["vennam"],
    include_package_data=True,
    install_requires=[
        "pandas","wordcloud","nltk","matplotlib","Pillow"
    ],
)