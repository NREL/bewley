
#!/usr/bin/env python
import io
import os
import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


# Read the version from the __init__.py file without importing it
def read(*names, **kwargs):
    with io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")
    ) as fp:
        return fp.read()

def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

setup(name='bewley',
      version=find_version("bewley", "__init__.py"),
      description='A package for visualizing Bewley lattice diagrams',
      author='Monte Lunacek',
      author_email='monte.lunacek@nrel.gov',
      url='https://github.com/nrel/bewley',
      packages=['bewley'],
      install_requires=['matplotlib'],
      package_data={'bewley': []},
     )
