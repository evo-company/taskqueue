from setuptools import setup, find_packages

setup(
    name='taskqueue-client',
    version='0.1.2',
    description='TaskQueue client',
    author='Vladimir Magamedov',
    author_email='vladimir@magamedov.com',
    packages=find_packages(),
    install_requires=[
        'taskqueue-protobuf>=0.1.2',
        'grpclib',
    ],
)
