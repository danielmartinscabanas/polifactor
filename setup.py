from setuptools import setup
import re

with open("README.md", "r") as f:
    desc = f.read()
    desc = desc.split("<!-- content -->")[-1]
    desc = re.sub("<[^<]+?>", "", desc)

setup(
    name="polifator",
    version="0.0.1",
    description="Multifactor modelling in python",
    long_description=desc,
    long_description_content_type="text/markdown",
    url="https://github.com/danielmartinscabanas/polifactor",
    author="Daniel Martins Cabanas",
    author_email="danielmartinscabanas@gmail.com",
    license="MIT",
    packages=["polifactor"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Office/Business :: Financial",
        "Topic :: Office/Business :: Financial :: Investment",
    ],
    keywords="multifactor models finance forecast investment",
    install_requires=["numpy", "pandas"],
    python_requires=">=3.5",
    project_urls={
        "",
    },
)