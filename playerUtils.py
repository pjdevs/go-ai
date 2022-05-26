import math
import random
import sys
import Goban

def evaluate_board_score(b: Goban.Board) -> float:
    """Evaluate the board based on its score

    Returns:
        float: The board score.
    """

    score = 0.2 * b.diff_stones_board() + b._capturedWHITE - 5 * b._capturedBLACK

    if b.is_game_over():
        match b.result():
            case "1-0":
                score = -1000000000
            case "0-1":
                score = 1000000000

    return score


def alpha_beta(b: Goban.Board, max_depth=3, alpha=-math.inf, beta=math.inf, maximizing=True, depth=0) -> float:
    """Alpha-Beta

    Returns:
        float: The score of the current board.
    """

    if depth >= max_depth or b.is_game_over():
        return evaluate_board_score(b)

    if maximizing:
        max_evaluation = -math.inf

        for move in  b.weak_legal_moves():
            valid = b.push(move)
            if not valid:
                b.pop()
                continue

            evaluation = alpha_beta(b, max_depth, alpha, beta, False, depth + 1)
            b.pop()

            max_evaluation = max(max_evaluation, evaluation)
            alpha = max(alpha, evaluation)

            if alpha >= beta:
                break

        return max_evaluation
    else:
        min_evaluation = math.inf

        for move in b.weak_legal_moves():
            valid = b.push(move)
            if not valid:
                b.pop()
                continue

            evaluation = alpha_beta(b, max_depth, alpha, beta, True, depth + 1)
            b.pop()

            min_evaluation = min(min_evaluation, evaluation)
            beta = min(beta, evaluation)

            if alpha >= beta:
                break

        return min_evaluation

def random_game(b: Goban.Board) -> float:
    """
    Go to the end of the move tree and return 1 for win of `color`.
    """

    if b.is_game_over():
        return evaluate_board_score(b)

    moves = b.weak_legal_moves()
    move = None
    valid = False

    while not valid:
        move = random.choice(moves)
        valid = b.push(move)
        if not valid:
            b.pop()
    
    win = random_game(b)
    
    b.pop()

    return win

def monte_carlo(b: Goban.Board, nb_try: int):
    """
    Returns board score on average according to random games.
    """

    board_score = 0

    for _ in range(nb_try):
        board_score += random_game(b)
        
    board_score /= nb_try

    return board_score

def alpha_beta_monte_carlo(b: Goban.Board, max_depth=0, alpha=-math.inf, beta=math.inf, maximizing=True, depth=0, p=0.2, nb_try=100) -> float:
    """Alpha-Beta with Monte Carlo

    Returns:
        float: The score of the current board.
    """

    if depth >= max_depth or b.is_game_over():
        r = random.Random().uniform(0.0, 1.0) 
        if r <= p:
            return monte_carlo(b, nb_try)
        else:
            return evaluate_board_score(b)

    moves = b.weak_legal_moves()
    random.shuffle(moves)

    if maximizing:
        max_evaluation = -math.inf

        for move in moves:
            valid = b.push(move)
            if not valid:
                b.pop()
                continue

            evaluation = alpha_beta_monte_carlo(b, max_depth, alpha, beta, False, depth + 1, p, nb_try)
            b.pop()

            max_evaluation = max(max_evaluation, evaluation)
            alpha = max(alpha, evaluation)

            if alpha >= beta:
                break

        return max_evaluation
    else:
        min_evaluation = math.inf

        for move in moves:
            valid = b.push(move)
            if not valid:
                b.pop()
                continue

            evaluation = alpha_beta_monte_carlo(b, max_depth, alpha, beta, True, depth + 1, p, nb_try)
            b.pop()

            min_evaluation = min(min_evaluation, evaluation)
            beta = min(beta, evaluation)

            if alpha >= beta:
                break

        return min_evaluation