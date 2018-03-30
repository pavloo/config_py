from setuptools import setup

setup(name='config_py',
      description='A Python package for managing configuration files in your apps',
      long_description='A package for managing configuration files in your apps ' +
        'depending on environment (development, test, production), and using Convention ' +
        'Over Configuration principle.',
      version='0.1',
      url='https://github.com/pavloo/config_py',
      author='Pavlo Osadchyi',
      author_email='posadchiy@gmail.com',
      license='MIT',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Python Developers',
          'License :: MIT',
          'Programming Language :: Python :: 3'
      ],
      packages=[
          'config_py',
          'config_py.bin',
          'config_py.lib',
          'config_py.fixtures.module',
          'config_py.fixtures.root',
      ],
      include_package_data=True,
      install_requires=[
          'click>=6.7'
      ],
      entry_points={
          'console_scripts': [
              'configpy=config_py.bin.config_py:config_py'
          ]
      }
)
