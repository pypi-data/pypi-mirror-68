# This Python file uses the following encoding: utf-8
from setuptools import setup, find_packages

setup(  name='rmodel',
        packages=find_packages(),
        version='0.0.1',
        description='rmodel: simple statistical models that follow R-like naming conventions',
        long_description='The point of this project is to set up a standardized UI for the statistical models one can use. The conventions are inspired by how it is handles in R. But, this is Python, so it must be way better, right?',
        author='MatteoLacki',
        author_email='matteo.lacki@gmail.com',
        url='https://github.com/MatteoLacki/rmodel.git',
        keywords=['R', 'models', 'R feel but Python structures'],
        classifiers=['Development Status :: 1 - Planning',
                     'License :: OSI Approved :: BSD License',
                     'Intended Audience :: Science/Research',
                     'Topic :: Scientific/Engineering :: Chemistry',
                     'Programming Language :: Python :: 3.6',
                     'Programming Language :: Python :: 3.7',
                     'Programming Language :: Python :: 3.8'],
        install_requires=['numpy'])
