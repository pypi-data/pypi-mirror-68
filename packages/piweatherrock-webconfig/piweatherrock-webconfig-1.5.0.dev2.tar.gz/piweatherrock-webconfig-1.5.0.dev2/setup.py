"""Module setup."""

import runpy
from setuptools import setup, find_namespace_packages

PACKAGE_NAME = "piweatherrock-webconfig"
version_meta = runpy.run_path("./version.py")
VERSION = version_meta["__version__"]


with open("README.md", "r") as fh:
    long_description = fh.read()


def parse_requirements(filename):
    """Load requirements from a pip requirements file."""
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


if __name__ == "__main__":
    setup(
        name=PACKAGE_NAME,
        author="Gene Liverman",
        author_email="gene@technicalissues.us",
        version=VERSION,
        packages=find_namespace_packages(include=['piweatherrock.*']),
        include_package_data=True,
        install_requires=parse_requirements("requirements.txt"),
        python_requires=">=3.6",
        scripts=["scripts/pwr-webconfig"],
        description="Provides a web interface for configuring PiWeatherRock",
        long_description=long_description,
        long_description_content_type="text/markdown",
        license='MIT',
        url='https://github.com/genebean/piweatherrock-webconfig',
        classifiers=[
            'License :: OSI Approved :: MIT License',
        ],
    )
