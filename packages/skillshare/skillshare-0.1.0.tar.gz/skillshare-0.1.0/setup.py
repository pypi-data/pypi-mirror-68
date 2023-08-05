import re

from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines() or []

with open('README.md') as f:
    readme = f.read() or ''

version = ''
with open('skillshare/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Version is not set!')

setup(
    name='skillshare',
    version=version,
    description='Async library to download Skillshare Courses',
    author='Technofab',
    author_email='skillshare.git@technofab.de',
    url='https://gitlab.com/TECHNOFAB/skillshare',
    license='MIT',
    packages=find_packages(),
    long_description=readme,
    long_description_content_type="text/markdown",
    install_requires=requirements,
    python_requires='>=3.5',
)
