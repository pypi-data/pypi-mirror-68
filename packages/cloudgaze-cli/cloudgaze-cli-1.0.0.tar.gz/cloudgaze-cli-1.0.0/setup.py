from setuptools import setup, find_packages
import pathlib


README = (pathlib.Path(__file__).parent/"README.md").read_text()


setup(
    name="cloudgaze-cli",
    version="1.0.0",
    description="Convert CloudFormation templates to draw.io compatible diagrams, with dependency arrows",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/cloudgaze/cloudgaze-cli",
    author="hawry",
    author_email="hawry@hawry.net",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Topic :: Software Development",
        "Topic :: Software Development :: Documentation"
    ],
    packages=find_packages(),
    install_requires=[
        "click>=7.0"
    ],
    tests_require=[
        "tox>=3.13.0"
    ],
    entry_points={
        "console_scripts": [
            "cloudgaze=cloudgaze_cli.__main__:cli"
        ]
    }
)