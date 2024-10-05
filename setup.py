# (c) KiryxaTech, 2024. Apache License 2.0

from io import open
from setuptools import setup


version = "0.1.1"


with open('README.md', encoding='utf-8') as f:
    long_discription = f.read()


setup(
    name='ooj',
    version=version,

    author='KiryxaTech',
    author_email='kiryxatech@gmail.com',

    description=(
        u'Object-Oriented JSON (OOJ) is a universal library'
        u'for working with JSON in Python, providing simplicity'
        u'and convenience in serializing and deserializing'
        u'complex objects.'
    ),
    long_description=long_discription,
    long_description_content_type='text/markdown',

    url='https://github.com/KiryxaTechDev/ooj',
    download_url=f'https://github.com/KiryxaTechDev/ooj/archive/refs/tags/{version}.zip',

    packages=[
        'ooj',
        'ooj.exceptions'
    ],
    install_requires=[
        'jsonschema>=4.0.0',
        'requests==2.32.3'
    ],
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12'
    ]
)