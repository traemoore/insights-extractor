import json
from nlp.pre_process import clean_text

from utils.json_utils import cleanse_and_tag_json_structure, extract_json_values


def corrilate_table_data(table_elements, table_data):
    """
    This function correlates the input table elements with their respective table data
    by finding the row and column for each element in the table_data.
    
    Parameters:
    table_elements (list): A list of dictionaries, where each dictionary represents a line of data with a 'table' key.
    table_data (list): A list of dictionaries, where each dictionary represents the structure of a table with a 'json' key.

    Returns:
    list: A list of updated table_data dictionaries with the correlated table elements.
    """

    # Initialize an empty dictionary to store tables and a search context dictionary to store search positions
    tables = {}
    search_context = {}

    # Iterate through each line in table_elements
    for line in table_elements:
        # Set initial search context for the table
        search_context[line['table']] = {'row': 0, 'column': 0}

        tbl_idx = line['table']
        table = table_data[tbl_idx]
        found = False

        # Iterate through the rows starting from the last searched row
        for idx in range(search_context[line['table']]['row'], len(table['json'])):
            # Reset the column search position if moving to a new row
            search_context[line['table']]['column'] = 0 if idx > search_context[line['table']]['row'] else search_context[line['table']]['column']
            
            row = table['json'][idx]

            # Iterate through the columns starting from the last searched column
            for col_idx in range(search_context[line['table']]['column'], len(row)):
                # Check if the column exists in the row
                if not f'{col_idx}' in row:
                    break
                
                col = row[f'{col_idx}']

                if not col:
                    continue

                # Check if the line text is in the column text
                if line['text'] in col:
                    line['row'] = idx
                    line['column'] = col_idx
                    search_context[line['table']]['row'] = idx
                    search_context[line['table']]['column'] = col_idx+1 if col.endswith(line['text']) else col_idx
                    found = True
                    break

            # Stop searching the current table if the element is found
            if found:
                break

        # Initialize an empty list for the table index if it's not in the tables dictionary
        if tbl_idx not in tables:
            tables[tbl_idx] = []

        # Remove the 'table' key from the line dictionary
        del line['table']

        # Append the modified line dictionary to the list corresponding to its table index
        tables[tbl_idx].append(line)
        
    for idx in range(len(table_data)):
        table_data[idx]['json'] = tables[idx]

    # Convert the tables dictionary to a list of tuples (table index, list of rows)
    return table_data


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