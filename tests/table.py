import unittest
from unittest.mock import MagicMock
from src.extractlib.document.table import corrilate_table_data

class TestCorrilateTableData(unittest.TestCase):

    def test_corrilate_table_data(self):
        # Test case 1
        table_elements = [
            {'table': 0, 'text': 'Header1'},
            {'table': 0, 'text': 'Header2'},
            {'table': 0, 'text': 'Data1'},
            {'table': 0, 'text': 'Data2'},
        ]
        
        table_data = [
            {
                'json': [
                    {'0': 'Header1', '1': 'Header2'},
                    {'0': 'Data1', '1': 'Data2'},
                ]
            }
        ]
        
        expected_output = {
            0: [
                {'text': 'Header1', 'row': 0, 'column': 0},
                {'text': 'Header2', 'row': 0, 'column': 1},
                {'text': 'Data1', 'row': 1, 'column': 0},
                {'text': 'Data2', 'row': 1, 'column': 1},
            ]
        }
        
        result = corrilate_table_data(table_elements, table_data)
        self.assertEqual(result, expected_output)

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

        self.assertEqual(corrilate_table_data(table_elements, table_data), None)
        
        # Call the function under test
        # result = corrilate_table_data(table_elements, table_data)

        # Assert the results
        # self.assertIsInstance(result, type(None)) # expects None as output if no input data provided

if __name__ == '__main__':
    unittest.main()
