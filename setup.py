#!/usr/bin/env python

from setuptools import setup

setup(
        name='pathtags',
        version='0.9.2',
        description='File tagging system that uses the filesystem for storage.',
        author='Jeremy Cantrell',
        author_email='jmcantrell@gmail.com',
        classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Intended Audience :: End Users/Desktop',
            'License :: OSI Approved :: BSD License',
            'Natural Language :: English',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            ],
        install_requires=[
            'PathUtils',
            'ScriptUtils',
            ],
        entry_points={
            'console_scripts': [
                'pathtags=pathtags:main',
                ]
            },
        py_modules=[
            'pathtags',
            ],
        )
