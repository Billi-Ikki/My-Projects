# Human Vs AI chess game using Minimax Algo with Alpha beta Pruning

import tkinter as tk
from tkinter import messagebox
from abc import ABC, abstractmethod

# Move class
class Move:
    def __init__(self, from_square, to_square, piece, captured_piece=None):
        self.from_row, self.from_col = from_square
        self.to_row, self.to_col = to_square
        self.piece = piece
        self.captured_piece = captured_piece
        self.is_castling = False
        self.is_en_passant = False
        self.is_promotion = False
        self.promotion_piece = None  # 'Q', 'R', 'B', or 'N'
        
    def __str__(self):
        files = 'abcdefgh'
        ranks = '87654321'
        move_str = f"{files[self.from_col]}{ranks[self.from_row]} to {files[self.to_col]}{ranks[self.to_row]}"
        
        if self.is_promotion:
            move_str += f" (promote to {self.promotion_piece})"
        elif self.is_castling:
            move_str += " (kingside castle)" if self.to_col > self.from_col else " (queenside castle)"
        elif self.is_en_passant:
            move_str += " (en passant)"
            
        return move_str
    
    def to_algebraic(self):
        files = 'abcdefgh'
        ranks = '87654321'
        notation = f"{files[self.from_col]}{ranks[self.from_row]}{files[self.to_col]}{ranks[self.to_row]}"
        
        if self.is_promotion:
            notation += self.promotion_piece.lower()
            
        return notation
    
    @staticmethod
    def from_algebraic(algebraic, board):
        if len(algebraic) < 4:
            return None
            
        files = 'abcdefgh'
        ranks = '87654321'
        
        from_col = files.index(algebraic[0].lower()) if algebraic[0].lower() in files else -1
        from_row = ranks.index(algebraic[1]) if algebraic[1] in ranks else -1
        to_col = files.index(algebraic[2].lower()) if algebraic[2].lower() in files else -1
        to_row = ranks.index(algebraic[3]) if algebraic[3] in ranks else -1
        
        if -1 in [from_col, from_row, to_col, to_row]:
            return None
            
        piece = board.get_piece(from_row, from_col)
        if not piece:
            return None
            
        move = Move((from_row, from_col), (to_row, to_col), piece)
        
        if len(algebraic) > 4 and isinstance(piece, Pawn) and (to_row == 0 or to_row == 7):
            promotion_piece = algebraic[4].upper()
            if promotion_piece in ['Q', 'R', 'B', 'N']:
                move.is_promotion = True
                move.promotion_piece = promotion_piece
        
        return move

# Piece classes
class Piece(ABC):
    def __init__(self, color, position):
        self.color = color
        self.row, self.col = position
        self.has_moved = False
        
    @abstractmethod
    def get_valid_moves(self, board, check_check=True):
        pass
        
    def __str__(self):
        return f"{self.color} {self.__class__.__name__}"
    
    def is_move_in_bounds(self, row, col):
        return 0 <= row < 8 and 0 <= col < 8
    
    def create_move(self, board, to_row, to_col):
        return Move((self.row, self.col), (to_row, to_col), self)

class Pawn(Piece):
    def get_valid_moves(self, board, check_check=True):
        moves = []
        direction = -1 if self.color == 'white' else 1
        
        new_row = self.row + direction
        if 0 <= new_row < 8 and board.squares[new_row][self.col] is None:
            move = self.create_move(board, new_row, self.col)
            if new_row == 0 or new_row == 7:
                move.is_promotion = True
                for piece_type in ['Q', 'R', 'B', 'N']:
                    promotion_move = self.create_move(board, new_row, self.col)
                    promotion_move.is_promotion = True
                    promotion_move.promotion_piece = piece_type
                    moves.append(promotion_move)
            else:
                moves.append(move)
            
            if not self.has_moved:
                new_row = self.row + 2 * direction
                if 0 <= new_row < 8 and board.squares[new_row][self.col] is None:
                    moves.append(self.create_move(board, new_row, self.col))
        
        for col_offset in [-1, 1]:
            new_col = self.col + col_offset
            new_row = self.row + direction
            
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                piece_to_capture = board.squares[new_row][new_col]
                
                if piece_to_capture and piece_to_capture.color != self.color:
                    move = self.create_move(board, new_row, new_col)
                    if new_row == 0 or new_row == 7:
                        for piece_type in ['Q', 'R', 'B', 'N']:
                            promotion_move = self.create_move(board, new_row, new_col)
                            promotion_move.is_promotion = True
                            promotion_move.promotion_piece = piece_type
                            moves.append(promotion_move)
                    else:
                        moves.append(move)
                
                elif piece_to_capture is None:
                    last_move = board.get_last_move()
                    if last_move:
                        last_piece = board.squares[last_move.to_row][last_move.to_col]
                        if (isinstance(last_piece, Pawn) and 
                            last_piece.color != self.color and 
                            abs(last_move.from_row - last_move.to_row) == 2 and
                            last_move.to_col == new_col and 
                            last_move.to_row == self.row):
                            en_passant_move = self.create_move(board, new_row, new_col)
                            en_passant_move.is_en_passant = True
                            moves.append(en_passant_move)
        
        if check_check:
            moves = [move for move in moves if not board.would_move_cause_check(move, self.color)]
            
        return moves

