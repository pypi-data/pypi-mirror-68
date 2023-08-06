#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()


requirements = ['cffi', 'numpy', 'matplotlib']
setup_requirements = ['pytest-runner', ]
test_requirements = ['pytest']


setup(
    author='',
    author_email='',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Python tools to interact with darshan log records of HPC applications.",
    install_requires=requirements,
    long_description=readme,
    include_package_data=True,
    keywords='darshan',
    name='darshan',
    packages=find_packages(include=['darshan']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='',
    version='0.0.1',
    zip_safe=False,
)
