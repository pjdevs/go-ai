# -*- coding: utf-8 -*-
''' This is the alpha beta player.
'''

import random
import sys
from time import perf_counter
import Goban
from playerInterface import *
from boardUtils import *


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
        return "Alpha-Beta with Monte-Carlo"

    def getPlayerMove(self):
        if self._board.is_game_over():
            print("Referee told me to play but the game is over!")
            return "PASS"

        move = self.find_best_move_iterative()

        self._board.push(move)
        self._turn += 1

        return Goban.Board.flat_to_name(move)

    def playOpponentMove(self, move: str):
        self._board.push(Goban.Board.name_to_flat(move))
        self._turn += 1

    def newGame(self, color: int):
        self._mycolor = color
        self._opponent = Goban.Board.flip(color)

        print(self.getPlayerName(), "is", self._board.player_name(color))

    def endGame(self, winner: int):
        if self._mycolor == winner:
            print("Alpha Beta won!!!")
        else:
            print("Alpha Beta lost :(!!")

    def find_best_move_iterative(self, total_time=5.0) -> int:
        """Find the best move in a maximum of `total_time` seconds using iterative deepening with alpha-beta.

        Returns:
            int: The best evaluated move
        """

        is_black = self._mycolor == Goban.Board._BLACK
        best_score = -math.inf if is_black else math.inf 
        best_move = self._board.name_to_flat("PASS")
        legal_moves = self._board.weak_legal_moves()
        max_depth = 0
        elapsed_time = 0.0

        random.shuffle(legal_moves)

        while 50 * elapsed_time < total_time:
            sys.stderr.write(f"Go depth = {max_depth}\n")
            t = perf_counter()

            for move in legal_moves:
                valid = self._board.push(move)

                if not valid:
                    self._board.pop()
                    continue

                move_score = alpha_beta_monte_carlo(self._board, max_depth=max_depth, maximizing=is_black, p=0.0001 * max_depth * 0.5 * (self._turn / 10), nb_try=100)
                self._board.pop()

                if (move_score > best_score and is_black) or (move_score < best_score and not is_black):
                    best_score = move_score
                    best_move = move

            depth_time = perf_counter() - t
            elapsed_time += depth_time
            sys.stderr.write(f"Depth {max_depth} done in {depth_time}s\nTotal elasped time = {elapsed_time}s\n")
            max_depth += 1

        return best_move