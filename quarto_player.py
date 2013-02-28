# quarto game - move generators and checkers
# Sean Straw

import random  # used for creating random moves
from quarto_interface import *
from quarto_state import *
from quarto_network import *


class GamePlayer():
    HUMAN = 0
    COMPUTER = 1
    NETWORK_HOST = 2
    NETWORK_CLIENT = 3
    
    def __init__(self):
        self.type = GamePlayer.HUMAN
        self.level = 0
        self.time_limit = 10000000

    def get_type(self):
        return self.type
    
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
            return get_computer_move(game_state)

# For each player, this should set
#   1) human, computer, network
#   1a) if computer, how much time allowed and what level to play
def get_players_info(player0, player1):
    players = [player0, player1]
    data = get_players_information()
    for index in range(2):
        if data[index] == "h":
            players[index].set_type(GamePlayer.HUMAN)
        elif index == 0 and data[index] == 'n':
            players[index].set_type(GamePlayer.NETWORK_HOST)
        elif index == 1 and data[index] == 'n':
            players[index].set_type(GamePlayer.NETWORK_CLIENT)
        else:
            players[index].set_type(GamePlayer.COMPUTER)
    return

# This first version will move randomly - someday this will be level 0 play
def get_computer_move(game_state):
    available_pieces = game_state.get_available_pieces()
    squares = game_state.get_squares()
    possible_move = list()
    possible_piece = list()
    for piece in range(len(available_pieces)):
        if available_pieces[piece] == GameState.AVAILABLE:
            possible_piece.append(piece)
    for move in range(len(squares)):
        if squares[move] == GameState.EMPTY:
            possible_move.append(move)
    if len(possible_piece) == 0:
        next_piece = -1
    else:
        next_piece = random.choice(possible_piece)
    next_move = random.choice(possible_move)
    next_move_row = next_move / 4
    next_move_col = next_move % 4
    computer_move = GameMove()
    computer_move.set_move(next_move_row, next_move_col, next_piece)
    return [computer_move, GameStatus.PLAYING]
