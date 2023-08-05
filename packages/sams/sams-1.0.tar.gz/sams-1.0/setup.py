# this setup below helps you to setup your own package in pipy.com for  other member of the community to use
import setuptools
from pathlib import Path

setuptools.setup(

    name="sams",
    version=1.0,
    long_description=Path("test/README.md").read_text(),
    #     if you have other directiory, then you have to exclude thenin find_packages as shown below
    packages=setuptools.find_packages(exclude=["data", "test"])

)
