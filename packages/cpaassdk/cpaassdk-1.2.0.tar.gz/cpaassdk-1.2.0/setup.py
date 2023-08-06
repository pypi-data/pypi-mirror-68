#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages
import os

requirements = [ 'requests>=2.22', 'PyJWT>=1.7.1', 'pyhumps' ]

current_dir = os.path.abspath(os.path.dirname(__file__))
about = {}
with open(os.path.join(current_dir, "cpaassdk", "__version__.py"), "r") as f:
    exec(f.read(), about)

setup(
    author="KeepWorks",
    author_email='kandy@keepworks.com',
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Python SDK to build robust real-time communication applications.",
    install_requires=requirements,
    license="SEE LICENSE IN LICENSE FILE",
    include_package_data=True,
    keywords='cpaassdk',
    name='cpaassdk',
    url='https://github.com/Kandy-IO/kandy-cpaas-python-sdk',
    packages=find_packages(include=['cpaassdk', 'cpaassdk.resources']),
    version=about['__version__'],
    zip_safe=False
)
