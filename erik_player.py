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

        #++++++++++
        self.neighbors = []
        #++++++++++

     #+++++++++++++++++++
    def _get_neighbors(self, fcoord):
        x, y = self._board.unflatten(fcoord)
        neighbors = [] 
        for i in range(4):
            for j in range(4):
                if((i!=2) and (j!=2)):
                    neighbors.append((x-2+i,y-2+j))
        neighbors = ((x+1, y), (x+1,y+1), (x-1, y), (x, y+1), (x, y-1))
        return [self._board.flatten(c) for c in neighbors if self._board._isOnBoard(c[0], c[1])]


    def update_neighbors(self, move):
        '''
            Permet de stocker dans self.neighbors l'ensembles des cases au voisinage des pions posés sur lesquels on peut jouer
            On peut donc jouer sur toute case de self neighbors
        '''
        if(move == "PASS"):
            return 0
        temp = self._get_neighbors(move)
        for i in range(len(temp)):
            self.neighbors.append(temp[i])
        self.neighbors = list(set(self.neighbors) & set(self._board.legal_moves()))

    #+++++++++++++++++++

    def getPlayerName(self):
        return "Alpha-Beta with Monte-Carlo"

    def getPlayerMove(self):
        if self._board.is_game_over():
            print("Referee told me to play but the game is over!")
            return "PASS"

        move = self.find_best_move_iterative()

        self._board.push(move)
        self.update_neighbors(move)
        self._turn += 1

        return Goban.Board.flat_to_name(move)

    def playOpponentMove(self, move: str):
        self._board.push(Goban.Board.name_to_flat(move))
        self._turn += 1
        #++++++++++
        self.update_neighbors(Goban.Board.name_to_flat(move))
        #++++++++++

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
        if( (81-len(legal_moves )<10) and (81-len(legal_moves))>2 ):
            legal_moves = self.neighbors
        
        
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