class Knight(Piece):
    def get_valid_moves(self, board, check_check=True):
        moves = []
        offsets = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        
        for row_offset, col_offset in offsets:
            new_row = self.row + row_offset
            new_col = self.col + col_offset
            
            if not self.is_move_in_bounds(new_row, new_col):
                continue
                
            target_piece = board.squares[new_row][new_col]
            
            if target_piece is None or target_piece.color != self.color:
                moves.append(self.create_move(board, new_row, new_col))
        
        if check_check:
            moves = [move for move in moves if not board.would_move_cause_check(move, self.color)]
            
        return moves

class Bishop(Piece):
    def get_valid_moves(self, board, check_check=True):
        moves = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        for row_dir, col_dir in directions:
            for i in range(1, 8):
                new_row = self.row + i * row_dir
                new_col = self.col + i * col_dir
                
                if not self.is_move_in_bounds(new_row, new_col):
                    break
                    
                target_piece = board.squares[new_row][new_col]
                
                if target_piece is None:
                    moves.append(self.create_move(board, new_row, new_col))
                elif target_piece.color != self.color:
                    moves.append(self.create_move(board, new_row, new_col))
                    break
                else:
                    break
        
        if check_check:
            moves = [move for move in moves if not board.would_move_cause_check(move, self.color)]
            
        return moves

class Rook(Piece):
    def get_valid_moves(self, board, check_check=True):
        moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for row_dir, col_dir in directions:
            for i in range(1, 8):
                new_row = self.row + i * row_dir
                new_col = self.col + i * col_dir
                
                if not self.is_move_in_bounds(new_row, new_col):
                    break
                    
                target_piece = board.squares[new_row][new_col]
                
                if target_piece is None:
                    moves.append(self.create_move(board, new_row, new_col))
                elif target_piece.color != self.color:
                    moves.append(self.create_move(board, new_row, new_col))
                    break
                else:
                    break
        
        if check_check:
            moves = [move for move in moves if not board.would_move_cause_check(move, self.color)]
            
        return moves

class Queen(Piece):
    def get_valid_moves(self, board, check_check=True):
        moves = []
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        
        for row_dir, col_dir in directions:
            for i in range(1, 8):
                new_row = self.row + i * row_dir
                new_col = self.col + i * col_dir
                
                if not self.is_move_in_bounds(new_row, new_col):
                    break
                    
                target_piece = board.squares[new_row][new_col]
                
                if target_piece is None:
                    moves.append(self.create_move(board, new_row, new_col))
                elif target_piece.color != self.color:
                    moves.append(self.create_move(board, new_row, new_col))
                    break
                else:
                    break
        
        if check_check:
            moves = [move for move in moves if not board.would_move_cause_check(move, self.color)]
            
        return moves

class King(Piece):
    def get_valid_moves(self, board, check_check=True):
        moves = []
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        
        for row_dir, col_dir in directions:
            new_row = self.row + row_dir
            new_col = self.col + col_dir
            
            if not self.is_move_in_bounds(new_row, new_col):
                continue
                
            target_piece = board.squares[new_row][new_col]
            
            if target_piece is None or target_piece.color != self.color:
                moves.append(self.create_move(board, new_row, new_col))
        
        if not self.has_moved and (not check_check or not board.is_check(self.color)):
            kingside_rook = board.squares[self.row][7]
            if kingside_rook and isinstance(kingside_rook, Rook) and not kingside_rook.has_moved:
                if board.squares[self.row][5] is None and board.squares[self.row][6] is None:
                    if not check_check or (
                        not board.is_square_under_attack(self.row, 5, 'black' if self.color == 'white' else 'white') and
                        not board.is_square_under_attack(self.row, 6, 'black' if self.color == 'white' else 'white')
                    ):
                        castle_move = self.create_move(board, self.row, 6)
                        castle_move.is_castling = True
                        moves.append(castle_move)
            
            queenside_rook = board.squares[self.row][0]
            if queenside_rook and isinstance(queenside_rook, Rook) and not queenside_rook.has_moved:
                if board.squares[self.row][1] is None and board.squares[self.row][2] is None and board.squares[self.row][3] is None:
                    if not check_check or (
                        not board.is_square_under_attack(self.row, 3, 'black' if self.color == 'white' else 'white') and
                        not board.is_square_under_attack(self.row, 2, 'black' if self.color == 'white' else 'white')
                    ):
                        castle_move = self.create_move(board, self.row, 2)
                        castle_move.is_castling = True
                        moves.append(castle_move)
        
        if check_check:
            opponent_color = 'black' if self.color == 'white' else 'white'
            moves = [move for move in moves if not (
                board.would_move_cause_check(move, self.color) or 
                (not move.is_castling and board.is_square_under_attack(move.to_row, move.to_col, opponent_color))
            )]
            
        return moves

