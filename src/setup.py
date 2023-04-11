from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="t-extractlib",
    version="0.0.7",
    author="Trae Moore",
    author_email="trae.dev@gmail.com",
    description="A package standardized for extracting data from PDFs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/traemoore/extractlib",
    project_urls={
        "Bug Tracker": "https://github.com/traemoore/extractlib/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    install_requires=[
        "setuptools>=61.0",
        "nltk==3.8.1",
        "PyMuPDF==1.21.1",
        "camelot-py==0.11.0",
        "opencv-python==4.7.0.72",
        "ghostscript==0.7"
    ],
    python_requires=">=3.10",
)
