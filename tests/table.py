import unittest
from unittest.mock import MagicMock
from src.extractlib.document.table import corrilate_table_data

class TestCorrilateTableData(unittest.TestCase):

    def test_corrilation_with_currency(self):
        # Define the test input data
        table_elements = [
            {'text': 'Date', 'table': 0},
            {'text': 'Amount', 'table': 0},
            {'text': 'Total', 'table': 0},
            {'text': 'Jan 1', 'table': 0},
            {'text': '$10.00', 'table': 0},
            {'text': '$20.00', 'table': 0},
            {'text': 'Jan 2', 'table': 0},
            {'text': '$15.00', 'table': 0},
            {'text': '$25.00', 'table': 0},
            {'text': 'Net', 'table': 0},
            {'text': '$25.00', 'table': 0},
            {'text': 'Date', 'table': 1},
            {'text': 'Amount', 'table': 1},
            {'text': 'Total', 'table': 1},
            {'text': 'Feb 1', 'table': 1},
            {'text': '¥1000', 'table': 1},
            {'text': '¥2000', 'table': 1},
            {'text': 'Feb 2', 'table': 1},
            {'text': '¥1500', 'table': 1},
            {'text': '¥2500', 'table': 1},
            {'text': 'Net', 'table': 1},
            {'text': '¥2500', 'table': 1},
        ]
        table_data = [
            {
                'valid': True,
                'table': 0,
                'json': [
                    {'0': 'Date', '1': 'Amount', '2': 'Total'},
                    {'0': 'Jan 1', '1': '$10.00', '2': '$20.00'},
                    {'0': 'Jan 2', '1': '$15.00', '2': '$25.00'},
                    {'0': 'Net', '1': '$25.00', '2': ''}
                ],
                'classification_training_data': ''
            },
            {
                'valid': True,
                'table': 1,
                'json': [
                    {'0': 'Date', '1': 'Amount', '2': 'Total'},
                    {'0': 'Feb 1', '1': '¥1000', '2': '¥2000'},
                    {'0': 'Feb 2', '1': '¥1500', '2': '¥2500'},
                    {'0': 'Net', '1': '¥2500', '2': ''}
                ],
                'classification_training_data': ''
            }
        ]

        # Call the function under test
        result = corrilate_table_data(table_elements, table_data)

        # Assert the results
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], list)
        self.assertIsInstance(result[1], list)
        self.assertEqual(len(result[0]), 11)
        self.assertEqual(len(result[1]), 11)

        # Assertions for first set of data
        self.assertEqual(result[0][0]['text'], 'Date')
        self.assertEqual(result[0][1]['text'], 'Amount')
        self.assertEqual(result[0][2]['text'], 'Total')
        self.assertEqual(result[0][3]['text'], 'Jan 1')
        self.assertEqual(result[0][4]['text'], '$10.00')
        self.assertEqual(result[0][5]['text'], '$20.00')
        self.assertEqual(result[0][6]['text'], 'Jan 2')
        self.assertEqual(result[0][7]['text'], '$15.00')
        self.assertEqual(result[0][8]['text'], '$25.00')
        self.assertEqual(result[0][9]['text'], 'Net')
        self.assertEqual(result[0][10]['text'], '$25.00')

        # Assertions for second set of data
        self.assertEqual(result[1][0]['text'], 'Date')
        self.assertEqual(result[1][1]['text'], 'Amount')
        self.assertEqual(result[1][2]['text'], 'Total')
        self.assertEqual(result[1][3]['text'], 'Feb 1')
        self.assertEqual(result[1][4]['text'], '¥1000')
        self.assertEqual(result[1][5]['text'], '¥2000')
        self.assertEqual(result[1][6]['text'], 'Feb 2')
        self.assertEqual(result[1][7]['text'], '¥1500')
        self.assertEqual(result[1][8]['text'], '¥2500')
        self.assertEqual(result[1][9]['text'], 'Net')
        self.assertEqual(result[1][10]['text'], '¥2500')

    def test_corrilation_empty_input(self):
        # Define the test input data
        table_elements = []
        table_data = [
            {
                'valid': True,
                'table': 0,
                'json': [
                    {'0': 'Date', '1': 'Amount', '2': 'Total'},
                    {'0': 'Jan 1', '1': '$10.00', '2': '$20.00'},
                    {'0': 'Jan 2', '1': '$15.00', '2': '$25.00'},
                    {'0': 'Net', '1': '$25.00', '2': ''}
                ],
                'classification_training_data': ''
            },
            {
                'valid': True,
                'table': 1,
                'json': [
                    {'0': 'Date', '1': 'Amount', '2': 'Total'},
                    {'0': 'Feb 1', '1': '$1000', '2': '$2000'},
                    {'0': 'Feb 2', '1': '$1500', '2': '$2500'},
                    {'0': 'Net', '1': '$2500', '2': ''}
                ],
                'classification_training_data': ''
            }
        ]

        self.assertRaises(ValueError, corrilate_table_data, table_elements, table_data)
        
        # Call the function under test
        # result = corrilate_table_data(table_elements, table_data)

        # Assert the results
        # self.assertIsInstance(result, type(None)) # expects None as output if no input data provided

if __name__ == '__main__':
    unittest.main()
