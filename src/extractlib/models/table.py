class Table:
    def __init__(self, bbox, order):
        self.bbox = bbox
        self.order = order

    def contains(self, line):
        # get the bbox for the table
        table_x1, table_y2, table_x2, table_y1 = self.bbox
        
        # get the bbox for the line
        x1, y1, x2, y2 = line['bbox']
        
        result = (x1 >= table_x1 and y1 <= table_y1 and x2 <= table_x2 and y2 >= table_y2)
        return result