# Board class
class Board:
    def __init__(self):
        self.squares = [[None for _ in range(8)] for _ in range(8)]
        self.move_history = []
        self.white_king_position = (7, 4)
        self.black_king_position = (0, 4)
        self.initialize_board()
        
    def initialize_board(self):
        for col in range(8):
            self.squares[1][col] = Pawn('black', (1, col))
            self.squares[6][col] = Pawn('white', (6, col))
        
        self.squares[0][0] = Rook('black', (0, 0))
        self.squares[0][1] = Knight('black', (0, 1))
        self.squares[0][2] = Bishop('black', (0, 2))
        self.squares[0][3] = Queen('black', (0, 3))
        self.squares[0][4] = King('black', (0, 4))
        self.squares[0][5] = Bishop('black', (0, 5))
        self.squares[0][6] = Knight('black', (0, 6))
        self.squares[0][7] = Rook('black', (0, 7))
        
        self.squares[7][0] = Rook('white', (7, 0))
        self.squares[7][1] = Knight('white', (7, 1))
        self.squares[7][2] = Bishop('white', (7, 2))
        self.squares[7][3] = Queen('white', (7, 3))
        self.squares[7][4] = King('white', (7, 4))
        self.squares[7][5] = Bishop('white', (7, 5))
        self.squares[7][6] = Knight('white', (7, 6))
        self.squares[7][7] = Rook('white', (7, 7))
    
    def make_move(self, move):
        piece = self.squares[move.from_row][move.from_col]
        move.captured_piece = self.squares[move.to_row][move.to_col]
        self.move_history.append(move)
        
        if move.is_en_passant:
            capture_row = move.from_row
            capture_col = move.to_col
            move.captured_piece = self.squares[capture_row][capture_col]
            self.squares[capture_row][capture_col] = None
        
        self.squares[move.to_row][move.to_col] = piece
        self.squares[move.from_row][move.from_col] = None
        piece.row, piece.col = move.to_row, move.to_col
        piece.has_moved = True
        
        if move.is_castling:
            if move.to_col > move.from_col:
                rook = self.squares[move.from_row][7]
                self.squares[move.from_row][5] = rook
                self.squares[move.from_row][7] = None
                rook.col = 5
                rook.has_moved = True
            else:
                rook = self.squares[move.from_row][0]
                self.squares[move.from_row][3] = rook
                self.squares[move.from_row][0] = None
                rook.col = 3
                rook.has_moved = True
        
        if move.is_promotion:
            promoted_piece = None
            if move.promotion_piece == 'Q':
                promoted_piece = Queen(piece.color, (move.to_row, move.to_col))
            elif move.promotion_piece == 'R':
                promoted_piece = Rook(piece.color, (move.to_row, move.to_col))
            elif move.promotion_piece == 'B':
                promoted_piece = Bishop(piece.color, (move.to_row, move.to_col))
            elif move.promotion_piece == 'N':
                promoted_piece = Knight(piece.color, (move.to_row, move.to_col))
            self.squares[move.to_row][move.to_col] = promoted_piece
            promoted_piece.has_moved = True
        
        if isinstance(piece, King):
            if piece.color == 'white':
                self.white_king_position = (move.to_row, move.to_col)
            else:
                self.black_king_position = (move.to_row, move.to_col)
    
    def undo_move(self):
        if not self.move_history:
            return
        
        move = self.move_history.pop()
        piece = self.squares[move.to_row][move.to_col]
        
        self.squares[move.from_row][move.from_col] = piece
        self.squares[move.to_row][move.to_col] = move.captured_piece
        piece.row, piece.col = move.from_row, move.from_col
        
        if len([m for m in self.move_history if m.piece == piece]) == 0:
            piece.has_moved = False
        
        if move.is_en_passant:
            capture_row = move.from_row
            capture_col = move.to_col
            self.squares[capture_row][capture_col] = move.captured_piece
            self.squares[move.to_row][move.to_col] = None
        
        if move.is_castling:
            if move.to_col > move.from_col:
                rook = self.squares[move.from_row][5]
                self.squares[move.from_row][7] = rook
                self.squares[move.from_row][5] = None
                rook.col = 7
                if len([m for m in self.move_history if m.piece == rook]) == 0:
                    rook.has_moved = False
            else:
                rook = self.squares[move.from_row][3]
                self.squares[move.from_row][0] = rook
                self.squares[move.from_row][3] = None
                rook.col = 0
                if len([m for m in self.move_history if m.piece == rook]) == 0:
                    rook.has_moved = False
        
        if move.is_promotion:
            pawn = Pawn(piece.color, (move.from_row, move.from_col))
            pawn.has_moved = True
            self.squares[move.from_row][move.from_col] = pawn
        
        if isinstance(piece, King):
            if piece.color == 'white':
                self.white_king_position = (move.from_row, move.from_col)
            else:
                self.black_king_position = (move.from_row, move.from_col)
    
    def get_piece(self, row, col):
        if 0 <= row < 8 and 0 <= col < 8:
            return self.squares[row][col]
        return None
    
    def is_valid_move(self, move):
        piece = self.get_piece(move.from_row, move.from_col)
        if not piece:
            return False
        
        valid_moves = piece.get_valid_moves(self)
        
        for valid_move in valid_moves:
            if valid_move.to_row == move.to_row and valid_move.to_col == move.to_col:
                move.is_castling = valid_move.is_castling
                move.is_en_passant = valid_move.is_en_passant
                move.is_promotion = valid_move.is_promotion
                move.promotion_piece = valid_move.promotion_piece
                return True
        
        return False
    
    def is_square_under_attack(self, row, col, attacking_color):
        for r in range(8):
            for c in range(8):
                piece = self.squares[r][c]
                if piece and piece.color == attacking_color:
                    if isinstance(piece, Pawn):
                        direction = 1 if piece.color == 'white' else -1
                        if (r - direction == row and (c - 1 == col or c + 1 == col)):
                            return True
                    else:
                        valid_moves = piece.get_valid_moves(self, check_check=False)
                        for move in valid_moves:
                            if move.to_row == row and move.to_col == col:
                                return True
        return False
    
    def is_check(self, color):
        king_position = self.white_king_position if color == 'white' else self.black_king_position
        king_row, king_col = king_position
        opponent_color = 'black' if color == 'white' else 'white'
        return self.is_square_under_attack(king_row, king_col, opponent_color)
    
    def would_move_cause_check(self, move, color):
        self.make_move(move)
        in_check = self.is_check(color)
        self.undo_move()
        return in_check
    
    def is_checkmate(self, color):
        if not self.is_check(color):
            return False
        return len(self.get_all_legal_moves(color)) == 0
    
    def is_stalemate(self, color):
        if self.is_check(color):
            return False
        return len(self.get_all_legal_moves(color)) == 0
    
    def get_all_moves(self, color):
        all_moves = []
        for row in range(8):
            for col in range(8):
                piece = self.squares[row][col]
                if piece and piece.color == color:
                    moves = piece.get_valid_moves(self, check_check=False)
                    all_moves.extend(moves)
        return all_moves
    
    def get_all_legal_moves(self, color):
        all_moves = self.get_all_moves(color)
        return [move for move in all_moves if not self.would_move_cause_check(move, color)]

    def get_last_move(self):
        return self.move_history[-1] if self.move_history else None

    def to_fen(self):
        fen = ""
        for row in range(8):
            empty = 0
            for col in range(8):
                piece = self.squares[row][col]
                if piece:
                    if empty > 0:
                        fen += str(empty)
                        empty = 0
                    symbol = piece.__class__.__name__[0]
                    if isinstance(piece, Knight):
                        symbol = 'N'
                    fen += symbol if piece.color == 'white' else symbol.lower()
                else:
                    empty += 1
            if empty > 0:
                fen += str(empty)
            if row < 7:
                fen += "/"
        return fen

