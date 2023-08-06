#!/usr/bin/env python3


import os
from setuptools import find_packages, setup, Command


class CleanCommand(Command):
    """Custom clean command to tidy up the project root."""
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    @staticmethod
    def run():
        os.system('rm -vrf ./build ./dist ./*.pyc ./*.egg-info')


setup(name='gtl-ville',
      version='2.0.96',
      description='GTL Ville common packages',
      url='https://gitlab.inria.fr/gtl-ville/gv-common',
      author='Vadim BERTRAND',
      author_email='vadim.bertrand@gipsa-lab.fr',
      license='MIT',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Topic :: Software Development',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3 :: Only',
      ],
      packages=find_packages(),
      install_requires=[
          'aiofiles',
          'asyncpg',
          'bitstring',
          'fiona',
          'grpcio-tools',
          'grpclib>=0.2.2rc2',
          'protobuf',
          'pytz',
          'shapely',
          'ujson'
      ],
      python_requires='>=3.7',
      )
