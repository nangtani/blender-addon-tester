#!/usr/bin/env python

from setuptools import setup
from blender_addon_tester.version import __version__
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='blender_addon_tester',
      version=__version__,
      description='Add-On Tester for Blender using Pytest',
      author='Dave Keeshan',
      author_email='dave.keeshan@daxzio.com',
      url='https://github.com/nangtani/blender-addon-tester',
      packages=['blender_addon_tester'],
      license = 'MIT',
      install_requires=['bs4', 'requests', 'flake8', 'dmglib', 'exceptiongroup', 'iniconfig'],
      long_description=read('README.md'),
      long_description_content_type='text/markdown',
      python_requires='>=3.7',
      include_package_data=True, # Make us of MANIFEST.in including extra files
      classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Artistic Software",
        "License :: OSI Approved :: MIT License"
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3 :: Only',
      ]
     )
