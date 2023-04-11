from ..settings import config
import os
import fitz

def split_document_pages(doc_path, output_dir=None):
    """
    Split a PDF document into individual pages and save each page to a separate PDF file.

    Args:
        doc_path (str): Path to the input PDF file.
        output_dir (str): Directory to save the output files (default=None).

    Raises:
        Exception: If doc_path is a directory instead of a file.

    Returns:
        tuple: A tuple containing the path to the output directory and a list of the output file paths.
    """

    # Check if doc_path is a file
    if os.path.isdir(doc_path):
        raise Exception('doc_path must be a file, not a directory')

    # Create an empty list to store the output file paths
    files = []

    # Get the PDF filename without extension
    pdf_filename = os.path.splitext(os.path.basename(doc_path))[0]

    # Create a directory for the PDF pages
    target_dir = os.path.join(os.path.dirname(doc_path), pdf_filename) if output_dir is None else output_dir
    os.makedirs(target_dir, exist_ok=True)

    # Open the input PDF document
    with fitz.open(doc_path) as doc:

        # Loop over each page in the PDF document
        for page_num in range(doc.page_count):
            # Construct the output filename for this page
            page_filename = f"{page_num+1}.pdf"
            page_path = os.path.join(target_dir, page_filename)

            # Create a new PDF document with only the current page
            with fitz.open() as new_doc:
                new_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)

                # Save the new PDF document to a file
                new_doc.save(page_path)

                # Add the output file path to the list of files
                files.append(page_path)

                # Print a message to the console (optional)
                if config.std_out_logging:
                    print(f"Saved page {page_num+1} to {page_path}")

    # Return the path to the output directory and the list of output file paths
    return (target_dir, files)
