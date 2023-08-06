from os import path
from setuptools import setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='Discogs-APY',
    version='1.0',
    packages=['Discogs-APY'],
    url='https://github.com/wiperandtrue/Discogs-APY',
    license='MIT Licence',
    author='Josh Taylor',
    author_email='joshvvtaylor@gmail.com',
    description='A lightweight Python wrapper for the Discogs database API.',
    long_description=long_description,
    long_description_content_type='text/markdown'
)
