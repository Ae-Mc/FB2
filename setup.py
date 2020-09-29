import setuptools
from os import system
from shutil import rmtree
from sys import argv, exit


with open("./README.md") as readmeFile:
    readme = readmeFile.read()

with open("./FB2/__version__.py") as aboutFile:
    about = {}
    exec(aboutFile.read(), about)

# 'setup.py publish' shortcut.
if argv[-1] == 'publish':
    try:
        rmtree("dist")
    except Exception:
        pass
    system('python setup.py sdist bdist_wheel')
    system('twine upload --repository FB2 dist/*')
    exit()

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
                 python_requires='>=3.5')
