#!/usr/bin/env python

from setuptools import setup
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='blender_addon_tester',
      version='0.9.2',
      description='Add-On Tester for Blender using Pytest',
      author='Dave Keeshan',
      author_email='dave.keeshan@daxzio.com',
      url='https://github.com/nangtani/blender-addon-tester',
      packages=['blender_addon_tester'],
      license = 'MIT',
      install_requires=['bs4', 'requests', 'flake8', 'dmglib'],
      long_description=read('README.md'),
      long_description_content_type='text/markdown',
      python_requires='>=3.7',
      include_package_data=True, # Make us of MANIFEST.in including extra files
      classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Artistic Software",
        "License :: OSI Approved :: MIT License"
      ]
     )
