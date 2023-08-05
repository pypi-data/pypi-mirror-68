from setuptools import setup, find_packages


VERSION = '0.0.6'

with open('requirements.txt') as f:
    install_requires = f.read().strip().split('\n')

setup(
    name='eisen-core',
    version=VERSION,
    description='Eisen is a collection of tools to train neural networks for medical image analysis',
    packages=find_packages(),
    install_requires=install_requires,
    entry_points={
        'console_scripts': [],
    },
)