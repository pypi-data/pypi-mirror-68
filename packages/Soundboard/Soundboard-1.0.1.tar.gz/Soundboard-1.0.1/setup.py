import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Soundboard", # Replace with your own username
    version="1.0.1",
    author="ghostlypi",
    author_email="parthi@khanlabschool.org",
    description="This is a sound generation & packaging software!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ghostlypi/Soundboard",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
