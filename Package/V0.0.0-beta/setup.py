from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1-beta'
DESCRIPTION = 'Database interaction'
LONG_DESCRIPTION = """

A Python module to make interacting with SQL databases easier and faster, a wrapper for other alternatives.

"""

# Setting up
setup(
    name="easyDataset",
    version=VERSION,
    author="Password-Classified",
    author_email="user@example.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['wheel', 'setuptools', 'pandas'],
    keywords=['python', 'sql', 'database', 'databases', 'data science', 'machine learning', 'easy'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)