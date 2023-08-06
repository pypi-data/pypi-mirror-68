import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="pyplayingcards",
    version="1.0.3",
    description="Create and manipulate playing cards in Python!",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/DaJodhi/pyplayingcards",
    author="Jodhviir Sekhon",
    author_email="jodhsekh07@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["pyplayingcards"]
)
