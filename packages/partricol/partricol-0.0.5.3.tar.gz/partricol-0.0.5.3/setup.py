import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="partricol", # Replace with your own username
    version="0.0.5.3",
    author="Yang Chen",
    author_email="cycyustc@gmail.com",
    description="Package collected during my work with PARSEC-TRILEGAL-COLIBRI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/cycyustc/partricol",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
