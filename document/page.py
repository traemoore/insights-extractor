import camelot, fitz

def extract_tables(file):
    """
    Extract tables from a PDF file using Camelot.
    
    Returns: a list of camelot.core.TableList objects
    """
    tables = camelot.read_pdf(file, flavor='lattice', pages='1')
    return tables


def extract_lines(filename, tables):
    """
    Extract lines of text from a PDF page and remove lines contained in tables.

    Args:
        filename (str): The path to the PDF file.
        tables (list): A list of table objects representing tables on the page.

    Returns:
        list: A list of dictionaries containing the extracted lines.
    """

    # Create an empty list to store the extracted lines
    lines = []

    # Open the PDF document
    with fitz.open(filename) as doc:
        # Get the first page of the document
        page = doc[0]

        # Get the page height and width
        page_height = page.mediabox.height
        page_width = page.mediabox.width
        
        # Get the text blocks on the page
        blocks = page.get_text('dict')
        
        # Remove lines contained in tables
        for block in blocks['blocks']:
            if 'lines' in block:
                for line in block['lines']:
                    # Get the bounding box for the line
                    x1, y1, x2, y2 = line['bbox']

                    # Normalize the line bounding box to the page
                    line['bbox'] = (x1, page_height-y2, x2, page_height-y1)

                    # Check if the line is contained in a table
                    if not any(table.contains(line, page_height, page_width) for table in tables):
                        # Add the line to the list of extracted lines
                        lines.append({
                            'text': line['spans'][0]['text'],
                            'valid': True,
                            'bbox': line['bbox'],
                            'font': {
                                'size': line['spans'][0]['size'],
                                'family': line['spans'][0]['font'],
                                'color': line['spans'][0]['color']
                            },
                        })
    
    # Sort the lines by y-coordinate and then x-coordinate
    sorted_lines = sorted(lines, key=lambda line: (-line['bbox'][3], line['bbox'][0]))

    # Return the sorted lines
    return sorted_lines
