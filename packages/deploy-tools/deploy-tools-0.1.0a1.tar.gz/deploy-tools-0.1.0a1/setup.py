# -*- coding: utf-8 -*-
import sys

from setuptools import find_packages, setup

setup(
    name='deploy-tools',
    version='0.1.0a1',
    description='A deploy tools',
    url='https://github.com/view868/deploy_tools',
    maintainer='view',
    maintainer_email='view868@gmail.com',
    include_package_data=True,
    packages=find_packages(exclude=['tests.py', 'fabfile.py'], include=['tasks.py']),
    install_requires=[
        'Fabric3',
        'PyYAML'
    ],
    platforms=['Any'],
    keywords=['deploy', 'git'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ]
)
