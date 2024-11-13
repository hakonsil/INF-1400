class Element:
    def __init__(self, type):
        self.squares = []
        self.type = type

    def add_square(self, square):
        """Add a square to the element, and identifies the element as the square's row, column or box"""
        self.squares.append(square)
        if self.type == "box":
            square.box = self
        elif self.type == "row":
            square.row = self
        elif self.type == "col":
            square.col = self

    def check_legal(self, possible_num):
        """Check if a possible number is legal in the element"""
        for square in self.squares:
            if square.get_value() == possible_num:
                return False
        return True