# -*- coding: utf-8 -*-


"""setup.py: setuptools control."""


import setuptools


version = '0.1.0'

REQUIRES = [
    "base58==1.0.3",
    "base58check==1.0.2",
    "eth-utils==1.7.0",
    "pycrypto==2.6.1",
    "pycryptodome==3.9.0",
    "two1",
]

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="new_hd_tools",
    packages=setuptools.find_packages(),
    version=version,
    install_requires=REQUIRES,
    description="HD wallet Tools.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="pschy",
    author_email="cj82@qq.com",
    url="https://github.com/pschy/new_hd_tools",
)
