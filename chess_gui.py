import tkinter as tk
from tkinter import messagebox
import chess
import os
from PIL import Image, ImageTk


# --- AI Functions ---
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

def evaluate_board(board):
    score = 0
    for piece in board.piece_map().values():
        value = piece_value(piece)
        score += value if piece.color == chess.WHITE else -value
    return score

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
                break
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
                break
        return min_eval

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

# --- GUI Class ---
class ChessApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Chess Game")

        self.board = chess.Board()
        self.square_size = 64  # <-- Define square size before loading images

        self.canvas = tk.Canvas(root, width=8*self.square_size, height=8*self.square_size)
        self.canvas.pack()

        self.images = {}
        self.load_images()  # <-- Now this is safe
        

        self.square_size = 65
        self.selected_square = None
        self.play_vs_ai = False

        self.ask_mode()

        self.canvas.bind("<Button-1>", self.on_click)
        self.draw_board()
        self.draw_pieces()

    def ask_mode(self):
        response = messagebox.askquestion("Choose Mode", "Do you want to play against the computer?")
        self.play_vs_ai = response == "yes"

    def load_images(self):
        piece_names = [
            'black-bishop', 'black-king', 'black-knight', 'black-pawn',
            'black-queen', 'black-rook', 'white-bishop', 'white-king',
            'white-knight', 'white-pawn', 'white-queen', 'white-rook'
        ]
        for name in piece_names:
            img = Image.open(f"images/{name}.png")
            

            img = img.resize((self.square_size, self.square_size), Image.Resampling.LANCZOS)

            self.images[name] = ImageTk.PhotoImage(img)


    def draw_board(self):
        color1 = "#f0d9b5"
        color2 = "#b58863"

        for row in range(8):
            for col in range(8):
                x1 = col * self.square_size
                y1 = row * self.square_size
                x2 = x1 + self.square_size
                y2 = y1 + self.square_size
                color = color1 if (row + col) % 2 == 0 else color2
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

    def draw_pieces(self):
        self.canvas.delete("piece")
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                row = 7 - (square // 8)
                col = square % 8
                color = 'white' if piece.color == chess.WHITE else 'black'
                piece_type = piece.piece_type
                type_map = {
                    chess.PAWN: "pawn",
                    chess.KNIGHT: "knight",
                    chess.BISHOP: "bishop",
                    chess.ROOK: "rook",
                    chess.QUEEN: "queen",
                    chess.KING: "king"
                }
                img_key = f"{color}-{type_map[piece_type]}"
                self.canvas.create_image(col * self.square_size, row * self.square_size,
                                        anchor=tk.NW, image=self.images[img_key], tags="piece")


    def on_click(self, event):
        col = event.x // self.square_size
        row = 7 - (event.y // self.square_size)
        square = chess.square(col, row)

        if self.selected_square is None:
            piece = self.board.piece_at(square)
            if piece and piece.color == self.board.turn:
                self.selected_square = square
        else:
            # Check if this move is a promotion
            move = None
            from_square = self.selected_square
            to_square = square
            piece = self.board.piece_at(from_square)

            # If pawn moves to last rank -> promotion needed
            if piece.piece_type == chess.PAWN and (chess.square_rank(to_square) == 0 or chess.square_rank(to_square) == 7):
                promotion_piece = self.ask_promotion()
                if promotion_piece:
                    move = chess.Move(from_square, to_square, promotion=promotion_piece)
            else:
                move = chess.Move(from_square, to_square)

            if move and move in self.board.legal_moves:
                self.board.push(move)
                self.selected_square = None
                self.draw_board()
                self.draw_pieces()

                if self.board.is_game_over():
                    self.show_result()
                    return

                if self.play_vs_ai and self.board.turn == chess.BLACK:
                    self.root.after(500, self.ai_move)
            else:
                self.selected_square = None

    def ask_promotion(self):
        # Popup to ask the user which piece to promote to
        promotion_window = tk.Toplevel(self.root)
        promotion_window.title("Choose Promotion")

        promotion_piece = {'piece': None}

        def select(piece_type):
            promotion_piece['piece'] = piece_type
            promotion_window.destroy()

        # Buttons for promotion options
        tk.Label(promotion_window, text="Promote to:").pack()

        tk.Button(promotion_window, text="Queen", command=lambda: select(chess.QUEEN)).pack(fill='x')
        tk.Button(promotion_window, text="Rook", command=lambda: select(chess.ROOK)).pack(fill='x')
        tk.Button(promotion_window, text="Bishop", command=lambda: select(chess.BISHOP)).pack(fill='x')
        tk.Button(promotion_window, text="Knight", command=lambda: select(chess.KNIGHT)).pack(fill='x')

        promotion_window.grab_set()  # Modal window
        self.root.wait_window(promotion_window)

        return promotion_piece['piece']


    def ai_move(self):
        move = best_move(self.board, 3)
        if move:
            self.board.push(move)
            self.draw_board()
            self.draw_pieces()
            if self.board.is_game_over():
                self.show_result()

    def show_result(self):
        result = self.board.result()
        messagebox.showinfo("Game Over", f"Result: {result}")
        self.root.quit()

# --- Run App ---
if __name__ == "__main__":
    root = tk.Tk()
    app = ChessApp(root)
    root.mainloop()
