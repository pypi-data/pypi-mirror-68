#!/usr/bin/env python3
import os
from setuptools import setup, find_packages

def convert_markdown_images(raw_markdown, github_repo):
    """Convert images in a string of raw markdown to display on PyPI."""
    github_raw_content_baseurl = 'https://raw.githubusercontent.com'
    repo_raw_content = f'{github_raw_content_baseurl}/{github_repo}/master/'
    markdown = raw_markdown.replace('src=', f'src={repo_raw_content}')

raw_long_description = open('README.md').read()
long_description = convert_markdown_images(raw_long_description, 'monopyly')

setup(
    name='monopyly',
    version='1.0.2',
    description='A homemade personal finance manager.',
    author='Mitch Negus',
    author_email='mitchnegus57@gmail.com',
    license='GNU GPLv3',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/mitchnegus/monopyly',
    download_url='https://pypi.org/project/monopyly',
    packages=find_packages(),
    include_package_data=True,
    scripts=['scripts/monopyly', 'scripts/backup_db.py'],
    python_requires='>=3.7',
    install_requires=[
        'flask',
        'flask-wtf',
        'python-dateutil'
    ]
)
