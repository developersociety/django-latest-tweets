#!/usr/bin/env python
from distutils.core import setup

# Use latest_tweets.VERSION for version numbers
version_tuple = __import__('latest_tweets').VERSION
version = '.'.join([str(v) for v in version_tuple])

setup(
    name='django-latest-tweets',
    version=version,
    description='Latest Tweets for Django',
    long_description=open('README.rst').read(),
    url='https://github.com/blancltd/django-latest-tweets',
    maintainer='Alex Tomkins',
    maintainer_email='alex@blanc.ltd.uk',
    platforms=['any'],
    install_requires=[
        'twitter>=1.9.1',
    ],
    packages=[
        'latest_tweets',
        'latest_tweets.management',
        'latest_tweets.management.commands',
        'latest_tweets.templatetags',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    license='BSD-2',
)
