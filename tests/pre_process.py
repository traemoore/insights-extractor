import unittest
from src.extractlib.nlp.pre_process import clean_text

class TestCleanText(unittest.TestCase):
    
    def test_simple(self):
        text = "This is a simple test. With some extra spaces    and a newline\n character."
        expected_result = "This is a simple test. With some extra spaces and a newline character."
        result = clean_text(text)
        self.assertEqual(result, expected_result)
        
    def test_complex(self):
        text = "This is a more complex test! It includes some numbers, like 1234567890, and some (punctuation marks), such as: commas, periods, colons, semicolons, exclamation points!, question marks?, and parentheses (). It also includes some non-ASCII characters, like ë, á, and ç. Finally, it includes some substrings that match regex patterns, such as 'www.example.com', 'email@example.com', and '[WARNING]'."
        expected_result = "This is a more complex test It includes some numbers like 1234567890 and some punctuation marks such as commas periods colons semicolons exclamation points question marks and parentheses It also includes some nonASCII characters like and Finally it includes some substrings that match regex patterns such as and"
        regex_list = [r'www\.\S+', r'\S+@\S+', r'\[WARNING\]']
        result = clean_text(text, remove_punctuation=True, regex_list=regex_list)
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
