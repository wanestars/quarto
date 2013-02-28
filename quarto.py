# Sean Straw

from quarto_interface import *
from quarto_player import *
from quarto_state import *
from quarto_network import *

def quarto():
    #Main Program Loop
    while not (user_wants_to_stop_quarto()):
        
        #Basic data setup and class assignment
        player_1 = GamePlayer()
        player_1.player_num = "1"
        player_2 = GamePlayer()
        player_2.player_num = "2"
        game_state = GameState()
        game_status = GameStatus.PLAYING

        #Sets up next game and resets data.
        game_state.reset()
        toggle_player_turns = 1
        turn_player = player_1
        get_players_info(player_1, player_2)
        display_game_state(game_state)
        
        #Main Game Loop
        while game_status == GameStatus.PLAYING:
            
            # Move Loop
            while True:
                [move, game_status] = turn_player.get_move(game_state)
                if game_status != GameStatus.PLAYING: 
                    break
                [move_check, game_status] = check_move(game_state,move)
                if move_check == MoveStatus.LEGAL_MOVE:
                    make_move_and_display(game_state, move)
                    break
                else:
                    display_game_state(game_state)
                    signal_bad_move(move, move_check, turn_player)      
            
            toggle_player_turns = -toggle_player_turns
            if toggle_player_turns == 1:
                turn_player = player_1
            else:
                turn_player = player_2

        signal_end_of_game(game_status, game_state, player_1, player_2, turn_player)

quarto()
