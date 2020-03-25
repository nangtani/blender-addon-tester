#!/usr/bin/env python

from setuptools import setup
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='blender_addon_tester',
      version='0.1',
      description='Add-On Tester for Blender using Pytest',
      author='Douglas Kastle',
      author_email='todo@todo.net',
      url='https://github.com/douglaskastle/blender-fake-addon',
      packages=['blender_addon_tester'],
      license = 'MIT',
      install_requires=['bs4','pytest','requests','pip', 'coverage', 'pytest-cov', 'dmglib'],
      long_description=read('README.md'),
      python_requires='>=3',
      include_package_data=True, # Make us of MANIFEST.in including extra files
      classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Artistic Software",
        "License :: OSI Approved :: MIT License"
      ]
     )
