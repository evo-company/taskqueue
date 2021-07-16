from setuptools import setup, find_packages

setup(
    name='taskqueue-protobuf',
    version='0.1.2',
    description='Protocol Buffers stub files for the TaskQueue service',
    author='Vladimir Magamedov',
    author_email='vladimir@magamedov.com',
    packages=find_packages(),
    install_requires=['protobuf'],
)
