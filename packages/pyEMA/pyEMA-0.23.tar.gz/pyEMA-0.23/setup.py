#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
from setuptools import setup

regexp = re.compile(r'.*__version__ = [\'\"](.*?)[\'\"]', re.S)

base_path = os.path.dirname(__file__)

init_file = os.path.join(base_path, 'pyEMA', '__init__.py')
with open(init_file, 'r') as f:
    module_content = f.read()

    match = regexp.match(module_content)
    if match:
        version = match.group(1)
    else:
        raise RuntimeError(
            'Cannot find __version__ in {}'.format(init_file))


def parse_requirements(filename):
    ''' Load requirements from a pip requirements file '''
    with open(filename, 'r') as fd:
        lines = []
        for line in fd:
            line.strip()
            if line and not line.startswith("#"):
                lines.append(line)
    return lines

requirements = parse_requirements('requirements.txt')

# Read the "README.rst" for project description
with open('README.rst', 'r') as f:
    readme = f.read()

setup(name='pyEMA',
      version=version,
      author='Klemen Zaletelj, Tomaž Bregar, Domen Gorjup, Janko Slavič',
      author_email='janko.slavic@fs.uni-lj.si, ladisk@gmail.com',
      description='Experimental and operational modal analysis.',
      url='https://github.com/ladisk/pyEMA',
      packages=['pyEMA'],
      long_description=readme,
      install_requires=requirements
      )