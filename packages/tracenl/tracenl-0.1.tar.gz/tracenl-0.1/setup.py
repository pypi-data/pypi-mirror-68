from setuptools import setup

from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


setup(
    name="tracenl",
    version="0.1",
    author="Mike Spindel",
    author_email="mike@spindel.is",
    description="Easily snoop on netlink messages with ptrace",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://github.com/deactivated/python-nltrace",
    keywords="netlink capture trace",
    license="MIT",
    packages=["tracenl"],
    install_requires=["pyroute2", "python-ptrace"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux"
    ],
    python_requires='>=3.6',
    entry_points={"console_scripts": ["tracenl=tracenl.__main__:main"]},
)
