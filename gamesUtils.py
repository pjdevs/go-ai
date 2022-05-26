import json
import random
import Goban


class ProGames:
    _GAMES_PATH = "games.json"
    _games = None

    def __init__(self, board: Goban.Board, color: int) -> None:
        self._color = color
        self._game = None
        self._board = board

        if ProGames._games is None:
            f = open(ProGames._GAMES_PATH)
            ProGames._games = json.loads(f.read())
            f.close()

    def load_random_winning_game(self):
        me = "W" if self._color == 2 else "B"
        game = {"winner": "B" if self._color == 2 else "W"}
        
        while game["winner"] != me:
            game = random.choice(ProGames._games)

        self._game = game

    def get_move(self, turn: int):
        if self._game is None:
            return None

        move = None
        index = 2 * turn + self._color - 1
        
        if index < len(self._game):
            move = self._board.name_to_flat(self._game["moves"][index])
        else:
            return None
        
        valid = self._board.push(move)
        self._board.pop()

        if valid:
            return move
        else:
            return None


