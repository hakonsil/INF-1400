from sudoku_reader import Sudoku_reader
from board import Board
from square import Square
from element import Element
import time
start_time = time.time()

class Sudokuboard(Board):
    def __init__(self, nums):
        super().__init__(nums)
        self._set_up_nums(nums)
        self._set_up_elems()

    def _set_up_nums(self, nums):
        """Set up the squares on the board (ints into Square objects)"""
        self.nums = [[Square(nums[i][j]) for j in range(self.n_rows)] for i in range(self.n_cols)]

    def _set_up_elems(self):
        """Link squares to their elements (rows, columns, boxes)"""

        # initialize lists of elements for each 'category'
        rows = []
        cols = []
        boxes = []

        # create elements and insert them in their respective lists
        for i in range(9):
            rows.append(Element("row"))
            cols.append(Element("col"))
            boxes.append(Element("box"))
        
        # Link squares to rows and columns
        for i in range(9):
            for j in range(9):
                rows[i].add_square(self.nums[i][j])
                cols[i].add_square(self.nums[j][i])
        
        # link squares to boxes (a bit ugly, and could be done in a more consise way, but it works)
        for i in range(9):
            for j in range(9):
                if i // 3 == 0:
                    if j // 3 == 0:
                        boxes[0].add_square(self.nums[i][j])
                    elif j // 3 == 1:
                        boxes[1].add_square(self.nums[i][j])
                    elif j // 3 == 2:
                        boxes[2].add_square(self.nums[i][j])
                elif i // 3 == 1:
                    if j // 3 == 0:
                        boxes[3].add_square(self.nums[i][j])
                    elif j // 3 == 1:
                        boxes[4].add_square(self.nums[i][j])
                    elif j // 3 == 2:
                        boxes[5].add_square(self.nums[i][j])
                elif i // 3 == 2:
                    if j // 3 == 0:
                        boxes[6].add_square(self.nums[i][j])
                    elif j // 3 == 1:
                        boxes[7].add_square(self.nums[i][j])
                    elif j // 3 == 2:
                        boxes[8].add_square(self.nums[i][j])

    def solve(self):
        """Solves the sudoku"""
        for i in range(9):
            for j in range(9):
                if self.nums[i][j].value == 0: # skips the numbers that are already filled in
                    for k in range(1, 10): # iterates through all numbers, starting at the lowest value
                        if self.nums[i][j].legal(k): #checks if the number is legal
                            self.nums[i][j].set_value(k) 
                            self.solve() # recursively calls the function (backtracking)
                            self.nums[i][j].set_value(0) # if the sudoku is not solved, the number is set to 0 and the loop continues
                    return
        #print(self)

    def __str__(self):
        """Prints the board in a reasonable format"""
        r = "Solved sudoku: " + "\n"
        r += "[["
        for num in self.nums:
            for elem in num:
                r += str(elem.get_value()) + ", "
            r = r[:-2] + "]" + "\n ["
        r = r[:-3] + "]"
        return r

if __name__ == "__main__":
    """Solves n sudokus"""
    n = 100
    reader = Sudoku_reader("sudoku_1M.csv")
    for i in range(n):
        board = Sudokuboard(reader.next_board())
        board.solve()
    # prints the time it takes to solve n sudokus
    print("Time to solve", n, "sudoku(s): ", time.time() - start_time, "seconds")