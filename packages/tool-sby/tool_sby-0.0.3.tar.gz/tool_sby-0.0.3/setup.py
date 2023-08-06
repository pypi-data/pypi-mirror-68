import codecs
import os

try:
    from setuptools import setup
except:
    from distutils.core import setup


def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()


platforms = ['linux/Windows']
classifiers = [
    'Development Status :: 3',
    'Topic :: Text Processing',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.7',
]

install_requires = [
    # 'numpy>=1.11.1',
    # 'pandas>=0.19.0'
    # 'sxtwl>=1.0.7',
    # 'requests>=2.22.0',
    # 'python-dateutil>=2.8.0',
    # 'arrow>=0.13.1',
    # 'regex>=2020.2.20',
    # 'pypinyin>=0.36.0'
]

setup(name='tool_sby',
      version='0.0.3',
      description='A test module for caozhi',
      long_description='',
      packages=['tool_sby', 'tool_sby.pipelines'],
      include_package_data=True,
      author="caozhi",
      author_email="hjp46193816@163.com",
      url="https://benyo.github.io",
      license="Apache License, Version 2.0",
      platforms=platforms,
      install_requires=install_requires,
      zip_safe=False
      )
