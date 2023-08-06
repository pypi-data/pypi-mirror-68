# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT license.

from setuptools import setup, Distribution, find_packages
from os import path

class BinaryDistribution(Distribution):
    def has_ext_modules(foo):
        return False

curr_version = open('encrypted/inference/internal/_version.py').readlines()[-1].split()[-1].strip('\'"')
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
      name = 'encrypted-inference',
      version = curr_version,
      description = 'SDK for calling/providing an encrypted inference service',
      long_description = long_description,
      long_description_content_type = 'text/markdown',
      author='Microsoft Research',
      author_email = 'sealcrypto@microsoft.com',
      url = 'https://sealcrypto.org',
      license = 'MIT',
      packages = [
           'encrypted.inference.eiclient',
           'encrypted.inference.eibase',
           'encrypted.inference.eiserver',
           'encrypted.inference.internal'
      ],
      package_data = {
          'encrypted.inference.internal': [ 'parameters.json' ]
      },
      classifiers = [
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: POSIX :: Linux",
          "Operating System :: Microsoft :: Windows"
      ],
      install_requires = [
          "numpy"
      ],
      distclass = BinaryDistribution)
