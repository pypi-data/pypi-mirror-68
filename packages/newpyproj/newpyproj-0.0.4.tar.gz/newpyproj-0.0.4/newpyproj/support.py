#!/usr/bin/env python
# -*- coding: utf-8 -*-

projectfile_txt = """
import logging
from [[projectname]].support import text_content

def first_function():
    logging.info('Executing first function...')
    print('First function executed properly')
    return None

def second_function(argument: str) -> bool:
    logging.info('Executing second function...')
    logging.info('Verifying argument...')
    verification = isinstance(argument, str)
    if verification:
        print(f"{argument} successfully imported.")
    print('Second function executed properly')
    return verification

def main():
    first_function()
    second_function(text_content)


if __name__ == '__main__':
    main()
"""
gitignore_txt = """
# Template
# From: https://github.com/github/gitignore/
# 
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
.pybuilder/
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
#   For a library or package, you might want to ignore these files since the code is
#   intended to run in multiple environments; otherwise, check them in:
# .python-version

# pipenv
#   According to pypa/pipenv#598, it is recommended to include Pipfile.lock in version control.
#   However, in case of collaboration, if having platform-specific dependencies or dependencies
#   having no cross-platform support, pipenv may install dependencies that don't work, or not
#   install all needed dependencies.
#Pipfile.lock

# PEP 582; used by e.g. github.com/David-OConnor/pyflow
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype static type analyzer
.pytype/

# Cython debug symbols
cython_debug/"""
cli_txt = """
from [[projectname]] import cli

cli.start_cli()
"""
gui_txt = """
from [[projectname]] import gui

gui.start_gui()
"""
cli2_txt = """

def start_cli():
    print('Starting cli')
"""
gui2_txt = """

def start_gui():
    print('Starting gui')
"""
readme_txt = """
# [[projectname]]

This is the [[projectname]] package. You can use
[Github-flavored Markdown](https://guides.github.com/features/mastering-markdown/)
to write your content.

## Installation

## Usage

"""
license_txt = """
MIT License

Copyright (c) YEAR YOUR NAME

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
setup_txt = """
import setuptools

with open("README", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="[[projectname]]",
    version="0.0.1",
    author="Example Author",
    author_email="author@example.com",
    description="The [[projectname]] package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/example",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)"""
init_txt = """"""
support_txt = """\n\ntext_content = 'String variable in support module'"""
test_advanced_txt = """
import unittest
from [[projectname]] import [[projectname]]

class TestFunctions(unittest.TestCase):

    def test_first_function(self):
        self.assertEqual([[projectname]].first_function(), None)

    def test_second_function(self):
        self.assertTrue([[projectname]].second_function('Testing string'))


if __name__ == '__main__':
    unittest.main()"""
test_basic_txt = """
import unittest

class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()"""

shebang_txt = """#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

content_dict = {'projectfile': projectfile_txt,
                'gitignore': gitignore_txt,
                'cli': cli_txt,
                'gui': gui_txt,
                'cli2': cli2_txt,
                'gui2': gui2_txt,
                'readme': readme_txt,
                'license': license_txt,
                'setup': setup_txt,
                'init': init_txt,
                'support': support_txt,
                'test_advanced': test_advanced_txt,
                'test_basic': test_basic_txt,
                'shebang': shebang_txt}