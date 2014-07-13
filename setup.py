# -*- coding: utf-8 -*-
# vim: set fileencodings=utf-8

import os
from setuptools import setup, find_packages


setup(
    name='discogs-client',
    version='1.1.1',
    description='Official Python API client for Discogs',
    url='https://github.com/discogs/discogs-python-client',
    author='Discogs',
    author_email='info@discogs.com',
    keywords='discogs api music',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    platforms=['any'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Communications',
        'Topic :: Utilities',
        ],
    install_requires=[
        'requests',
        'urllib3',
    ],
    extras_require=dict(
        test=[
            'zope.testing',
            'WebTest',
        ],
    ),
)
