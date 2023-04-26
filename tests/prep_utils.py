import unittest
from src.extractlib.classification.prep_utils import calculate_keyword_frequencies, extract_classification_text, tokenize_content

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

    def test_tokenize_content(self):
        content = "The quick brown fox jumps over the lazy dog."
        stop_words = ['the', 'and', 'a', 'to']
        expected_result = ['quick', 'brown', 'fox', 'jumps', 'lazy', 'dog', '.']
        result = tokenize_content(content, True, stop_words)
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
