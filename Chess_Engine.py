import chess
import random

# Function to assign values to pieces
def piece_value(piece):
    if piece.piece_type == chess.PAWN:
        return 1
    elif piece.piece_type == chess.KNIGHT or piece.piece_type == chess.BISHOP:
        return 3
    elif piece.piece_type == chess.ROOK:
        return 5
    elif piece.piece_type == chess.QUEEN:
        return 9
    elif piece.piece_type == chess.KING:
        return 1000
    return 0

# Function to evaluate the board (positive = advantage white, negative = advantage black)
def evaluate_board(board):
    score = 0
    for piece in board.piece_map().values():
        value = piece_value(piece)
        score += value if piece.color == chess.WHITE else -value
    return score

# Minimax algorithm with alpha-beta pruning
def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    if maximizing_player:
        max_eval = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # Beta cutoff
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break  # Alpha cutoff
        return min_eval

# Function to find the best move using minimax
def best_move(board, depth):
    best = None
    max_eval = float('-inf')
    alpha = float('-inf')
    beta = float('inf')

    for move in board.legal_moves:
        board.push(move)
        eval = minimax(board, depth - 1, alpha, beta, False)
        board.pop()

        if eval > max_eval:
            max_eval = eval
            best = move

        alpha = max(alpha, eval)

    return best

# Main function to play a game: AI (White) vs User (Black)
def play_game():
    board = chess.Board()
    depth = 3  # Search depth

    while not board.is_game_over():
        print("\nCurrent Board:")
        print(board)

        # AI's move (White)
        print("\nAI's Move:")
        move = best_move(board, depth)
        board.push(move)
        print(f"AI played: {move}")

        if board.is_game_over():
            break

        print("\nYour Move (Black):")
        user_move = input("Enter your move in UCI format (e.g., e2e4): ")

        try:
            move_obj = chess.Move.from_uci(user_move)
            if move_obj in board.legal_moves:
                board.push(move_obj)
            else:
                print("❌ Invalid move. Try again.")
        except:
            print("❌ Invalid format. Try again.")

    print("\n🏁 Game Over!")
    print(board)
    print(f"Result: {board.result()}")

# Start the game
play_game()
