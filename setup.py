from setuptools import setup, find_packages
import sys, os

VERSION = '0.1.1'

LONG = """
"""

setup(name='mojo',
    version=VERSION,
    description="A Web Frontend for Monkey Farm",
    long_description=LONG,
    classifiers=[], 
    keywords='django',
    author='Jeffrey Ness',
    author_email='',
    url='http://github.com/jness/monkeyfarmweb',
    license='',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    test_suite='nose.collector',
    install_requires=[
        "django>=1.3",
        ],
    setup_requires=[
        ],
    entry_points="""
    """,
    namespace_packages=[
        ],
    )
