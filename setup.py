from setuptools import find_packages, setup

with open("requirements.txt") as f:
    requirements = f.read().splitlines()
    
setup(
    name="MLProject",
    version="0.0.1",
    description="A machine learning project",
    author="Prem",
    packages=find_packages(),
    install_requires=requirements,
)