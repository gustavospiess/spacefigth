import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="spacefigth-ghspiess", # Replace with your own username
    version="0.0.1",
    author="Gustavo Henrique Spiess",
    author_email="gustavospiess@gmail",
    description="A 3D sea battle game",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gustavospiess/spacefigth",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
