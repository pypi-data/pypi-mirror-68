#!/usr/bin/env python3.7

from pathlib import Path

# Non-standard library python package imports
from setuptools import (  # type: ignore
    find_packages,
    setup,
)

# Internal module package imports
from blackjack import version

setup(
    # Metadata
    name='x10-blackjack',
    version=version,
    author_email='x10an14@gmail.com',
    description='A small blackjack game.',
    long_description=Path('README.md').read_text(),
    long_description_content_type='text/markdown',
    url='https://gitlab.com/x10an14/blackjack',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Operating System :: OS Independent',
        'Topic :: Games/Entertainment',
        'Topic :: Software Development',
    ],

    # Package data
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
    ],
    entry_points='''
        [console_scripts]
        blackjack=blackjack.cli:main
    ''',
    python_requires='>=3.7'
)
