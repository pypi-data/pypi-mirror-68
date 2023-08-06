from setuptools import setup, find_packages

with open("requirements.txt", 'r') as file:
    requirements = file.readlines()

setup(
    name='PyNeutralNews',
    version='0.9.1',
    packages=find_packages(),
    install_requires=requirements,
    license='copyright: Neutral News',
    author='Jonas Bouaziz',
    description='Neutral News client for api communication https://neutralnews.fr'
)
