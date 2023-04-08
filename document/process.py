import json
import shutil
import os
from models.table import Table
from nlp.pre_process import clean_text
from .utils import split_document_pages
from settings import config
from concurrent.futures import ThreadPoolExecutor
from .page import extract_lines, extract_tables
from utils.json_utils import cleanse_and_tag_json_structure, extract_json_values
from exceptions import DocumentProcessingError, PageProcessingError
from .utils import split_document_pages


def process_document(file: str, exclude_pages=None, extracted_files_output_dir=None, use_multithreading=False, delete_split_pages=True):
    """
    Process a document by splitting it into pages and processing each page individually.

    Args:
        file (str): The path to the input document file.
        pages (list): A list of page numbers to exclude (non-zero based index). If None, all pages are processed (default=None).
        extracted_files_output_dir (str): The path to the directory where extracted pages should be saved (default=None).
        use_multithreading (bool): Whether to use multi-threading to process the pages (default=False).
        delete_split_pages (bool): Whether to delete the split pages after processing (default=True).

    Returns:
        dict: A dictionary containing the processed data for each page. The dictionary has the following keys:
            - 'pages': A list of dictionaries containing the processed data for each page. Each dictionary has the following keys:
                - 'page': An integer identifying the page number.
                - 'content': A dictionary containing the extracted content for the page.

    Raises: DocumentProcessingError if an error occurs while processing the document.
    """
    result = {
        'pages': []
    }

    try:
        # Split the input document into individual pages
        target_dir, files = split_document_pages(
            file, extracted_files_output_dir)

        # Process each page in the document
        if use_multithreading:
            # If multi-threading is enabled, process each page in a separate thread
            with ThreadPoolExecutor() as executor:
                futures = []
                for i, file_path in enumerate(files):
                    if exclude_pages is None or i+1 not in exclude_pages:
                        futures.append(executor.submit(
                            process_page, file_path, i+1))

                # Wait for all threads to complete and collect the results
                for future in futures:
                    result['pages'].append(future.result())
        else:
            # If multi-threading is disabled, process each page sequentially in the main thread
            for i, file_path in enumerate(files):
                if exclude_pages is None or i+1 in exclude_pages:
                    result['pages'].append(process_page(file_path, i+1))

        # Sort the pages list by page number
        result['pages'] = sorted(result['pages'], key=lambda x: x['page'])
    except Exception as e:
        raise DocumentProcessingError(f'Error processing document {file}: {e}')

    # Delete the extracted pages if the delete_extracted_pages flag is set
    if delete_split_pages:
        shutil.rmtree(target_dir)

    return result


def process_page(file_path, index):
    """
    Process a PDF page and extract data from tables and lines.

    Args:
        path (str): The path to the PDF file.
        index (int): The index of the page to process.

    Raises:
        PageProcessingError: If an error occurs while processing the page.

    Returns:
        dict: A dictionary containing the extracted data.
    """

    # Create an empty dictionary to store the extracted data
    data = {}

    # Print a message to the console indicating that the processing has started
    print(f'starting {file_path}')

    # Check if the file type is supported
    if os.path.splitext(file_path)[1] in config.supported_file_types:
        print(f'processing {file_path}')

        # Create the full file path
        #file_path = path if not os.path.isabs(path) else os.path.join(os.path.dirname(path), path)

        # Check if the file exists
        if not os.path.exists(file_path):
            raise PageProcessingError(f'File {file_path} does not exist')

        try:
            # Extract tables from the PDF page
            raw_tables = extract_tables(file_path)

            # Extract lines from the PDF page
            lines, training_data = extract_lines(file_path, [Table(table._bbox)
                                  for table in raw_tables])

            # Cleanse and tag the lines JSON structure
            cleanse_and_tag_json_structure(lines)

            # Extract data from the tables
            tables = get_table_data(raw_tables)

            # Store the extracted data in the dictionary
            data = {
                'page': index,
                'content': {
                    'sections': lines,  # todo - extract sections
                    'tables': tables,
                    'images': [],
                    'classification_training_data': clean_text(training_data, remove_punctuation=True),
                    # 'kvps': []
                }
            }

            return data
        except Exception as e:
            # Raise an error if an exception occurs while processing the page
            raise PageProcessingError(
                f'Error processing page {index} of {file_path}: {e}')


def get_table_data(tables):
    """
    Extract and clean data from a list of PyMuPDF table objects.

    Args:
        tables (list): A list of PyMuPDF table objects to extract data from.

    Returns:
        list: A list of dictionaries containing cleaned data and metadata for each table.
            Each dictionary has the following keys:
            - 'valid': A boolean indicating whether the data is valid or not.
            - 'table': An integer identifying the table.
            - 'json': A list of dictionaries containing the raw data extracted from the table.
            - 'data': A string containing the cleaned data extracted from the table.
    """
    result_tables = []

    for idx in range(len(tables)):
        jsonString = tables[idx].df.to_json(orient='records')
        jsonData = json.loads(jsonString)

        cleanse_and_tag_json_structure(jsonData)
        dataValue = extract_json_values(jsonData, [])

        cleaned = clean_text(dataValue, remove_punctuation=True)

        table = {
            'valid': True,
            'table': idx,
            'json': jsonData,
            'classification_training_data': cleaned
        }

        result_tables.append(table)
    return result_tables
