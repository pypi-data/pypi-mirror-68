import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "cli-typingtest-NathanBitTheMoon",
    version = "1.0",
    author = "NathanBitTheMoon",
    description = ("A command line typing test written using curses in Python 3"),
    license = "BSD",
    keywords = "cli typing test wpm cpm",
    python_requires = '>=3.6'
)