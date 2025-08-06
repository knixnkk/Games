import random
import numpy as np

class Sudoku:
    def __init__(self, size=9):
        self.size = size
        self.board = np.zeros((size, size), dtype=int)
        self.generate_board()
        
    def generate_board(self):
        self.fill_diagonal()
        self.fill_remaining(0, 0)
        
    def fill_diagonal(self):
        for i in range(0, self.size, 3):
            self.fill_box(i, i)
                
    def fill_box(self, row, col):
        nums = list(range(1, 10))
        random.shuffle(nums)
        for i in range(3):
            for j in range(3):
                self.board[row + i][col + j] = nums.pop()
    def fill_remaining(self, row, col):
        if row >= self.size - 1 and col >= self.size:
            return True
        if col >= self.size:
            row += 1
            col = 0
        if self.board[row][col] != 0:
            return self.fill_remaining(row, col + 1)
        
        for num in range(1, 10):
            if self.is_safe(row, col, num):
                self.board[row][col] = num
                if self.fill_remaining(row, col + 1):
                    return True
                self.board[row][col] = 0
        return False
    
    def is_safe(self, row, col, num):
        return (num not in self.board[row] and
                num not in self.board[:, col] and
                num not in self.board[row - row % 3:
                row - row % 3 + 3, col - col % 3:col - col % 3 + 3])

    def print_board(self):
        for i, row in enumerate(self.board):
            print(" ".join(str(num) if num != 0 else '.' for num in row[0:3]), "|",
                  " ".join(str(num) if num != 0 else '.' for num in row[3:6]), "|",
                  " ".join(str(num) if num != 0 else '.' for num in row[6:9]))
            if i % 3 == 2 and i != 8:
                print("-" * 21)
    
    def get_board(self):
        return self.board.copy()

    def reset_board(self):
        self.board.fill(0)
        self.generate_board()
    
    def play_move(self, row, col, num):
        if self.is_safe(row, col, num):
            self.board[row][col] = num
            return True
        return False

    def is_solved(self):
        return all(num != 0 for row in self.board for num in row) and \
               all(len(set(row)) == self.size for row in self.board) and \
               all(len(set(self.board[:, col])) == self.size for col in range(self.size)) and \
               all(len(set(self.board[row - row % 3:row - row % 3 + 3, col - col % 3:col - col % 3 + 3].flatten())) == self.size
                   for row in range(0, self.size, 3) for col in range(0, self.size, 3))
    def get_hint(self, row, col):
        if self.board[row][col] != 0:
            return None
        for num in range(1, 10):
            if self.is_safe(row, col, num):
                return num
        return None

    def remove_numbers(self, count):
        positions = [(r, c) for r in range(self.size) for c in range(self.size)]
        random.shuffle(positions)
        for r, c in positions[:count]:
            self.board[r][c] = 0

    def create_puzzle(self, difficulty='easy'):
        if difficulty == 'easy':
            self.remove_numbers(20)
        elif difficulty == 'medium':
            self.remove_numbers(40)
        elif difficulty == 'hard':
            self.remove_numbers(60)
        else:
            raise ValueError("Difficulty must be 'easy', 'medium', or 'hard'.")
    def save_board(self, filename):
        np.savetxt(filename, self.board, fmt='%d')
    
    def load_board(self, filename):
        self.board = np.loadtxt(filename, dtype=int)
        if self.board.shape != (self.size, self.size):
            raise ValueError("Loaded board size does not match initialized size.")

    def clear_board(self):
        self.board.fill(0)
    
    def get_size(self):
        return self.size

    def __str__(self):
        return "\n".join(" ".join(str(num) if num != 0 else '.' for num in row) for row in self.board)
    def __repr__(self):
        return f"Sudoku(size={self.size})"
    
if __name__ == "__main__":
    sudoku = Sudoku()
    sudoku.create_puzzle('medium')
    print("Sudoku Puzzle:")
    sudoku.print_board()

    while not sudoku.is_solved():
        try:
            user_input = input("\nEnter row (1-9), column (1-9), and number (1-9) separated by spaces (or 'q' to quit): ")
            if user_input.lower() == 'q':
                print("Exiting game.")
                break
            row, col, num = map(int, user_input.split())
            if sudoku.play_move(row - 1, col - 1, num):
                print("\nMove successful!")
            else:
                print("\nInvalid move. Try again.")
            sudoku.print_board()
        except Exception as e:
            print("Invalid input. Please enter three numbers separated by spaces.")

    if sudoku.is_solved():
        print("\nCongratulations! You solved the Sudoku.")