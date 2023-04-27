import json
from src.extractlib.document.table import corrilate_table_data

import unittest
from unittest.mock import MagicMock, patch

class TestGetTableData(unittest.TestCase):
    
    def test_corrilate_table_data(self):
        table_elements = [
            {'text': 'col1', 'table': 0},
            {'text': 'col2', 'table': 0},
            {'text': 'col3', 'table': 0},
            {'text': 'row1', 'table': 0},
            {'text': 'a', 'table': 0},
            {'text': 'b', 'table': 0},
            {'text': 'row2', 'table': 0},
            {'text': 'c', 'table': 0},
            {'text': 'd', 'table': 0},
        ]
        
        table_data = [
            {'valid': True, 'table': 0, 'json': [
                {'0': 'col1', '1': 'col2', '2': 'col3'},
                {'0': 'row1', '1': 'a', '2': 'b'},
                {'0': 'row2', '1': 'c', '2': 'd'},
            ]},
        ]
        
        result = corrilate_table_data(table_elements, table_data)
        
        self.assertEqual(len(result), 1)
        self.assertEqual(len(result[0]), 9)
        self.assertEqual(result[0][0]['text'], 'col1')
        self.assertEqual(result[0][1]['text'], 'col2')
        self.assertEqual(result[0][2]['text'], 'col3')
        self.assertEqual(result[0][3]['text'], 'row1')
        self.assertEqual(result[0][4]['text'], 'a')
        self.assertEqual(result[0][5]['text'], 'b')
        self.assertEqual(result[0][6]['text'], 'row2')
        self.assertEqual(result[0][7]['text'], 'c')
        self.assertEqual(result[0][8]['text'], 'd')
