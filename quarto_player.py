# quarto game - move generators and checkers
# Sean Straw & Ari Cohen

import random  # used for creating random moves
from quarto_interface import *
from quarto_state import *
from quarto_network import *


class GamePlayer():
    HUMAN = 0
    COMPUTER = 1
    NETWORK_HOST = 2
    NETWORK_CLIENT = 3

    MAXIMIZE = 1
    MINIMIZE = -1
    
    def __init__(self):
        self.type = GamePlayer.HUMAN
        self.level = 0
        self.time_limit = 10000000

    def get_type(self):
        return self.type

    def set_level(self, level):
        self.level = level
    
    def game_over(self, game_status):
        if self.type == self.NETWORK_HOST:
            signal_host_game_over(self, game_status)
            self.connection.close()
        if self.type == self.NETWORK_CLIENT:
            signal_client_game_over(self, game_status)
    def set_type(self, new_type):
        self.type = new_type
        if self.type == GamePlayer.NETWORK_HOST:
            [self.HOST_IP, self.HOST_PORT] = get_host_information()
            self.connection = connect_to_host(self)
        elif self.type == GamePlayer.NETWORK_CLIENT:
            self.HOST_IP = '0.0.0.0'
            self.HOST_PORT = get_port_number()
            self.HOST_PORT = start_host_server(self)
            
    def get_move(self, game_state):
        if self.type == GamePlayer.HUMAN:
            return get_human_move(game_state)
        elif self.type == GamePlayer.NETWORK_HOST:
            return get_network_host_move(game_state, self.connection)
        elif self.type == GamePlayer.NETWORK_CLIENT:
            return get_network_client_move(game_state)
        else:
            return get_computer_move(game_state, self.level)

# For each player, this should set
#   1) human, computer, network
#   1a) if computer, how much time allowed and what level to play
def get_players_info(player0, player1):
    players = [player0, player1]
    data = get_players_information()
    for index in range(2):
        if data[index*2] == "h":
            players[index].set_type(GamePlayer.HUMAN)
        elif index == 0 and data[index*2] == 'n':
            players[index].set_type(GamePlayer.NETWORK_HOST)
        elif index == 1 and data[index*2] == 'n':
            players[index].set_type(GamePlayer.NETWORK_CLIENT)
        else:
            players[index].set_type(GamePlayer.COMPUTER)
            players[index].set_level((index*2)+1)
    return

def get_computer_move(game_state, level):
    if level == 1:
        return get_random_move(game_state)
    else if level == 2:
        return simple_move_test(game_state)
    else if level == 3:
        depth = len(get_good_pieces_and_squares(game_state)[0])
    return test_moves(game_state, depth, GameState.MAXIMIZE, depth)

def test_moves(game_state, depth, minimax, initial_depth):
    good_pieces, good_squares = get_good_pieces_and_squares(game_state)
    good_moves = []
    for piece in good_pieces:
        for square in good_squares:
            test_game_state = copy_game_state(game_state)
            test_move = GameMove()
            test_move.set_move(square[0],square[1],piece)
            move_state = check_move(test_game_state, test_move)
            if(move_state[1] == GameStatus.WIN):
                return [test_move, GameStatus.WIN]
            test_game_state.make_move(test_move)
            opponent_moves = test_opponent_moves(test_game_state)
            if(opponent_moves != GameStatus.WIN):
                good_moves.append(test_move)
    if(len(good_moves) != 0):
        return [random.choice(good_moves), GameStatus.PLAYING]
    else:
        notify("Well Done")
        return get_random_move(game_state)

def test_opponent_moves(game_state):
    good_pieces, good_squares = get_good_pieces_and_squares(game_state)
    test_game_state = copy_game_state(game_state)
    for piece in good_pieces:
        for square in good_squares:
            test_game_state = copy_game_state(game_state)
            test_move = GameMove()
            test_move.set_move(square[0],square[1],piece)
            move_state = check_move(test_game_state, test_move)
            if(move_state[1] == GameStatus.WIN):
                return GameStatus.WIN
    return GameStatus.PLAYING

def get_random_move(game_state):
    move = GameMove()
    good_pieces, good_squares = get_good_pieces_and_squares(game_state)
    chosen_square = random.choice(good_squares)
    if(len(good_pieces) != 0):
        chosen_piece = random.choice(good_pieces)
        move.set_move(chosen_square[0],chosen_square[1],chosen_piece)
        return [move, GameStatus.PLAYING]
    else:
        chosen_piece = -1
        move.set_move(chosen_square[0],chosen_square[1],chosen_piece)
        return [move, GameStatus.WIN]

def get_good_pieces_and_squares(game_state):
    avail_pieces = game_state.available_pieces
    all_squares = game_state.squares
    good_pieces = []
    good_squares = []
    for piece in range(len(avail_pieces)):
        if(avail_pieces[piece]):
            good_pieces.append(piece)
        if(all_squares[piece] == GameState.EMPTY):
            good_squares.append([piece/4, piece%4])
    return good_pieces, good_squares
