#!/usr/bin/env python
# encoding: utf-8

from setuptools import setup, find_packages
import io


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


with open('requirements.txt') as f:
    required = f.read().splitlines()
install_requires = [r for r in required if r and r[0] != '#' and not r.startswith('git')]

long_description = read('README.txt')


setup(
    name='pyixnetwork',
    version='3.0.2',
    url='https://github.com/shmir/PyIxNetwork/',
    license='Apache Software License',
    author='Yoram Shamir',
    install_requires=install_requires,
    tests_require=['pytest'],
    author_email='yoram@ignissoft.com',
    description='Python OO API package to automate Ixia IxNetwork traffic generator',
    long_description=long_description,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    platforms='any',
    test_suite='tests',
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 5 - Production/Stable',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Testing :: Traffic Generation',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'],
    keywords='ixnetwork l2l3 test tool ixia automation',
)