# Player classes
class Player(ABC):
    def __init__(self, board, color):
        self.board = board
        self.color = color
        
    @abstractmethod
    def make_move(self, *args, **kwargs):
        pass

class HumanPlayer(Player):
    def make_move(self, move_text):
        move = Move.from_algebraic(move_text, self.board)
        if not move:
            print(f"Invalid move format: {move_text}")
            return None
        if move.piece.color != self.color:
            print(f"That's not your piece to move!")
            return None
        if not self.board.is_valid_move(move):
            print(f"Invalid move: {move_text}")
            return None
        return move

class AIPlayer(Player):
    def __init__(self, board, color, depth=3):
        super().__init__(board, color)
        self.depth = depth
        self.evaluation = Evaluation()
        
    def make_move(self):
        print(f"AI is thinking at depth {self.depth}...")
        best_score, best_move = self.minimax(self.depth, float('-inf'), float('inf'), True)
        if best_move:
            print(f"AI chose move: {best_move} with score: {best_score}")
            return best_move
        return None
        
    def minimax(self, depth, alpha, beta, maximizing_player):
        if depth == 0 or self.board.is_checkmate(self.color) or self.board.is_stalemate(self.color):
            return self.evaluation.evaluate(self.board, self.color), None
            
        color = self.color if maximizing_player else ('black' if self.color == 'white' else 'white')
        moves = self.board.get_all_legal_moves(color)
        
        if not moves:
            if self.board.is_check(color):
                return float('-inf') if maximizing_player else float('inf'), None
            return 0, None
        
        best_move = None
        
        if maximizing_player:
            best_score = float('-inf')
            for move in moves:
                self.board.make_move(move)
                current_score, _ = self.minimax(depth - 1, alpha, beta, False)
                self.board.undo_move()
                if current_score > best_score:
                    best_score = current_score
                    best_move = move
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
            return best_score, best_move
        else:
            best_score = float('inf')
            for move in moves:
                self.board.make_move(move)
                current_score, _ = self.minimax(depth - 1, alpha, beta, True)
                self.board.undo_move()
                if current_score < best_score:
                    best_score = current_score
                    best_move = move
                beta = min(beta, best_score)
                if beta <= alpha:
                    break
            return best_score, best_move

