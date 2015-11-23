#!/usr/bin/env python
from setuptools import find_packages, setup

# Use latest_tweets.VERSION for version numbers
version_tuple = __import__('latest_tweets').VERSION
version = '.'.join([str(v) for v in version_tuple])

setup(
    name='django-latest-tweets',
    version=version,
    description='Latest Tweets for Django',
    long_description=open('README.rst').read(),
    url='https://github.com/blancltd/django-latest-tweets',
    maintainer='Blanc Ltd',
    maintainer_email='studio@blanc.ltd.uk',
    platforms=['any'],
    install_requires=[
        'twitter>=1.9.1',
    ],
    packages=find_packages(),
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    license='BSD',
)
