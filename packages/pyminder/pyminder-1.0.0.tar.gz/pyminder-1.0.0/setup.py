import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="pyminder",
    python_requires=">3.6",
    version="1.0.0",
    description="Beeminder power tools library",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/narthur/pyminder",
    author="Nathan Arthur",
    author_email="nathan@nathanarthur.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    install_requires=["requests", "natlibpy"],
)