# Evaluation class
class Evaluation:
    def __init__(self):
        self.piece_values = {'Pawn': 100, 'Knight': 320, 'Bishop': 330, 'Rook': 500, 'Queen': 900, 'King': 20000}
        
        self.pawn_position_values = [
            [0,  0,  0,  0,  0,  0,  0,  0],
            [50, 50, 50, 50, 50, 50, 50, 50],
            [10, 10, 20, 30, 30, 20, 10, 10],
            [5,  5, 10, 25, 25, 10,  5,  5],
            [0,  0,  0, 20, 20,  0,  0,  0],
            [5, -5,-10,  0,  0,-10, -5,  5],
            [5, 10, 10,-20,-20, 10, 10,  5],
            [0,  0,  0,  0,  0,  0,  0,  0]
        ]
        
        self.knight_position_values = [
            [-50,-40,-30,-30,-30,-30,-40,-50],
            [-40,-20,  0,  0,  0,  0,-20,-40],
            [-30,  0, 10, 15, 15, 10,  0,-30],
            [-30,  5, 15, 20, 20, 15,  5,-30],
            [-30,  0, 15, 20, 20, 15,  0,-30],
            [-30,  5, 10, 15, 15, 10,  5,-30],
            [-40,-20,  0,  5,  5,  0,-20,-40],
            [-50,-40,-30,-30,-30,-30,-40,-50]
        ]
        
        self.bishop_position_values = [
            [-20,-10,-10,-10,-10,-10,-10,-20],
            [-10,  0,  0,  0,  0,  0,  0,-10],
            [-10,  0, 10, 10, 10, 10,  0,-10],
            [-10,  5,  5, 10, 10,  5,  5,-10],
            [-10,  0,  5, 10, 10,  5,  0,-10],
            [-10,  5,  5,  5,  5,  5,  5,-10],
            [-10,  0,  5,  0,  0,  5,  0,-10],
            [-20,-10,-10,-10,-10,-10,-10,-20]
        ]
        
        self.rook_position_values = [
            [0,  0,  0,  0,  0,  0,  0,  0],
            [5, 10, 10, 10, 10, 10, 10,  5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [0,  0,  0,  5,  5,  0,  0,  0]
        ]
        
        self.queen_position_values = [
            [-20,-10,-10, -5, -5,-10,-10,-20],
            [-10,  0,  0,  0,  0,  0,  0,-10],
            [-10,  0,  5,  5,  5,  5,  0,-10],
            [-5,  0,  5,  5,  5,  5,  0, -5],
            [0,  0,  5,  5,  5,  5,  0, -5],
            [-10,  5,  5,  5,  5,  5,  0,-10],
            [-10,  0,  5,  0,  0,  0,  0,-10],
            [-20,-10,-10, -5, -5,-10,-10,-20]
        ]
        
        self.king_position_values_early = [
            [-30,-40,-40,-50,-50,-40,-40,-30],
            [-30,-40,-40,-50,-50,-40,-40,-30],
            [-30,-40,-40,-50,-50,-40,-40,-30],
            [-30,-40,-40,-50,-50,-40,-40,-30],
            [-20,-30,-30,-40,-40,-30,-30,-20],
            [-10,-20,-20,-20,-20,-20,-20,-10],
            [20, 20,  0,  0,  0,  0, 20, 20],
            [20, 30, 10,  0,  0, 10, 30, 20]
        ]
        
        self.king_position_values_end = [
            [-50,-40,-30,-20,-20,-30,-40,-50],
            [-30,-20,-10,  0,  0,-10,-20,-30],
            [-30,-10, 20, 30, 30, 20,-10,-30],
            [-30,-10, 30, 40, 40, 30,-10,-30],
            [-30,-10, 30, 40, 40, 30,-10,-30],
            [-30,-10, 20, 30, 30, 20,-10,-30],
            [-30,-30,  0,  0,  0,  0,-30,-30],
            [-50,-30,-30,-30,-30,-30,-30,-50]
        ]
        
        self.position_values = {
            'Pawn': self.pawn_position_values,
            'Knight': self.knight_position_values,
            'Bishop': self.bishop_position_values,
            'Rook': self.rook_position_values,
            'Queen': self.queen_position_values,
            'King': self.king_position_values_early
        }
        
    def count_material(self, board, color):
        total = 0
        for row in range(8):
            for col in range(8):
                piece = board.squares[row][col]
                if piece and piece.color == color:
                    piece_type = piece.__class__.__name__
                    total += self.piece_values[piece_type]
        return total
    
    def evaluate_piece_position(self, piece, row, col):
        piece_type = piece.__class__.__name__
        position_table = self.position_values[piece_type]
        if piece.color == 'black':
            row = 7 - row
        return position_table[row][col]
    
    def evaluate_board_position(self, board, color):
        total = 0
        for row in range(8):
            for col in range(8):
                piece = board.squares[row][col]
                if piece:
                    pos_value = self.evaluate_piece_position(piece, row, col)
                    total += pos_value if piece.color == color else -pos_value
        return total
    
    def evaluate_king_safety(self, board, color):
        king_row, king_col = board.white_king_position if color == 'white' else board.black_king_position
        opponent_color = 'black' if color == 'white' else 'white'
        safety_score = 0
        for row_offset in [-1, 0, 1]:
            for col_offset in [-1, 0, 1]:
                if row_offset == 0 and col_offset == 0:
                    continue
                check_row = king_row + row_offset
                check_col = king_col + col_offset
                if 0 <= check_row < 8 and 0 <= check_col < 8:
                    if board.is_square_under_attack(check_row, check_col, opponent_color):
                        safety_score -= 10
                    piece = board.squares[check_row][check_col]
                    if piece and piece.color == color:
                        safety_score += 5
        if board.is_check(color):
            safety_score -= 50
        return safety_score
    
    def evaluate_mobility(self, board, color):
        legal_moves = board.get_all_legal_moves(color)
        opponent_color = 'black' if color == 'white' else 'white'
        opponent_moves = board.get_all_legal_moves(opponent_color)
        return len(legal_moves) - len(opponent_moves)
    
    def is_endgame(self, board):
        white_material = self.count_material(board, 'white') - self.piece_values['King']
        black_material = self.count_material(board, 'black') - self.piece_values['King']
        return white_material < 1500 and black_material < 1500
        
    def evaluate(self, board, color):
        if board.is_checkmate(color):
            return float('-inf')
        elif board.is_checkmate('black' if color == 'white' else 'white'):
            return float('inf')
        elif board.is_stalemate(color) or board.is_stalemate('black' if color == 'white' else 'white'):
            return 0
            
        material_score = self.count_material(board, color) - self.count_material(board, 'black' if color == 'white' else 'white')
        position_score = self.evaluate_board_position(board, color)
        king_safety_score = self.evaluate_king_safety(board, color)
        mobility_score = self.evaluate_mobility(board, color)
        
        if self.is_endgame(board):
            self.position_values['King'] = self.king_position_values_end
        else:
            self.position_values['King'] = self.king_position_values_early
            
        return (
            material_score * 1.0 +
            position_score * 0.1 +
            king_safety_score * 0.2 +
            mobility_score * 0.1
        )

# ChessGUI class
class ChessGUI:
    def __init__(self, root, game):
        self.root = root
        self.game = game
        self.square_size = 60
        self.selected_piece = None
        self.selected_square = None
        self.valid_moves = []
        self.white_captured_pieces = []
        self.black_captured_pieces = []
        self.load_piece_images()
        self.setup_gui()
        
    def setup_gui(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(padx=10, pady=10)
        
        self.black_player_frame = tk.Frame(self.main_frame)
        self.black_player_frame.pack(side=tk.TOP, fill=tk.X, pady=5)
        
        self.black_score_label = tk.Label(self.black_player_frame, text="Black score: 0", font=("Arial", 10, "bold"))
        self.black_score_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.black_captured_label = tk.Label(self.black_player_frame, text="Black captured: ", font=("Arial", 10))
        self.black_captured_label.pack(side=tk.LEFT)
        
        self.canvas = tk.Canvas(self.main_frame, width=self.square_size * 8, height=self.square_size * 8)
        self.canvas.pack(side=tk.TOP)
        
        self.white_player_frame = tk.Frame(self.main_frame)
        self.white_player_frame.pack(side=tk.TOP, fill=tk.X, pady=5)
        
        self.white_score_label = tk.Label(self.white_player_frame, text="White score: 0", font=("Arial", 10, "bold"))
        self.white_score_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.white_captured_label = tk.Label(self.white_player_frame, text="White captured: ", font=("Arial", 10))
        self.white_captured_label.pack(side=tk.LEFT)
        
        self.canvas.bind("<Button-1>", self.handle_click)
        
        self.status_label = tk.Label(self.main_frame, text="White's turn", font=("Arial", 12))
        self.status_label.pack(pady=5)
        
        self.new_game_button = tk.Button(self.main_frame, text="New Game", command=self.new_game)
        self.new_game_button.pack(pady=5)
        
        self.draw_board()
        
    def load_piece_images(self):
        self.piece_images = {}
        self.piece_chars = {
            'white': {'Pawn': '♙', 'Knight': '♘', 'Bishop': '♗', 'Rook': '♖', 'Queen': '♕', 'King': '♔'},
            'black': {'Pawn': '♟', 'Knight': '♞', 'Bishop': '♝', 'Rook': '♜', 'Queen': '♛', 'King': '♚'}
        }
        
    def draw_board(self):
        self.canvas.delete("all")
        colors = ["#B58863", "#5D8AA8"]
        highlight_color = "#FFFF00"
        move_color = "#7FFF00"
        
        for row in range(8):
            for col in range(8):
                x1 = col * self.square_size
                y1 = row * self.square_size
                x2 = x1 + self.square_size
                y2 = y1 + self.square_size
                color_index = (row + col) % 2
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=colors[color_index], outline="")
                
                if col == 0:
                    self.canvas.create_text(x1 + 5, y1 + 5, text=str(8-row), anchor=tk.NW, fill="black" if color_index == 0 else "white")
                if row == 7:
                    self.canvas.create_text(x2 - 5, y2 - 5, text=chr(97+col), anchor=tk.SE, fill="black" if color_index == 0 else "white")
        
        if self.selected_square:
            row, col = self.selected_square
            x1 = col * self.square_size
            y1 = row * self.square_size
            x2 = x1 + self.square_size
            y2 = y1 + self.square_size
            self.canvas.create_rectangle(x1, y1, x2, y2, outline=highlight_color, width=3)
            
        for move in self.valid_moves:
            row, col = move.to_row, move.to_col
            x1 = col * self.square_size
            y1 = row * self.square_size
            center_x = x1 + self.square_size // 2
            center_y = y1 + self.square_size // 2
            radius = self.square_size // 6
            self.canvas.create_oval(center_x - radius, center_y - radius, center_x + radius, center_y + radius, fill=move_color, outline="")
        
        for row in range(8):
            for col in range(8):
                piece = self.game.board.squares[row][col]
                if piece:
                    x = col * self.square_size + self.square_size // 2
                    y = row * self.square_size + self.square_size // 2
                    piece_char = self.piece_chars[piece.color][piece.__class__.__name__]
                    self.canvas.create_text(x, y, text=piece_char, font=("Arial", 32), fill="black" if piece.color == "black" else "white")
        
        self.update_captured_pieces_display()
    
    def update_captured_pieces_display(self):
        white_captured_text = "White captured: "
        for piece in self.white_captured_pieces:
            piece_class = piece.__class__.__name__
            white_captured_text += self.piece_chars[piece.color][piece_class] + " "
        self.white_captured_label.config(text=white_captured_text)
        
        black_captured_text = "Black captured: "
        for piece in self.black_captured_pieces:
            piece_class = piece.__class__.__name__
            black_captured_text += self.piece_chars[piece.color][piece_class] + " "
        self.black_captured_label.config(text=black_captured_text)
        
        self.white_score_label.config(text=f"White score: {self.game.white_score}")
        self.black_score_label.config(text=f"Black score: {self.game.black_score}")
    
    def handle_click(self, event):
        if self.game.game_over or self.game.current_player != self.game.human_player:
            return
            
        col = event.x // self.square_size
        row = event.y // self.square_size
        
        if not (0 <= row < 8 and 0 <= col < 8):
            return
            
        clicked_piece = self.game.board.get_piece(row, col)
        
        if self.selected_piece is None:
            if clicked_piece and clicked_piece.color == self.game.human_player.color:
                self.selected_piece = clicked_piece
                self.selected_square = (row, col)
                self.valid_moves = clicked_piece.get_valid_moves(self.game.board)
                self.valid_moves = [move for move in self.valid_moves 
                                  if not self.game.board.would_move_cause_check(move, clicked_piece.color)]
                self.draw_board()
        else:
            if self.selected_square == (row, col):
                self.selected_piece = None
                self.selected_square = None
                self.valid_moves = []
                self.draw_board()
                return
                
            if clicked_piece and clicked_piece.color == self.game.human_player.color:
                self.selected_piece = clicked_piece
                self.selected_square = (row, col)
                self.valid_moves = clicked_piece.get_valid_moves(self.game.board)
                self.valid_moves = [move for move in self.valid_moves 
                                  if not self.game.board.would_move_cause_check(move, clicked_piece.color)]
                self.draw_board()
                return
                
            selected_row, selected_col = self.selected_square
            move_found = None
            
            for move in self.valid_moves:
                if move.to_row == row and move.to_col == col:
                    move_found = move
                    break
            
            if move_found:
                captured_piece = self.game.board.squares[row][col]
                if captured_piece:
                    self.white_captured_pieces.append(captured_piece)
                    self.game.white_score += self.game.get_piece_value(captured_piece)
                
                if move_found.is_promotion:
                    promotion_piece = self.ask_promotion()
                    if promotion_piece:
                        move_found.promotion_piece = promotion_piece
                    else:
                        return
                
                self.game.board.make_move(move_found)
                self.selected_piece = None
                self.selected_square = None
                self.valid_moves = []
                self.draw_board()
                self.game.check_game_state()
                self.update_status()
                
                if not self.game.game_over:
                    self.game.current_player = self.game.ai_player
                    self.status_label.config(text="Black's turn (AI is thinking...)")
                    self.root.update()
                    self.root.after(500, self.game.ai_turn)
    
    def ask_promotion(self):
        promotion_window = tk.Toplevel(self.root)
        promotion_window.title("Promotion")
        promotion_window.geometry("300x100")
        promotion_window.resizable(False, False)
        promotion_piece = [None]
        
        def set_promotion(piece):
            promotion_piece[0] = piece
            promotion_window.destroy()
        
        tk.Label(promotion_window, text="Choose promotion piece:").pack(pady=5)
        buttons_frame = tk.Frame(promotion_window)
        buttons_frame.pack(pady=5)
        
        tk.Button(buttons_frame, text="Queen", command=lambda: set_promotion('Q')).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="Rook", command=lambda: set_promotion('R')).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="Bishop", command=lambda: set_promotion('B')).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="Knight", command=lambda: set_promotion('N')).pack(side=tk.LEFT, padx=5)
        
        promotion_window.transient(self.root)
        promotion_window.grab_set()
        self.root.wait_window(promotion_window)
        return promotion_piece[0]
    
    def update_status(self):
        if self.game.game_over:
            if self.game.board.is_checkmate('white'):
                self.status_label.config(text="Checkmate! Black wins!")
            elif self.game.board.is_checkmate('black'):
                self.status_label.config(text="Checkmate! White wins!")
            elif self.game.board.is_stalemate('white') or self.game.board.is_stalemate('black'):
                self.status_label.config(text="Stalemate! Game is a draw.")
        else:
            current_color = self.game.current_player.color.capitalize()
            if self.game.board.is_check(self.game.current_player.color):
                self.status_label.config(text=f"{current_color} is in check!")
            else:
                if self.game.current_player == self.game.ai_player:
                    self.status_label.config(text=f"Black's turn (AI is thinking...)")
                else:
                    self.status_label.config(text=f"{current_color}'s turn")
    
    def new_game(self):
        self.game.reset_game()
        self.selected_piece = None
        self.selected_square = None
        self.valid_moves = []
        self.white_captured_pieces = []
        self.black_captured_pieces = []
        self.draw_board()
        self.update_status()

