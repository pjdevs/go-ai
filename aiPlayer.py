# -*- coding: utf-8 -*-
''' This is the file you have to modify for the tournament. Your default AI player must be called by this module, in the
myPlayer class.

Right now, this class contains the copy of the randomPlayer. But you have to change this!
'''

import math
from unittest import mock
import Goban 
from random import choice
from playerInterface import *
import tensorflow as tf

PATH = "model.tf"

class myPlayer(PlayerInterface):
    ''' Example of a random player for the go. The only tricky part is to be able to handle
    the internal representation of moves given by legal_moves() and used by push() and 
    to translate them to the GO-move strings "A1", ..., "J8", "PASS". Easy!

    '''

    def __init__(self):
        self._board = Goban.Board()
        self._mycolor = None
        self.model = tf.keras.models.load_model(PATH)

    def evaluate_board(self):
        if self._board.is_game_over():
            if self._board.result() == "1-0":
                return -1000000000
            elif self._board.result() == "0-1":
                return 1000000000
            else:
                return 0

        res = self.model.predict(tf.constant([self._board.get_board()]))
        return res[0]

    def getPlayerName(self):
        return "AI Player"

    def getPlayerMove(self):
        if self._board.is_game_over():
            print("Referee told me to play but the game is over!")
            return "PASS"

        moves = self._board.legal_moves() # Dont use weak_legal_moves() here!
        is_black = self._mycolor == Goban.Board._BLACK
        best_move = None
        best_score = -math.inf if is_black else math.inf 

        # Try pass
        self._board.push(self._board.name_to_flat("PASS"))
        
        if len(self._board.legal_moves()) == 1 and self._board.result() == ("0-1" if is_black else "1-0"):
            return "PASS"
        
        self._board.pop()

        # Select best move
        for move in moves:
            self._board.push(move)
            move_score = self.evaluate_board()
            self._board.pop()

            if (move_score > best_score and is_black) or (move_score < best_score and not is_black):
                best_score = move_score
                best_move = move

        self._board.push(best_move)

        return Goban.Board.flat_to_name(best_move) 

    def playOpponentMove(self, move):
        self._board.push(Goban.Board.name_to_flat(move)) 

    def newGame(self, color):
        self._mycolor = color
        self._opponent = Goban.Board.flip(color)

    def endGame(self, winner):
        if self._mycolor == winner:
            print("I won!!!")
        else:
            print("I lost :(!!")



