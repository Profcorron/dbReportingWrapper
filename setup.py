import os
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

from distutils.core import setup

setup(
    name = 'dbreportingwrapper',
    packages = ['dbreportingwrapper'],
    version = '1.0.0',
    description = 'Database Reporting Wrapper',
    author='A Guinane, B Croker',
    url='https://github.com/aguin/dbreportingwrapper',
    license='MIT',
    classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.0',
            'Programming Language :: Python :: 3.1',
            'Programming Language :: Python :: 3.2',
            'Programming Language :: Python :: 3.3',
            'License :: OSI Approved :: GNU General Public License (GPL)',
            'Operating System :: OS Independent',
            'Topic :: Scientific/Engineering :: GIS',
            'Topic :: Software Development :: Libraries :: Python Modules'
          ],
    long_description="""
Database Reporting Wrapper
A package to simplify reporting with queries.
"""

)