import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyslackline",
    version="0.0.1",
    author="Markus Rampp",
    author_email="markus.rampp@tum.de",
    description="Package to analyze load cell data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/Grommi/pyslackline",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)