# write your code here
import random
board = []
last_move = 'X'

def initialize_board(board_p=''):
    """Initialize board"""
    if board_p == '':
        for i in range(3):
            temp = []
            for j in range(3):
                temp.append(' ')
            board.append(temp)
    else:
        sp = [*board_p]
        increment = 0
        for i in range(3):
            temp = []
            for j in range(3):
                temp.append(sp[increment])
                increment += 1
            board.append(temp)
def game_state():
    """Print the state of the game"""
    if len(board) != 0:
        print('---------')
        for i in range(3):
            print('| ', end='')
            for j in range(3):
                print(f'{board[i][j]} ', end='')
            print('|')
        print('---------')
    else:
        print("Board is empty")
def validate_input(input_command):
    """Return True if user input is correct"""
    user_input = input_command.split()
    parameters = ['start easy easy', 'start user user', 'start easy user', 'start user easy']
    if len(user_input) != 3:
        print('Bad parameters!--')
        return True
    elif not input_command in parameters :
        print('Bad parameters!++')
        return True

    return False

def check_space(coordinate):
    """Check if the given coordinate is free space"""
    x = 0
    y = 0
    while True:
        try:
            sp = coordinate.split()
            x = int(sp[0])
            y = int(sp[1])
            if board[x - 1][y - 1] != ' ':
                print('This cell is occupied! Choose another one!')
                coordinate = input('Enter the coordinates: ')
                continue
            elif (x < 1 or x > 3) and (y < 1 or y > 3):
                print('Coordinates should be from 1 to 3!')
                coordinate = input('Enter the coordinates: ')
                continue
        except ValueError:
            print('You should enter numbers!')
            coordinate = input('Enter the coordinates: ')
            continue
        except IndexError:
            print('Coordinates should be from 1 to 3!')
            coordinate = input('Enter the coordinates: ')
            continue
        break
    return x, y

def place_move(move):
    global board
    """Place the move on the board"""
    x = int(move[0]) - 1
    y = int(move[1]) - 1

    # join_board = [item for innerlist in board for item in innerlist] # join board to one list and count the elements
    # x_count = join_board.count('X') # count x
    # y_count = join_board.count('O') # count y

    board[x][y] = last_move
    change_last_move()

def change_last_move():
    global last_move
    if last_move == 'X':
        last_move = 'O'
    else:
        last_move = 'X'

def computer_move():
    while True:
        x = random.randint(0, 2)
        y = random.randint(0, 2)

        if board[x][y] != ' ':
            continue

        board[x][y] = last_move
        change_last_move()
        break

    print('Making move level "easy"')

def winner_state():
    """Check the state of the game and print the winner"""
    winning_lines = [
        [board[0][0], board[0][1], board[0][2]],  # Top row
        [board[1][0], board[1][1], board[1][2]],  # Middle row
        [board[2][0], board[2][1], board[2][2]],  # Bottom row
        [board[0][0], board[1][0], board[2][0]],  # Left column
        [board[0][1], board[1][1], board[2][1]],  # Middle column
        [board[0][2], board[1][2], board[2][2]],  # Right column
        [board[0][0], board[1][1], board[2][2]],  # Diagonal top-left to bottom-right
        [board[0][2], board[1][1], board[2][0]],  # Diagonal top-right to bottom-left
    ]

    # Check each line for a winner
    for line in winning_lines:
        if line.count(line[0]) == 3 and line[0] != ' ':
            print(f'{line[0]} wins')
            return True

    # Check for draw
    if all(cell != ' ' for row in board for cell in row):
        print('Draw')
        return True

    #print('Game not finished')
    return False

def game():
    """Game starts when user puts in the board"""
    start = True
    index = 1 # to take turns

    while start:
        input_command = input('Input command: ')
        if input_command == 'exit':
            break
        
        if validate_input(input_command):
            continue
        sp = input_command.split()
        initialize_board()
        game_state()
        if sp[1] == 'user' and sp[2] == 'user':
            while True:
                coordinates = input('Enter the coordinates: ')
                coord = check_space(coordinates) # check space if valid
                place_move(coord)
                game_state()
                stop = winner_state()
                if stop:
                    break
        elif sp[1] == 'easy' and sp[2] == 'easy':
            while True:
                computer_move()
                game_state()
                stop = winner_state()
                if stop:
                    break
        elif (sp[1] == 'easy' and sp[2] == 'user') or (sp[1] == 'user' and sp[2] == 'easy'):
            if sp[1] == 'user':
                index = 0

            while True:
                if index == 0:
                    coordinates = input('Enter the coordinates: ')
                    coord = check_space(coordinates)  # check space if valid
                    place_move(coord)
                    index = 1
                else:
                    computer_move()
                    index = 0
                game_state()
                stop = winner_state()  # check state after we place a move
                if stop:
                    break
        board.clear()

game()