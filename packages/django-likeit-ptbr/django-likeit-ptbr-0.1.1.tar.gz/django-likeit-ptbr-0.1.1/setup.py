#!/usr/bin/env python

from setuptools import setup, find_packages

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='django-likeit-ptbr',
    version='0.1.1',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/gustavodesc/django-likeit-ptbr',
    download_url='https://github.com/gustavodesc/django-likeit-ptbr/tarball/0.1',
    author='Gustavo Guella',
    author_email='gustavodesc@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        ],
    )
