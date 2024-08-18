from setuptools import setup, find_packages

version = "0.0.1"

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

setup(
    name="back-me-up",
    version=version,
    description="A Command Line Utility for backing up files and directories on a server or a PC.",
    long_description=readme,
    long_description_content_type='text/markdown',
    author="Aseem Savio",
    author_email="aseemsavio3@gmail.com",
    url="https://github.com/aseemsavio/back-me-up/blob/master/README.md",
    license="MIT",
    keywords="cli, server, backup, archive",
    packages=find_packages(exclude=["tests", "tests.*"]),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'typer[all]>=0.12.4',
        'rich>=13.7.1',
        'keyring>=25.3.0'
    ],
    entry_points={
        'console_scripts': [
            'backmeup=backmeup.backmeup:cli',
        ],
    },
)
