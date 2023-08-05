import os.path
from setuptools import setup

HERE = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

setup(
    name="xindi-lib",
    version="0.1.0",
    description="library to manage ip subnets",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/wolfbo/xindi-lib",
    author="Wolfgang Wangerin",
    author_email="wolfgang.wangerin@budohh.de",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    packages=["xindi-lib"],
    include_package_data=True,
    install_requires=["ipaddress"],
)
