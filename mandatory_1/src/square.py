class Square:
    def __init__(self, value):
        self.value = value
        self.row = None
        self.col = None
        self.box = None
    
    def legal(self, number):
        """Check if a number is legal"""
        self.number = number
        # using the method from Element to check that the number is not in row, column or box
        if self.row.check_legal(self.number) and self.col.check_legal(self.number) and self.box.check_legal(self.number):
            return True
        return False
    
    def set_value(self, value):
        self.value = value
    
    def get_value(self):
        return self.value