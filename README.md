# Extractlib

This is a Python package that provides a set of tools and utilities for processing and analyzing PDF documents. It includes functionality for extracting text and tables from PDFs, cleaning and preprocessing text data, and analyzing content for keywords and patterns. The package also provides a number of configuration options for customizing the behavior of the tools and utilities, making it flexible and easy to use in a variety of different contexts. Whether you need to extract data from PDF documents for data analysis, or analyze PDF content for specific keywords or patterns, this package provides the tools you need to get the job done quickly and efficiently.

#### manually install supporting binaries
## dependency overview
- https://camelot-py.readthedocs.io/en/master/user/install-deps.html#install-deps

## windows dependency installations
- Install ghostscript: https://ghostscript.com/releases/gsdnld.html
- Install Tinker: https://platform.activestate.com/activestate/activetcl-8.6/auto-fork?_ga=2.93217438.2024444162.1679060315-1994225326.1678735799
 

# Example

from extractlib.document.process import process_document
import json

def main(file: str):
    result = process_document(file, extracted_files_output_dir='./output', use_multithreading=False, exclude_pages=[2,3])
    # Save the HTML content to a temporary file
    with open('temp.json', 'w') as f:
        json.dump(result, f, indent=4)


if __name__ == '__main__':

    # get working directory
    import os
    target_dir = os.path.dirname(os.path.abspath(__file__))
    main(f'{target_dir}/_tempdata/PDF.pdf')