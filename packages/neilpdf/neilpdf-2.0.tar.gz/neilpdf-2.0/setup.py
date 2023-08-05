import setuptools
from pathlib import Path

setuptools.setup(
    name="neilpdf",
    version=2.0,
    long_decription=Path("README.md").read_text,
    packages=setuptools.find_packages(exclude=["tests", "data"])
)
