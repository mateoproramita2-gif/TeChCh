#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name="techch",
    version="2.0.0",
    description="TeChCh - Terminal Enhanced Cyber Command Hub",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="TeChCh Security Team",
    author_email="techch@security.local",
    url="https://github.com/techch/techch",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "colorama>=0.4.0",
        "requests>=2.28.0",
    ],
    entry_points={
        "console_scripts": [
            "techch=techch:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Topic :: Security",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
    ],
)
