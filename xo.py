# X|O
# first turn is X

turn = 0
board = [' ' for _ in range(9)]

def print_board():
    print(f"{board[0]}|{board[1]}|{board[2]}")
    print("-+-+-")
    print(f"{board[3]}|{board[4]}|{board[5]}")
    print("-+-+-")
    print(f"{board[6]}|{board[7]}|{board[8]}")
def check_winner():
    winning_combinations = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8), 
        (0, 4, 8), (2, 4, 6)  
    ]
    for a, b, c in winning_combinations:
        if board[a] == board[b] == board[c] and board[a] != ' ':
            return True, board[a] 
    if ' ' not in board:
        return True, 'Draw' 
    return False

print_board()
while not check_winner() and ' ' in board:
    if turn % 2 == 0:
        print("X's turn")
    else:
        print("O's turn")
    
    user_movement = input("Enter your move (1-9): ")
    print('----------------------------------------')
    
    if user_movement.isdigit() and 1 <= int(user_movement) <= 9:
        index = int(user_movement) - 1
        if board[index] == ' ':
            board[index] = 'X' if turn % 2 == 0 else 'O'
            turn += 1
        else:
            print("Invalid move, try again.")
    else:
        print("Invalid input, please enter a number between 1 and 9.")
    
    print_board()
print(f"Game over! Result: {check_winner()[1]} is the winner!" if check_winner()[1] != "Draw" else "Game over! It's a draw.")