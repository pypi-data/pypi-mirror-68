# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 16:17:00 2017

@author: Yoel Cortes-Pena
"""
from setuptools import setup
#from Cython.Build import cythonize
#import numpy

setup(
    name='pipeml',
    packages=['pipeml'],
    license='MIT',
    version='0.1',
    description='Pipeline tools for machine learning models',
    long_description=open('README.rst').read(),
    author='Yoel Cortes-Pena',
    install_requires=['sklearn', 'numpy'],
    python_requires=">=3.6",
    package_data=
        {'pipeml': []},
    platforms=['Windows', 'Mac', 'Linux'],
    author_email='yoelcortes@gmail.com',
    url='https://github.com/yoelcortes/pipeml',
    download_url='https://github.com/yoelcortes/pipeml.git',
    classifiers=['Development Status :: 3 - Alpha',
                 'Environment :: Console',
                 'License :: OSI Approved :: MIT License',
                 'Programming Language :: Python :: 3.6',
				 'Programming Language :: Python :: 3.7',
                 'Topic :: Scientific/Engineering'],
    keywords='machine learning tools function pipeline',
)