import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cogsly", 
    version="0.0.1",
    author="Jake Kara",
    author_email="jake@jakekara.com",
    description="Prototype for notebook module system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jakekara/cogsly",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "nbformat==5.0.6",
        "IPython"
    ],
    python_requires='>=3.6',
)
