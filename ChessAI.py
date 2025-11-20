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
    
    def get_best_move(self, depth=5):
        """Get the best move using Minimax with Alpha-Beta Pruning"""
        legal_moves = self.get_all_legal_moves(self.color, self.game.board)
        
        if not legal_moves:
            return None
        
        best_move = None
        best_score = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        
        for move in legal_moves:
            score = self.minimax_ab(move, depth - 1, False, alpha, beta, self.game.board)
            if score > best_score:
                best_score = score
                best_move = move
            alpha = max(alpha, best_score)
        
        return best_move
    
    def minimax_ab(self, move, depth, is_maximizing, alpha, beta, board):
        """Minimax with Alpha-Beta Pruning"""
        from_pos, to_pos = move
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        # Create a copy of the board to simulate the move
        temp_board = [row[:] for row in board]
        piece = temp_board[from_row][from_col]
        temp_board[from_row][from_col] = None
        temp_board[to_row][to_col] = piece
        
        # Base case: depth reached or game over
        if depth == 0:
            return self.evaluate_position(temp_board)
        
        # Maximizing player (AI)
        if is_maximizing:
            max_score = float('-inf')
            opponent_moves = self.get_all_legal_moves(self.color, temp_board)
            
            if not opponent_moves:
                return self.evaluate_position(temp_board)
            
            for next_move in opponent_moves:
                score = self.minimax_ab(next_move, depth - 1, False, alpha, beta, temp_board)
                max_score = max(score, max_score)
                alpha = max(alpha, max_score)
                
                # Beta cutoff
                if beta <= alpha:
                    break
            
            return max_score
        
        # Minimizing player (opponent)
        else:
            min_score = float('inf')
            opponent_moves = self.get_all_legal_moves(self.opponent_color, temp_board)
            
            if not opponent_moves:
                return self.evaluate_position(temp_board)
            
            for next_move in opponent_moves:
                score = self.minimax_ab(next_move, depth - 1, True, alpha, beta, temp_board)
                min_score = min(score, min_score)
                beta = min(beta, min_score)
                
                # Alpha cutoff
                if beta <= alpha:
                    break
            
            return min_score
    
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