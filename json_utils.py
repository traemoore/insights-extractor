import re

from nlp.pre_process import clean_text

def extract_json_values(json_obj, result_str):
    """
    Recursively extract all string values from a nested JSON object and concatenate them into a single string.

    Args:
        json_obj (dict or list): A nested JSON object to extract values from.
        result_str (list): A list used to accumulate the extracted values.

    Returns:
        str: A string containing all extracted values concatenated together, converted to lowercase.
    """
    if isinstance(json_obj, dict):
        for key, value in json_obj.items():
            extract_json_values(value, result_str)
    elif isinstance(json_obj, list):
        for item in json_obj:
            extract_json_values(item, result_str)
    else:
        result_str.append(json_obj)
    return ' '.join(result_str).lower()


def cleanse_and_tag_json_structure(data):
    """
    Evaluate a JSON data structure for invalid content and tag it with validity information.

    Args:
        data (dict or list): A dictionary or list containing the JSON data structure to cleanse.

    Returns: None

    Example: { "valid": true | false, "item1": ..., "item2": ..., ... }
    """

    # Check if the data is a dictionary
    if isinstance(data, dict):
        keys_to_remove = []

        # Loop over the dictionary keys and values
        for key, value in data.items():
            # If the value is a string
            if isinstance(value, str):
                # Check if the string contains any invalid content
                if test_for_invalid_content(value):
                    # If the string contains invalid content, tag the entire data structure as invalid
                    data["valid"] = False
                else:
                    # Otherwise, clean the string using the clean_text function and update the dictionary value
                    data[key] = clean_text(value, False)
            else:
                # If the value is not a string, recurse into the data structure to cleanse and tag nested values
                cleanse_and_tag_json_structure(value)

        # Remove any keys that were flagged for removal during the loop
        for key in keys_to_remove:
            del data[key]

    # Check if the data is a list
    elif isinstance(data, list):
        # Loop over the list items
        for i, value in enumerate(data):
            # If the list item is a string
            if isinstance(value, str):
                # Check if the string contains any invalid content
                if test_for_invalid_content(value):
                    # If the string contains invalid content, tag the entire data structure as invalid
                    data["valid"] = False
                else:
                    # Otherwise, clean the string using the clean_text function and update the list item
                    data[i] = clean_text(value, False)
            else:
                # If the list item is not a string, recurse into the data structure to cleanse and tag nested values
                cleanse_and_tag_json_structure(value)


def test_for_invalid_content(text, regex_list):
    """
    Check if a string contains any invalid content based on a list of regex statements.

    Args:
        text (str): The input text to check.
        regex_list (list): A list of regex statements to evaluate against the input text.

    Returns:
        bool: True if the input text contains any invalid content, False otherwise.
    """
    for regex in regex_list:
        if re.search(regex, text):
            return True
    return False