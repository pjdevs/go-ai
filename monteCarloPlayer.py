# -*- coding: utf-8 -*-
''' This is the alpha beta player.
'''

import random
import Goban
from playerInterface import *
from playerUtils import *

class myPlayer(PlayerInterface):
    '''
    An implementation of the Alpha Beta player.
    '''

    def __init__(self):
        self._board = Goban.Board()
        self._mycolor = None
        self._opponent = None
        self._turn = 0

    def getPlayerName(self):
        return "Monte Carlo"

    def getPlayerMove(self):
        if self._board.is_game_over():
            print("Referee told me to play but the game is over!")
            return "PASS"

        move = self.find_best_move()

        self._board.push(move)
        self._turn += 1

        return Goban.Board.flat_to_name(move)

    def playOpponentMove(self, move: str):
        self._board.push(Goban.Board.name_to_flat(move))
        self._turn += 1

    def newGame(self, color: Goban.Board):
        self._mycolor = color
        self._opponent = Goban.Board.flip(color)

    def endGame(self, winner: int):
        if self._mycolor == winner:
            print(self.getPlayerName(), "won!!!")
        else:
            print(self.getPlayerName(), "lost :(!!")

    def find_best_move(self, nb_try=50) -> int:
        """Find the best move using Monte Carlo method.

        Returns:
            int: The best evaluated move
        """

        is_black = self._mycolor == Goban.Board._BLACK
        best_score = -math.inf if is_black else math.inf 
        best_move = None
        legal_moves = self._board.weak_legal_moves()


        if self._turn < 40:
            valid = False
            while not valid:
                move = random.choice(legal_moves)
                valid = self._board.push(move)
                self._board.pop()

            return move

        for move in legal_moves:
            valid = self._board.push(move)

            if not valid:
                self._board.pop()
                continue
            
            move_score = 0

            for _ in range(nb_try):
                move_score += random_game(self._board)
            
            self._board.pop()
            move_score /= nb_try

            if (move_score > best_score and is_black) or (move_score < best_score and not is_black):
                best_score = move_score
                best_move = move

        return best_move
