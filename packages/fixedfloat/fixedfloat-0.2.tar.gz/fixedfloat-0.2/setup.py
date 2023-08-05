#!/usr/bin/env python

import sys
from setuptools import setup

if sys.version_info < (3, 6):
    requires = ['requests']
else:
    requires = ['requests', 'aiohttp']

setup(
    name='fixedfloat',
    version='0.2',
    description='FixedFloat API wrapper',
    long_description='The FixedFloat API allows you to automate the receipt of information about the exchange rates of currencies, created orders, presented on the FixedFloat service, create orders and manage them using it.',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Office/Business :: Financial',
    ],
    keywords='fixedfloat api exchange crypto',
    url='http://github.com/fixedfloat/api-python',
    author='Leon Todd',
    author_email='leontodd@protonmail.com',
    license='MIT',
    packages=['fixedfloat'],
    install_requires=requires
)
