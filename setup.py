from os import path
from setuptools import setup
import version


long_description = """
    A package for managing configuration files in Python applications
    depending on environment (development, test, production), using Convention
    Over Configuration principle.
"""

setup(name='config-py',
      description='A Python package for managing configuration files in your apps',
      long_description=long_description,
      version=version.__version__,
      url='https://github.com/pavloo/config_py',
      author='Pavlo Osadchyi',
      author_email='posadchiy@gmail.com',
      license='MIT',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3'
      ],
      packages=[
          'config_py',
          'config_py.bin',
          'config_py.lib',
          'config_py.fixtures',
          'version'
      ],
      include_package_data=True,
      install_requires=[
          'click>=6.7'
      ],
      entry_points={
          'console_scripts': [
              'config_py=config_py.bin.config_py:config_py'
          ]
      }
)
