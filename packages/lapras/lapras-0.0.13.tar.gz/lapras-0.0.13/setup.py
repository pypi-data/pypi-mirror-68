#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from setuptools import setup, find_packages

filepath = 'README.md'

setup(
    name='lapras',
    version='0.0.13',
    packages = find_packages(),

    description='scorecard',
    long_description=open(filepath).read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yhangang',
    author='Badtom',
    author_email='yhangang@gmail.com',
    license='MIT',
    python_requires = '>=3.5',
    install_requires = [
        'numpy >= 1.15.4',
        'pandas',
        'scipy',
        'scikit-learn',
        'seaborn >= 0.10.0',
    ],
    classifiers=[
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        # '': ['*.txt', '*.rst', '*.csv'],
        # include any *.msg files found in the 'test' package, too:
        # 'data': ['*.csv'],
    },
    # data_files=[('DealConfig.py'),('performance.py')],

    keywords=['scorecard'],
    entry_points={

    },
    data_files=[filepath]
)