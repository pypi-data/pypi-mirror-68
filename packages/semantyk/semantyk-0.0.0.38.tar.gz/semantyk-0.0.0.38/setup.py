from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = "semantyk",
    version = "0.0.0.38",
    author = "Daniel Bakas Amuchastegui",
    maintainer = "Semantyk Team",
    description = "Ideas Wonder.",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/semantykcom/Semantyk",
    packages = find_packages(
        exclude = [
            'docs',
            'tests*'
        ]
    ),
    classifiers = [
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3"
    ],
    install_requires = [
        'rdflib'
    ],
    python_requires = '>=3.6',
    keywords = 'semantyk'
)