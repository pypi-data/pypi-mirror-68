#!/usr/bin/env python
from setuptools import setup, find_packages
from flower import __version__


def get_requirements(filename):
    return open('requirements/' + filename).read().splitlines()


classes = """
    Development Status :: 4 - Beta
    Intended Audience :: Developers
    License :: OSI Approved :: BSD License
    Topic :: System :: Distributed Computing
    Programming Language :: Python
    Programming Language :: Python :: 3
    Programming Language :: Python :: 3.3
    Programming Language :: Python :: 3.4
    Programming Language :: Python :: 3.5
    Programming Language :: Python :: 3.6
    Programming Language :: Python :: 3.7
    Programming Language :: Python :: Implementation :: CPython
    Programming Language :: Python :: Implementation :: PyPy
    Operating System :: OS Independent
"""
classifiers = [s.strip() for s in classes.split('\n') if s]


setup(
    name='flowest',
    version=__version__,
    description='Celery Flower',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Mher Movsisyan',
    author_email='mher.movsisyan@gmail.com',
    url='https://github.com/mher/flower',
    license='BSD',
    classifiers=classifiers,
    packages=find_packages(exclude=['tests', 'tests.*']),
    install_requires=get_requirements('default.txt'),
    test_suite="tests",
    tests_require=get_requirements('test.txt'),
    package_data={'flower': ['templates/*', 'static/*.*',
                             'static/**/*.*', 'static/**/**/*.*']},
    entry_points={
        'console_scripts': [
            'flower = flower.__main__:main',
        ],
        'celery.commands': [
            'flower = flower.command:FlowerCommand',
        ],
    },
)
