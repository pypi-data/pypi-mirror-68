import io
import os
from setuptools import setup


def read(fname):
    with io.open(os.path.join(os.path.dirname(__file__), fname), encoding='utf8') as f:
        return f.read()


setup(
    name="diplomat",
    version="0.0.1",
    author="Veit Heller",
    author_email="veit.heller@port-zero.com",
    description="is the arbiter between shell scripts and commands.",
    license="Proprietary",
    keywords="odin ansible orchestration",
    packages=["diplomat"],
    url="https://gitlab.service.wobcom.de/infrastructure/diplomat",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    classifiers=["Development Status :: 3 - Alpha", "Topic :: Utilities"],
    install_requires=[],
)
