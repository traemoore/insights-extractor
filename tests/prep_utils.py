import unittest
from src.extractlib.classification.prep_utils import calculate_keyword_frequencies, extract_classification_text, tokenize_content

standard_test_data = {
    "0": [
        {
            "text": "Plans",
            "valid": True,

            "row": 0,
            "column": 0
        },
        {
            "text": "Type",
            "valid": True,

            "row": 0,
            "column": 1
        },
        {
            "text": "Total Monthly Premium",
            "valid": True,

            "row": 0,
            "column": 2
        },
        {
            "text": "Bundled Premium",
            "valid": True,

            "row": 0,
            "column": 3
        },
        {
            "text": "Essential Choice Classic CA-C26",
            "valid": True,

            "row": 1,
            "column": 0
        },
        {
            "text": "Network:Dental Complete",
            "valid": True,

            "row": 1,
            "column": 0
        },
        {
            "text": "Contract Code:3KM9",
            "valid": True,

            "row": 1,
            "column": 0
        },
        {
            "text": "Dental",
            "valid": True,

            "row": 1,
            "column": 1
        },
        {
            "text": "$786.98",
            "valid": True,

            "row": 1,
            "column": 2
        },
        {
            "text": "$747.59",
            "valid": True,

            "row": 1,
            "column": 3
        },
        {
            "text": "Dental Net 3000D-1",
            "valid": True,

            "row": 2,
            "column": 0
        },
        {
            "text": "Network:Dental Net HMO",
            "valid": True,

            "row": 2,
            "column": 0
        },
        {
            "text": "Contract Code:3T8E",
            "valid": True,

            "row": 2,
            "column": 0
        },
        {
            "text": "Dental",
            "valid": True,

            "row": 2,
            "column": 1
        },
        {
            "text": "$292.16",
            "valid": True,

            "row": 2,
            "column": 2
        },
        {
            "text": "$277.56",
            "valid": True,

            "row": 2,
            "column": 3
        },
        {
            "text": "FS.A.10.25.130.130",
            "valid": True,

            "row": 3,
            "column": 0
        },
        {
            "text": "Network:Blue View Vision",
            "valid": True,

            "row": 3,
            "column": 0
        },
        {
            "text": "Contract Code:4B4L",
            "valid": True,
            "row": 3,
            "column": 0
        },
        {
            "text": "Funding Type : Employer Paid",
            "valid": True,

            "row": 3,
            "column": 0
        },
        {
            "text": "Vision",
            "valid": True,

            "row": 3,
            "column": 1
        },
        {
            "text": "$154.15",
            "valid": True,

            "row": 3,
            "column": 2
        },
        {
            "text": "$146.47",
            "valid": True,
            "row": 3,
            "column": 3
        }
    ]
}

class TestMyModule(unittest.TestCase):
    def test_calculate_keyword_frequencies(self):
        content = "The quick brown fox jumps over the lazy dog."
        keywords = {'quick': 2, 'brown': 1}
        synonyms = {'fox': ['animal'], 'dog': ['pet', 'canine']}
        regex_list = [r'\bthe\b', r'\bover\b']
        stop_words = ['the', 'and', 'a', 'to']
        expected_result = [('quick', 2), ('brown', 1), ('fox', 1), ('jumps', 1), ('lazy', 1), ('dog', 1)]
        result = calculate_keyword_frequencies(content, keywords, synonyms, regex_list, False, stop_words)
        self.assertEqual(result, expected_result)

    def test_extract_classification_text(self):
        json_data = {
            'title': {'text': 'The quick brown fox', 'valid': True},
            'body': {'text': 'jumps over the lazy dog.', 'valid': True},
            'comments': [
                {'text': 'Great post!', 'valid': True },
                {'text': 'This is spam.', 'valid': True}
            ],
        }
        regex_list = [r'\bspam\b']
        stop_words = ['the', 'and', 'a', 'to', 'over']
        expected_result = 'quick brown fox jumps lazy dog Great post'
        result = extract_classification_text(json_data, regex_list, stop_words)
        self.assertEqual(result, expected_result)

    def test_extract_classification_text_standard(self):
        json_data = standard_test_data
        regex_list = [r'(?<!\S)\$(?:[1-9]\d{0,2}(?:,\d{3}){0,2}|[1-9]\d{0,7}|0)(?:\.\d{1,2})?(?!\S)']
        stop_words = []
        expected_result = 'Plans Type Total Monthly Premium Bundled Premium Essential Choice Classic CAC26 NetworkDental Complete Contract Code3KM9 Dental Dental Net 3000D1 NetworkDental Net HMO Contract Code3T8E Dental FSA1025130130 NetworkBlue View Vision Contract Code4B4L Funding Type Employer Paid Vision'
        result = extract_classification_text(json_data, regex_list, stop_words)
        self.assertEqual(result, expected_result)

    def test_tokenize_content(self):
        content = "The quick brown fox jumps over the lazy dog."
        stop_words = ['the', 'and', 'a', 'to']
        expected_result = ['quick', 'brown', 'fox', 'jumps', 'lazy', 'dog', '.']
        result = tokenize_content(content, True, stop_words)
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
