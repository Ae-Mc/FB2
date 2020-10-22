import setuptools
from os import system
from shutil import rmtree
from sys import argv, exit
from typing import Dict, Any


with open("./README.md") as readmeFile:
    readme = readmeFile.read()

with open("./FB2/__version__.py") as aboutFile:
    about: Dict[str, Any] = {}
    exec(aboutFile.read(), about)

# 'setup.py publish' shortcut.
if argv[-1] == 'publish':
    try:
        rmtree("dist")
    except Exception:
        pass
    system('python setup.py sdist bdist_wheel')
    system('twine upload --repository pypi dist/*')
    exit()

requires = open("requirements.txt", 'r').read().split("\n")

setuptools.setup(name=about["__title__"],
                 version=about["__version__"],
                 author=about["__author__"],
                 author_email=about["__author_email__"],
                 description=about["__description__"],
                 long_description=readme,
                 long_description_content_type="text/markdown",
                 url=about["__url__"],
                 packages=setuptools.find_packages(),
                 classifiers=about["__classifiers__"],
                 python_requires='>=3.5',
                 install_requires=requires)
