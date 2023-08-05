import setuptools
from pathlib import Path

setuptools.setup(
    name="mjpdf",
    author="Monir Hossain",
    author_email="monir.ja.10@gmail.com",
    version=1.0,
    long_description=Path("README.md").read_text(),
    packages=setuptools.find_packages(exclude=["data", "test"])
)
