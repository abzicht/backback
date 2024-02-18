import os
import sys
from setuptools import find_packages, setup
from pathlib import Path

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 6)

# This check and everything above must remain compatible with Python 2.7.
if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write("""
==========================
Unsupported Python version
==========================
This version of backback requires Python {}.{}, but you're trying to
install it on Python {}.{}.
""".format(*(REQUIRED_PYTHON + CURRENT_PYTHON)))
    sys.exit(1)

def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()

home = str(Path.home())

setup(
    name='backback',
    version="1.0.2",
    python_requires='>={}.{}'.format(*REQUIRED_PYTHON),
    author='Abzicht',
    author_email='abzicht@gmail.com',
    description=('A tool for quickly running all sorts of backups'),
    long_description=read('README.md'),
    license='apache2',
    include_package_data=True,
    packages=find_packages(),
    entry_points={'console_scripts': [
       'backback = backback.script:main',
    ]},
    data_files=[
        (os.path.join(home, '.backback/'), ['backback/data/config.yml']),
    ],
    install_requires=['prompt_toolkit'],
)
