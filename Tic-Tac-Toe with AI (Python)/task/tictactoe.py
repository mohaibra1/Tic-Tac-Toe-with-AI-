# write your code here
import random
board = []
last_move = 'X'
previous_move = ''
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
    parameters = ['start easy easy', 'start user user', 'start easy user', 'start user easy', 'start user medium',
                  'start medium user', 'start easy medium', 'start medium easy', 'start medium medium',
                  'start user hard', 'start hard user', 'start hard hard'] # List of valid parameters
    if len(user_input) != 3:
        print('Bad parameters!')
        return True
    elif not input_command in parameters :
        print('Bad parameters!')
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

    board[x][y] = last_move
    change_last_move()

def change_last_move():
    global last_move, previous_move
    previous_move = last_move
    if last_move == 'X':
        last_move = 'O'
    else:
        last_move = 'X'
def random_computer_move():
    while True:
        x = random.randint(0, 2)
        y = random.randint(0, 2)

        if board[x][y] != ' ':
            continue

        board[x][y] = last_move
        break


def make_center_move():
    """Make a move in the center of the board"""
    if board[1][1] =='':
        board[1][1] = last_move
        return True


def computer_move(mode):
    if mode == 'easy':
        random_computer_move()
    elif mode == 'medium':
        medium_move(mode)
    elif mode == 'hard':
        best_score = float('-inf')
        best_move = None
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = last_move
                    score = minimax(board, 0, False)
                    board[i][j] = ' '
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        if best_move:
            board[best_move[0]][best_move[1]] = last_move
    print(f'Making move level "{mode}"')
    change_last_move()

def medium_move(mode):
    global board
    moved = False
    dia_1 = [board[0][0], board[1][1], board[2][2]]
    dia_2 = [board[0][2], board[1][1], board[2][0]]
    if dia_1.count(previous_move) == 2:
        if ' ' in dia_1:
            num = dia_1.index(' ')
            if num == 0:
                board[0][0] = last_move
            elif num == 1:
                board[1][1] = last_move
            else:
                board[2][2] = last_move
            dia_1.clear()
            return
    if dia_2.count(previous_move) == 2:
        if ' ' in dia_2:
            num = dia_2.index(' ')
            if num == 0:
                board[0][2] = last_move
            elif num == 1:
                board[1][1] = last_move
            else:
                board[2][0] = last_move
            dia_2.clear()
            return
    else:
        for i in range(3):
            temp = []
            coord = []
            col = []
            col_coord = []
            for j in range(3):
                temp.append(board[i][j])  # check rows
                coord.append([i, j])  # add coordinates
                col.append(board[j][i])  # check columns
                col_coord.append([j, i])  # add coordinates

            if temp.count(previous_move) == 2:
                if ' ' in temp:
                    for el in temp:
                        if el == ' ':
                            index = temp.index(el)
                            x = coord[index][0]
                            y = coord[index][0]
                            board[x][y] = last_move
                            temp.clear()
                            coord.clear()
                            moved = True
                            break
                    break

            if col.count(previous_move) == 2:
                if ' ' in col:
                    for el in col:
                        if el == ' ':
                            index = col.index(el)
                            x = col_coord[index][0]
                            y = col_coord[index][1]
                            board[x][y] = last_move
                            col.clear()
                            coord.clear()
                            moved = True
                            break
                    break
    if not moved:
        random_computer_move()


def minimax(board, depth, is_maximizing):
    result = check_winner()
    if result == last_move:
        return 10 - depth
    elif result == previous_move:
        return depth - 10
    elif result == 'tie':
        return 0
    
    if is_maximizing:
        best_score = float('-inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = last_move
                    score = minimax(board, depth + 1, False)
                    board[i][j] = ' '
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = previous_move
                    score = minimax(board, depth + 1, True)
                    board[i][j] = ' '
                    best_score = min(score, best_score)
        return best_score

def check_winner():
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != ' ':
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != ' ':
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] != ' ':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != ' ':
        return board[0][2]
    if all(board[i][j] != ' ' for i in range(3) for j in range(3)):
        return 'tie'
    return None

def make_winning_move():
    return check_and_make_move(last_move)

def block_opponent_win():
    return check_and_make_move(previous_move)

def check_and_make_move(player):
    for i in range(3):
        if check_line(board[i], player) or check_line([board[j][i] for j in range(3)], player):
            return True
    if check_line([board[i][i] for i in range(3)], player) or check_line([board[i][2-i] for i in range(3)], player):
        return True
    return False

def check_line(line, player):
    if line.count(player) == 2 and ' ' in line:
        idx = line.index(' ')
        line[idx] = last_move
        return True
    return False

def make_strategic_move():
    # Add strategic move logic here
    # For example, try to take the center if it's free
    if board[1][1] == ' ':
        board[1][1] = last_move
        return True
    # Try to take corners
    corners = [(0,0), (0,2), (2,0), (2,2)]
    for x, y in corners:
        if board[x][y] == ' ':
            board[x][y] = last_move
            return True
    return False

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
    global last_move
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
        elif sp[1] in ('easy', 'medium', 'hard') and sp[2] in ('easy', 'medium','hard'):
            while True:
                if index == 1:
                    computer_move(sp[1])
                else:
                    computer_move(sp[2])
                game_state()
                stop = winner_state()
                if stop:
                    break

        elif (sp[1] in ('easy', 'medium', 'hard') and sp[2] == 'user') or (sp[1] == 'user' and sp[2] in ('easy','medium', 'hard')) :
            if sp[1] == 'user':
                sp[1] = sp[2]
                index = 0

            while True:
                if index == 0:
                    coordinates = input('Enter the coordinates: ')
                    coord = check_space(coordinates)  # check space if valid
                    place_move(coord)
                    index = 1
                else:
                    computer_move(sp[1])
                    index = 0
                game_state()
                stop = winner_state()  # check state after we place a move
                if stop:
                    break
        board.clear()
        change_last_move()
        index = 1
        last_move = 'X'
game()