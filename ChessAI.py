from pieces import Pawn, Rook, Knight, Bishop, Queen, King
import random

class ChessAI:
    def __init__(self, color, game):
        self.color = color
        self.game = game
        self.opponent_color = 'black' if color == 'white' else 'white'
        
        # Piece values for evaluation
        self.piece_values = {
            'pawn': 1,
            'night': 3,  # Knight
            'bishop': 3,
            'rook': 5,
            'queen': 9,
            'king': 0  # King value not counted
        }
    
    def get_best_move(self):
        """Get the best move for the AI"""
        legal_moves = self.get_all_legal_moves(self.color, self.game.board)
        
        if not legal_moves:
            return None
        
        # Evaluate each move and pick the best one
        best_move = None
        best_score = float('-inf')
        
        for move in legal_moves:
            score = self.evaluate_move(move)
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_move
    
    def get_all_legal_moves(self, color, board):
        """Get all legal moves for a color"""
        all_moves = []
        
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece is not None and piece.color == color:
                    legal_moves = self.game.get_legal_moves(piece, board)
                    for move in legal_moves:
                        all_moves.append(((row, col), move))
        
        return all_moves
    
    def evaluate_move(self, move):
        """Evaluate a move and return a score"""
        from_pos, to_pos = move
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        piece = self.game.board[from_row][from_col]
        captured_piece = self.game.board[to_row][to_col]
        
        score = 0
        
        # Prioritize captures - highest value target first
        if captured_piece is not None:
            score += self.piece_values.get(captured_piece.type, 0) * 10
        
        # Slight preference for moving pieces to the center
        center_distance = self.distance_to_center(to_row, to_col)
        score -= center_distance  # Closer to center = higher score
        
        # Penalize moving into attack (very basic)
        if self.game.is_square_attacked(to_row, to_col, self.opponent_color, self.game.board):
            score -= self.piece_values.get(piece.type, 0) * 2
        
        return score
    
    def distance_to_center(self, row, col):
        """Calculate how far a square is from the center (0-3, lower is better)"""
        center_row, center_col = 3.5, 3.5
        return abs(row - center_row) + abs(col - center_col)
    
    def evaluate_position(self, board):
        """Evaluate the overall position from the AI's perspective"""
        score = 0
        
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece is not None:
                    piece_value = self.piece_values.get(piece.type, 0)
                    
                    if piece.color == self.color:
                        score += piece_value
                    else:
                        score -= piece_value
        
        return score
    
    def make_move(self):
        """Execute the best move for the AI"""
        move = self.get_best_move()
        if move:
            from_pos, to_pos = move
            self.game.move_piece(from_pos, to_pos)
            return True
        return False