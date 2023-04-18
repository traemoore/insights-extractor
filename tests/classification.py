import unittest
from src.extractlib.classification.prep_utils import calculate_keyword_frequencies

class TestCalculateKeywordFrequencies(unittest.TestCase):
    def test_calculate_keyword_frequencies_basic(self):
        content = "This is a test. The test is about testing keyword frequencies."
        keywords = {"test": 2}
        keyword_synonyms = {"test": ["testing"]}
        regex_list = [r'\d+']
        stop_words = ["a", "an", "the", "is", "about"]

        expected_output = [("test", 6), ("This", 1), ("frequencies", 1)]

        result = calculate_keyword_frequencies(content, keywords, keyword_synonyms, regex_list, stop_words)
        self.assertEqual(result, expected_output)

    # Add more test methods for different cases, inputs, and expected outputs.

if __name__ == "__main__":
    unittest.main()