from setuptools import setup
import subprocess
import sys

if (sys.version_info.major, sys.version_info.minor) < (3, 6):
    print("Python >= 3.6 required")
    sys.exit(-1)

long_description = open("README.md").read()
version = subprocess.getoutput("python3 ./risset.py --version")

setup(
    name = "risset",
    version = version,
    python_requires = ">=3.6",
    description = "A package manager for csound",
    author = "Eduardo Moguillansky",
    author_email = "eduardo.moguillansky@gmail.com",
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    py_modules=["risset"],
    install_requires = [
        "dataclasses"
    ],

    url="https://github.com/csound-plugins/risset",

    entry_points={
        "console_scripts": [
            "risset=risset:main",
        ]
    }

)
