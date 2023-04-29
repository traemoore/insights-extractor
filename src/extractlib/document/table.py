import json
from ..nlp.pre_process import clean_text
from ..utils.json_utils import cleanse_and_tag_json_structure, extract_json_values



def corrilate_table_data(table_elements, table_data):
    # Initialize an empty dictionary to store tables
    tables = {}
    
    if not table_elements or not table_data:
        return None

    # Iterate through each table in table_data
    tbl_idx = 0
    while tbl_idx < len(table_data):
        table = table_data[tbl_idx]

        # Iterate through each row in the table's JSON data
        row_idx = 0
        while row_idx < len(table['json']):
            row = table['json'][row_idx]

            # Iterate through each column in the row
            col_idx = 0
            while col_idx < len(row):
                col = row[f'{col_idx}']
                
                # If the column is empty, increment the column index and continue to the next column
                if not col:
                    col_idx += 1
                    continue
                
                ends_column = False

                # Iterate through each line in table_elements
                line_idx = 0
                while line_idx < len(table_elements):
                    line = table_elements[line_idx]
                    
                    # If the line text is empty, remove the line and continue to the next line
                    if not line['text'].strip():
                        table_elements.pop(line_idx)
                        continue
                    
                    # If the line text is found in the column or _col_contains_line_text returns a positive value
                    if line['text'] in col or _col_contains_line_text(col, line['text']) > -1:
                        ends_column = col.endswith(line['text'])
                        
                        # Update the line with its row and column information
                        line.update({'row': row_idx, 'column': col_idx})
                        
                        # If the table index is not in the tables dictionary, create a new empty list for the table index
                        if tbl_idx not in tables:
                            tables[tbl_idx] = []
                        
                        # Remove the line from table_elements and append it to the corresponding table in tables
                        element = table_elements.pop(line_idx)
                        del element['table']
                        tables[tbl_idx].append(element)

                        # If the column ends with the line text, increment the column index and break the loop
                        if ends_column:
                            col_idx += 1
                            break
                        continue
                    else:
                        col_idx += 1
                        break

            # Increment the row index
            row_idx += 1

        # If there are no more elements with 'table': 0, increment the table index
        if all(element.get('table') != 0 for element in table_elements):
            tbl_idx += 1
    
    # Sort the elements in each table by their row and column values
    sorted_tables = {key: sorted(tables[key], key=lambda x: (x['row'], x['column'])) for key in tables}
    
    # Return the sorted tables if table_elements is empty, otherwise return None
    return sorted_tables if not any(table_elements) else None


def _col_contains_line_text(col, line_text):
    try:
        return col.index(line_text.strip())
    except Exception:
        return -1

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