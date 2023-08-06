import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nonfig-sdk",
    version="0.0.2",
    author="Nonfig",
    author_email="admin@nonfig.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nonfig/python-sdk",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
