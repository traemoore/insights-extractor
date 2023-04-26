import camelot
import fitz
import base64

def get_images(filename):
    """
    Extract images from a PDF page.

    Args:
        filename (str): The path to the PDF file.

    Returns:
        list: A list of dictionaries containing the extracted images.
    """

    images_json = []

    # Open the PDF document
    with fitz.open(filename) as doc:
        page = doc[0]
        image_info_list = page.get_image_info()
        images = page.get_images(full=True)

        # Iterate through the extracted images and their rectangles
        for i, image in enumerate(images):
            target_image = None
            
            target_image = image_info_list[i]
            # target_image = [img for img in image_info_list if img['cs-name'] == image[5]][0]

            # Get the image binary data
            img_base64 = doc.extract_image(image[0])['image']

            # Convert the image binary data to a base64 encoded string
            img_base64_str = base64.b64encode(img_base64).decode('utf-8')

            # Create a dictionary containing the image metadata
            image_data = {
                "xref": image[0],
                "width": target_image['width'],
                "height": target_image['height'],
                "colorspace": target_image['colorspace'],
                "bpc": target_image['bpc'],
                "image": img_base64_str,
                "bbox": target_image['bbox'],
                "transform": target_image['transform'],
            }

            # Add the image metadata dictionary to the images_json list
            images_json.append(image_data)
    return images_json

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
    page_lines = []

    # Open the PDF document
    with fitz.open(filename) as doc:
        # Get the first page of the document
        page = doc[0]

        # Get the page height and width
        page_height = page.mediabox.height
        page_width = page.mediabox.width
        
        # Get the text blocks on the page
        blocks = page.get_text('dict')
        
        # collect all lines into a set
        table_lines = []

        # Remove lines contained in tables
        for block in blocks['blocks']:
            if 'lines' in block:
                for line in block['lines']:
                    # Get the bounding box for the line
                    x1, y1, x2, y2 = line['bbox']

                    # Normalize the line bounding box to the page
                    line['bbox'] = (x1, page_height-y2, x2, page_height-y1)

                    table_idx = _in_table(line, tables)
                    # Check if the line is contained in a table
                    collection = page_lines if not table_idx else table_lines
                    
                    data = {
                        'text': line['spans'][0]['text'],
                        'valid': True,
                        'bbox': line['bbox'],
                        'font': {
                            'size': line['spans'][0]['size'],
                            'family': line['spans'][0]['font'],
                            'color': line['spans'][0]['color']
                        },
                    }
                    
                    # Add the table index to the line if it is contained in a table
                    if table_idx:
                        data['table'] = table_idx - 1

                    # Add the line to the list of extracted lines
                    collection.append(data)

    

    # Sort the lines by y-coordinate and then x-coordinate
    sorted_page_elements = sorted(page_lines, key=lambda line: (-line['bbox'][3], line['bbox'][0]))

    # Return the sorted lines
    return sorted_page_elements, table_lines


def _in_table(line, tables):
    """
    Check if a line is contained in a table.

    Args:
        line (dict): A dictionary containing the line data.
        tables (list): A list of table objects representing tables on the page.

    Returns:
        bool: True if the line is contained in a table, False otherwise.
    """
    for table in tables:
        if table.contains(line):
            return table.order
    return None