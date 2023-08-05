import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="matrix-henryj",
    version="1.0.0",
    author="Henry",
    author_email="henryj@kth.se",
    description="A package implementing matrices",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/grudat20/henryj-ovn7",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
