from setuptools import setup, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="AS-Object_models",
    version="0.1",
    description="A Project that captures all of the data manipulation used in apps developed by Analytics Supply LLC.",
    url="https://gitlab.com/AnalyticsSupply/as-object-models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Jason Bowles",
    author_email="jasonbowles@analyticssupply.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python"
    ],
    python_requires=">=3.7",
    packages=find_packages(),
    install_requires=["docutils>=0.3","pandas>=1.0.3","jmespath>=0.9.3","python-dateutil>=2.8.1","google-cloud-firestore>=1.6.2","google-cloud-storage>=1.26.0"],
)