#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['beautifulsoup4', 'arrow', 'requests', ]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    author="Nick Hobart",
    author_email='nick@hobart.io',
    entry_points={
        'console_scripts': [
            'tmrwppk = tmrwppk.tmrwppk:main',
            ],
        },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Tomorrow's Prices Today",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='tmrwppk',
    name='tmrwppk',
    packages=find_packages(include=['tmrwppk']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/hobakill/tmrwppk',
    version='0.0.7',
    zip_safe=False,
)
