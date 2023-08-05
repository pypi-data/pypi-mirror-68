# encoding: utf-8

from setuptools import setup, find_packages, Command
import sys
import os
import re
import ast

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

setup(
    name='lurl',
    version='0.1.2',
    description='cURL please....',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Fernanda Panca Prima',
    author_email='pancaprima8@gmail.com',
    url='',
    license='MIT',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        "requests",
        "puncurl",
        "Naked",
        "inquirer"
    ],
    entry_points={
        'console_scripts': [
            'lurl = lurl.main:main',
        ]
    },
    include_package_data=True,
    python_requires='>=3.6'
)