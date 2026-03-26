import sys
import math


# GLOBALS


nodes_no_prune = 0

nodes_prune = 0
alpha_cuts = 0
beta_cuts = 0

nodes_killer = 0
killer_alpha_cuts = 0
killer_beta_cuts = 0
killer_moves = {}

rotation_hits = 0
transposition = {}

# BOARD UTILITIES


def print_board(board):
    for i in range(0, 9, 3):
        print("".join(board[i:i+3]))

def check_winner(board):
    wins = [(0,1,2),(3,4,5),(6,7,8),
            (0,3,6),(1,4,7),(2,5,8),
            (0,4,8),(2,4,6)]
    for i,j,k in wins:
        if board[i] == board[j] == board[k] and board[i] != '_':
            return board[i]
    return None

def terminal(board):
    return check_winner(board) or '_' not in board

def utility(board):
    w = check_winner(board)
    if w == 'X': return 1
    if w == 'O': return -1
    return 0

def get_turn(board):
    return 'X' if board.count('X') == board.count('O') else 'O'

def get_moves(board):
    return [i for i in range(9) if board[i] == '_']

def apply_move(board, move, player):
    b = board.copy()
    b[move] = player
    return b


# ROTATION


def rotate90(b):
    return [b[6],b[3],b[0],
            b[7],b[4],b[1],
            b[8],b[5],b[2]]

def rotate180(b):
    return rotate90(rotate90(b))

def rotate270(b):
    return rotate90(rotate180(b))

def canonical(board):
    global rotation_hits
    rotations = [
        tuple(board),
        tuple(rotate90(board)),
        tuple(rotate180(board)),
        tuple(rotate270(board))
    ]
    best = min(rotations)
    if best in transposition:
        rotation_hits += 1
    return best


# MINIMAX


def minimax(board, is_max):
    global nodes_no_prune

    if terminal(board):
        return utility(board)

    if is_max:
        v = -math.inf
        for m in get_moves(board):
            nodes_no_prune += 1
            v = max(v, minimax(apply_move(board, m, 'X'), False))
        return v
    else:
        v = math.inf
        for m in get_moves(board):
            nodes_no_prune += 1
            v = min(v, minimax(apply_move(board, m, 'O'), True))
        return v

# ----------------------------------------
# ALPHA-BETA
# ----------------------------------------

def alphabeta(board, alpha, beta, is_max):
    global nodes_prune, alpha_cuts, beta_cuts

    if terminal(board):
        return utility(board)

    if is_max:
        v = -math.inf
        for m in get_moves(board):
            nodes_prune += 1
            v = max(v, alphabeta(apply_move(board, m, 'X'), alpha, beta, False))
            alpha = max(alpha, v)

            if alpha >= beta:
                alpha_cuts += 1
                print_board(board)
                print("Alpha cut")
                break
        return v
    else:
        v = math.inf
        for m in get_moves(board):
            nodes_prune += 1
            v = min(v, alphabeta(apply_move(board, m, 'O'), alpha, beta, True))
            beta = min(beta, v)

            if beta <= alpha:
                beta_cuts += 1
                print_board(board)
                print("Beta cut")
                break
        return v


# KILLER


def alphabeta_killer(board, alpha, beta, is_max, depth):
    global nodes_killer, killer_alpha_cuts, killer_beta_cuts

    if terminal(board):
        return utility(board)

    moves = get_moves(board)

    if depth in killer_moves and killer_moves[depth] in moves:
        moves.remove(killer_moves[depth])
        moves.insert(0, killer_moves[depth])

    if is_max:
        v = -math.inf
        for m in moves:
            nodes_killer += 1
            v = max(v, alphabeta_killer(apply_move(board, m, 'X'), alpha, beta, False, depth+1))
            alpha = max(alpha, v)

            if alpha >= beta:
                killer_alpha_cuts += 1
                killer_moves[depth] = m
                print_board(board)
                print("Alpha cut")
                break
        return v
    else:
        v = math.inf
        for m in moves:
            nodes_killer += 1
            v = min(v, alphabeta_killer(apply_move(board, m, 'O'), alpha, beta, True, depth+1))
            beta = min(beta, v)

            if beta <= alpha:
                killer_beta_cuts += 1
                killer_moves[depth] = m
                print_board(board)
                print("Beta cut")
                break
        return v


