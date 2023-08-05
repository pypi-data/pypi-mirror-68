import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

__author__ = "Thu Hoai"
__copyright__ = "Copyright (C) 2020, Intek Institute"
__credits__ = ["Thu Hoai"]
__email__ = "hoai.le@f4.intek.edu.vn"
__license__ = "MIT"
__maintainer__ = "Thu Hoai"
__version__ = "1.0.2"

# This call to setup() does all the work
setup(
    name="flickr_photostream_mirroring",
    version=__version__,
    description="Flickr mirroring",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/intek-training-jsc/flickr-mirroring-hoaithu1.git",
    author=__author__,
    author_email=__email__,
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["flickr_photostream"],
    include_package_data=True,
    install_requires=[
        "certifi==2020.4.5.1",
        "chardet==3.0.4",
        "idna==2.9",
        "langdetect==1.0.8",
        "requests==2.23.0",
        "six==1.14.0",
        "urllib3==1.25.9",
    ],
    entry_points={
        "console_scripts": ["mirror_flickr=flickr_photostream.__main__:main"],
    },
    python_requires=">=3.6",
)
