"""
Setup a pip package

How to upload a package to pypi:
 * Update the version number
 * Build the package `python setup.py bdist_wheel`
 * Deploy: `python3 -m twine upload --repository-url https://upload.pypi.org/legacy/  dist/*`

"""
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sshalosh-borisgorelik",
    version="0.0.3",
    author="Boris Gorelik",
    author_email="boris@gorelik.net",
    description="convenience functions for serialization to s3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bgbg/shalosh",
    packages=setuptools.find_packages('./'),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
