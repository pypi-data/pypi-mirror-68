#!/usr/bin/env python
# coding: utf-8

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python-pangu", # Replace with your own username
    version="0.0.7",
    author="championchangpeng",
    author_email="championchangpeng@gmail.com",
    description="ai adapter client for python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/GokGok_group/python-pangu",
    packages=[
        'python_pangu',
        'python_pangu.pangu_base_aio',
        'python_pangu.gateway_base_aio'
    ],
    install_requires=[
        'pyzmq',
        'msgpack-python',
        'psutil'
    ],
    keywords=['python pangu',  'RPC', 'Remote Procedure Call', 'Event Driven',
              'Asynchronous', 'Non-Blocking',
              'Raspberry Pi', 'ZeroMQ', 'MessagePack', 'Arduino'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Other Environment',
        'Intended Audience :: Education',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Education',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: System :: Hardware'
    ]
)
