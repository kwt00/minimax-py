from math import inf
from random import choice
import platform
import time
from os import system

human = -1
computer = 1
board = [[0,0,0], [0,0,0], [0,0,0]]

def wins(state, player):
    win_state = [
        [state[0][0], state[0][1], state[0][2]],
        [state[1][0], state[1][1], state[1][2]],
        [state[2][0], state[2][1], state[2][2]],
        [state[0][0], state[1][0], state[2][0]],
        [state[0][1], state[1][1], state[2][1]],
        [state[0][2], state[1][2], state[2][2]],
        [state[0][0], state[1][1], state[2][2]],
        [state[2][0], state[1][1], state[0][2]]
    ]
    if [player,player,player] in win_state:
        return True 
    else: 
        return False

def evaluate(state):
    if wins(state,computer):
        score = 1
    elif wins(state,human):
        score = -1
    else:
        score = 0
    return score

def gameOver(state):
    return wins(state,human) or wins(state,computer)

def emptyCells(state):
    cells = []
    for x, row in enumerate(state):
        for y, cell in enumerate(row):
            if cell == 0:
                cells.append([x,y])
    return cells

def validMove(x,y):
    if [x,y] in emptyCells(board):
        return True
    else:
        return False

def setMove(x,y,player):
    if validMove(x,y):
        board[x][y] = player
        return True
    else:
        return False

def minimax(state,depth,player):
    if player == computer:
        best = [-1,-1,-inf]
    else:
        best = [-1,-1, inf]
    if depth == 0 or gameOver(state):
        score = evaluate(state)
        return [-1,-1,score]
    for cell in emptyCells(state):
        x,y = cell[0],cell[1]
        state[x][y] = player
        score = minimax(state,depth-1,-player)
        state[x][y] = 0
        score[0], score[1] = x,y
        if player == computer:
            if score[2] > best[2]:
                best = score
        else:
            if score[2] < best[2]:
                best = score
    return best

def cleaner():
    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')

def render(state,c_choice,h_choice):
    characters = {-1:h_choice,1:c_choice,0:" "}
    stringLine = '---------------'
    print('\n' + stringLine)
    for row in state:
        for cell in row:
            symbol = characters[cell]
            print(f"| {symbol} |", end="")
        print('\n' + stringLine)

def aiturn(c_choice,h_choice):
    depth = len(emptyCells(board))
    if(depth == 0 or gameOver(board)):
        return
    cleaner()
    print(f"computer turn [{'5'}]")
    render(board,c_choice,h_choice)
    if(depth == 9):
        x = choice([0,1,2])
        y = choice([0,1,2])
    else:
        move = minimax(board,depth,computer)
        x,y = move[0],move[1]
    setMove(x,y,computer)
    time.sleep(1)

def humanturn(c_choice,h_choice):
    depth = len(emptyCells(board))
    if(depth == 0 or gameOver(board)):
        return
    move = -1
    moves = {
        1: [0,0], 2: [0,1], 3: [0,2],
        4: [1,0], 5: [1,1], 6: [1,2],
        7: [2,0], 8: [2,1], 9: [2,2]
    }
    cleaner()
    print(f"human turn [{h_choice}]")
    render(board,c_choice,h_choice)
    while move < 1 or move > 9:
        try:
            move = int(input('Enter a number between 1-9 to make your move'))
            coordinate = moves[move]
            can_move = setMove(coordinate[0], coordinate[1], human)
            if not can_move:
                print('Bad move!')
                move = -1
        except(EOFError,KeyboardInterrupt):
            print('Bye')
            exit()
        except(KeyError,ValueError):
            print("Bad choice!")

def main():
    cleaner()
    h_choice = ''
    c_choice = ''
    first = ''
    while h_choice != 'O' and h_choice != 'X':
        try:
            print('')
            h_choice = input('Choose X or O: ').upper()
        except(EOFError,KeyboardInterrupt):
            print('Bye')
            exit()
        except(KeyError,ValueError):
            print("Bad choice!")
    if h_choice == 'X':
        c_choice = 'O'
    else:
        c_choice = 'X'
        h_choice = 'O'
    cleaner()
    while first != 'Y' and first != 'N':
        try:
            first = input('Would you like to go first? Y/N').upper()
        except(EOFError,KeyboardInterrupt):
            print('Bye')
            exit()
        except(KeyError,ValueError):
            print("Bad choice!")
    while len(emptyCells(board)) > 0 and not gameOver(board):
        if first == 'N':
            aiturn(c_choice,h_choice)
            first = ''
        humanturn(c_choice,h_choice)
        aiturn(c_choice,h_choice)
    if wins(board, human):
        cleaner()
        print(f"human turn [{h_choice}]")
        render(board,c_choice,h_choice)
        print('You beat the computer!')
    elif wins(board, computer):
        cleaner()
        print(f"computer turn [{c_choice}]")
        render(board,c_choice,h_choice)
        print('You got clapped!')
    else:
        cleaner()
        render(board,c_choice,h_choice)
        print('Draw!')
    exit()

if __name__ == "__main__":
    main()
