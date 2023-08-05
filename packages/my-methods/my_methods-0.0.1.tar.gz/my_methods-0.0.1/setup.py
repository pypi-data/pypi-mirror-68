import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="my_methods", # Replace with your own username
    version="0.0.1",
    author="Noushad Khan",
    author_email="noushadkhan1994@gmail.com",
    description="my_methods",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/noushadkhan01/my_methods",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
