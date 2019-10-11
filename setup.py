from distutils.core import setup
from setuptools import find_packages

setup(
    name='parametric',
    version='0.1',
    description='Parameter framework for simulations and experiments',
    author='Robert Fasano',
    author_email='robert.j.fasano@colorado.edu',
    packages=find_packages(exclude=['docs']),
    license='MIT',
    long_description=open('README.md').read(),
    install_requires=['numpy', 'visa', 'zmq']
)
