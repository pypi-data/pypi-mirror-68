try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

long_desc = '''Simple PyTorch utils, yet another package.
This one is mostly for my personal applications.'''

# rm -rf dist build && python3 setup.py sdist bdist_wheel
# twine upload dist/*
setup(
    name='sorch',
    version='0.2.5',
    packages=['sorch', 'sorch.trainer'],
    url='https://github.com/PiotrDabkowski/sorch',
    license='MIT',
    author='Piotr Dabkowski',
    author_email='piodrus@gmail.com',
    description='Simple PyTorch utils, yet another package :)',
    long_description=long_desc)
