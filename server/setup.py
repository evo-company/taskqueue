from setuptools import setup, find_packages

setup(
    name='taskqueue-server',
    version='0.1.0',
    description='TaskQueue server',
    author='Vladimir Magamedov',
    author_email='vladimir@magamedov.com',
    packages=find_packages(),
    install_requires=[
        'taskqueue-protobuf>=0.1.2',
        'click',
        'strictconf>=0.3.0rc2',
        'metricslog>=0.1.3',
        'pyyaml',
        'grpclib>=0.3.0',
        'aiokafka',
    ],
)
