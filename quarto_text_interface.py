# quarto game - text interface
# Sean Straw & Ari Cohen

import string          
from quarto_state import *


# Gives binary of number as a string
def binary(number):
    return "{0:0>4b}".format(number)

# Makes a matrix by row and column given
def make_matrix(row, column, default_value):
    output = list()
    for x in range(row):
        temp_column = column*[default_value]
        output += [temp_column]
    return output

# Display available pieces, piece to move, and the board
def display_game_state(game_state):
    begin_name = list('SEAN')
    end_name = list('STAN')
    available_pieces = game_state.get_available_pieces()
    square_pieces = game_state.get_squares()
    current_piece = binary(game_state.get_current_piece())
    printed_pieces = make_matrix(4,4,'----')
    board = make_matrix(4,4,'----')
    # Split up pieces into nested list, [[row1],[row2]..]
    for piece in range(len(available_pieces)):
        if available_pieces[piece] == GameState.AVAILABLE:
            row_val = piece / 4
            col_val = piece % 4
            printed_pieces[row_val][col_val] = binary(piece)
    # Split up pieces into nested list, [[row1],[row2]..]
    for space in range(len(available_pieces)):
        if square_pieces[space] != GameState.EMPTY:
            row_val = space / 4
            col_val = space % 4
            board[row_val][col_val] = binary(square_pieces[space])
    # Prints out the actual board
    print ' '
    for row in range(len(printed_pieces)):
        if row == 1: # Shows current piece on one row
            print (begin_name[row] + ' ' * 4 + ' '.join(printed_pieces[row]) + # Left side
                   ' ' * 4 + current_piece + ' ' * 4 +       # Middle
                   ' '.join(board[row]) + ' ' + end_name[row])   # Right
        else:
            print (begin_name[row] + ' ' * 4 + ' '.join(printed_pieces[row]) + 
                   ' ' * 12 +  
                   ' '.join(board[row]) + ' ' + end_name[row])
    
# This combines making the move and displaying the board
# in case some animation is desired
def make_move_and_display(game_state, move):
    game_state.make_move(move)
    display_game_state(game_state)

# For each player, this should set
#   1) human, computer, network
#   1a) if computer, how much time allowed and what level to play
# Return information as text and numbers
#   This function returns either "h" or "c" as appropriate
def get_players_information():
    data = []
    for counter in range(2):
        level0 = 0
        player = raw_input('Is Player 1 human, computer, or network? (h/c/n)')
        if player == "c":
            while(True):
                level0 = raw_input('Enter Computer Level (1-3)')
                try:
                    level0 = int(level0)
                except:
                    continue
                break
        data.extend([player, level0])
    return data

def get_bound_integer_input(prompt_string, lower, upper):
    while True:
        prompt_string += ' (%i - %i): ' % (lower, upper)
        value = raw_input(prompt_string)
        try:
            value = int(value)
        except:
            print "Please enter an integer"
            continue
        if value >= lower and value <= upper:
            return value
        print "Integer must be %i-%i." % (lower, upper)        

def get_human_move(game_state):
    move = GameMove()
    row = get_bound_integer_input('Row of next move', 1, 4)
    column = get_bound_integer_input('Column of next move', 1, 4)
    next_piece = get_bound_integer_input('Piece of next move, or 0 if no pieces.', 
                                          0, 16)
    # compensate for human-computer difference
    row += -1
    column += -1
    next_piece += -1
    move.set_move(row, column, next_piece)
    return [move, GameStatus.PLAYING]

# Make an error message for various types of bad moves
#   1) ILLEGAL_MOVE - only one for now
def signal_bad_move(move, move_status, current_player):
    print "Illegal move, try again.\n"


# Signal end of game and ask if they want to play another
def signal_end_of_game(game_status, game_state, player_1,
                       player_2, current_player):
    player_1.game_over(game_state)
    player_2.game_over(game_state)
    if game_status == GameStatus.QUITTING:
        print "Game over - player quitting."
    elif game_status == GameStatus.TIE:
        print "Game over - it's a tie."
    elif game_status == GameStatus.WIN:
        print "Game over - Player "+current_player.player_num+" wins!."
    else:
        print "Game over - unknown reason"

def user_wants_to_stop_quarto():
    user_input = raw_input("Do you want to stop playing Quarto? (y/n) ")
    if user_input == "y":
        return True
    return False
    
# Allows any sort of "heads up."  Made so interface can be radically changed
def notify(string):
    print string

def get_port_number():
    while True:
        port = raw_input('Port to operate on, or 0 for random (0 is suggested)')
        try:
            return int(port)
        except:
            print "Please enter an integer."
def get_host_information():
    print "Please be careful, there's no error-checking for this section yet."
    host_ip = raw_input('What\'s the IP of the host?')
    port = int(raw_input('What\'s the port of the host?'))
    return [host_ip, port]