# ROTATION KILLER


def alphabeta_rotation(board, alpha, beta, is_max, depth):
    global nodes_killer, killer_alpha_cuts, killer_beta_cuts

    key = canonical(board)
    if key in transposition:
        return transposition[key]

    if terminal(board):
        val = utility(board)
        transposition[key] = val
        return val

    moves = get_moves(board)

    if depth in killer_moves and killer_moves[depth] in moves:
        moves.remove(killer_moves[depth])
        moves.insert(0, killer_moves[depth])

    if is_max:
        v = -math.inf
        for m in moves:
            nodes_killer += 1
            v = max(v, alphabeta_rotation(apply_move(board, m, 'X'), alpha, beta, False, depth+1))
            alpha = max(alpha, v)

            if alpha >= beta:
                killer_alpha_cuts += 1
                killer_moves[depth] = m
                print_board(board)
                print("Alpha cut")
                break
        transposition[key] = v
        return v
    else:
        v = math.inf
        for m in moves:
            nodes_killer += 1
            v = min(v, alphabeta_rotation(apply_move(board, m, 'O'), alpha, beta, True, depth+1))
            beta = min(beta, v)

            if beta <= alpha:
                killer_beta_cuts += 1
                killer_moves[depth] = m
                print_board(board)
                print("Beta cut")
                break
        transposition[key] = v
        return v


# MAIN


def main():
    global nodes_no_prune, nodes_prune, nodes_killer
    global alpha_cuts, beta_cuts, killer_alpha_cuts, killer_beta_cuts
    global rotation_hits, transposition, killer_moves

   
    if len(sys.argv) < 2:
        print("Usage: python HW_4.py BOARD_STRING")
        return

    board = list(sys.argv[1])
    while len(board) < 9:
        board.append('_')

    turn = get_turn(board)

    # ----------------------------
    print("Running without alpha-beta pruning")
    r1 = minimax(board, turn == 'X')
    print("Game Result:", r1)
    print("Moves considered without alpha-beta pruning:", nodes_no_prune)
    print("-----------------------------------------")

    # ----------------------------
    print("Running with alpha-beta pruning")
    print_board(board)

    r2 = alphabeta(board, -math.inf, math.inf, turn == 'X')

    print("Game Result:", r2)
    print("Moves considered with alpha-beta pruning:", nodes_prune)
    print("Alpha cuts:", alpha_cuts)
    print("Beta cuts:", beta_cuts)
    print("-----------------------------------------")

    # RESET
    nodes_killer = 0
    killer_alpha_cuts = 0
    killer_beta_cuts = 0
    killer_moves.clear()

    # ----------------------------
    print("Running with the killer heuristic")
    print_board(board)

    r3 = alphabeta_killer(board, -math.inf, math.inf, turn == 'X', 0)

    print("Game Result:", r3)
    print("Moves considered with alpha-beta pruning:", nodes_killer)
    print("Alpha cuts:", killer_alpha_cuts)
    print("Beta cuts:", killer_beta_cuts)
    print("-----------------------------------------")

    # RESET
    nodes_killer = 0
    killer_alpha_cuts = 0
    killer_beta_cuts = 0
    rotation_hits = 0
    killer_moves.clear()
    transposition.clear()

    # ----------------------------
    print("Running with the killer heuristic and using rotation invariance.")
    print_board(board)

    r4 = alphabeta_rotation(board, -math.inf, math.inf, turn == 'X', 0)

    print("Game Result:", r4)
    print("Moves considered with alpha-beta pruning:", nodes_killer)
    print("Alpha cuts:", killer_alpha_cuts)
    print("Beta cuts:", killer_beta_cuts)
    print("Rotation invariance invoked:", rotation_hits)

    # ----------------------------
    if not (r1 == r2 == r3 == r4):
        print("ERROR: inconsistent results")

# ----------------------------------------

if __name__ == "__main__":
    main()