# ChessGame class
class ChessGame:
    def __init__(self, root):
        self.root = root
        self.board = Board()
        self.human_player = HumanPlayer(self.board, 'white')
        self.ai_player = AIPlayer(self.board, 'black', depth=3)
        self.current_player = self.human_player
        self.game_over = False
        self.white_score = 0
        self.black_score = 0
        self.gui = ChessGUI(root, self)
    
    def ai_turn(self):
        if self.game_over:
            return
            
        move = self.ai_player.make_move()
        if move:
            captured_piece = self.board.squares[move.to_row][move.to_col]
            if captured_piece:
                self.gui.black_captured_pieces.append(captured_piece)
                self.black_score += self.get_piece_value(captured_piece)
            
            self.board.make_move(move)
            self.gui.draw_board()
            self.check_game_state()
            
            if not self.game_over:
                self.current_player = self.human_player
                self.gui.update_status()
    
    def check_game_state(self):
        opponent_color = 'black' if self.current_player.color == 'white' else 'white'
        if self.board.is_checkmate(opponent_color):
            self.game_over = True
            winner = self.current_player.color.capitalize()
            messagebox.showinfo("Game Over", f"Checkmate! {winner} wins!")
            self.gui.update_status()
        elif self.board.is_stalemate(opponent_color):
            self.game_over = True
            messagebox.showinfo("Game Over", "Stalemate! Game is a draw.")
            self.gui.update_status()
    
    def get_piece_value(self, piece):
        piece_values = {'Pawn': 1, 'Knight': 3, 'Bishop': 3, 'Rook': 5, 'Queen': 9, 'King': 0}
        return piece_values.get(piece.__class__.__name__, 0)
    
    def reset_game(self):
        self.board = Board()
        self.human_player.board = self.board
        self.ai_player.board = self.board
        self.current_player = self.human_player
        self.game_over = False
        self.white_score = 0
        self.black_score = 0

# Main function
def main():
    root = tk.Tk()
    root.title("Chess Game with Minimax AI")
    game = ChessGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()