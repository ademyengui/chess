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
    
    def get_best_move(self, depth=4):
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
        
        # Material count
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece is not None:
                    piece_value = self.piece_values.get(piece.type, 0)
                    positional = self.get_positional_bonus(piece, row, col, board)
                    
                    if piece.color == self.color:
                        # AI's pieces add to score
                        score += piece_value + positional
                    else:
                        # Opponent's pieces subtract from score
                        score -= piece_value + positional
        
        return score
    
    def get_positional_bonus(self, piece, row, col, board):
        """Get positional bonus for a piece"""
        bonus = 0
        
        # Pawn positioning
        if piece.type == 'pawn':
            bonus += self.pawn_bonus(piece, row, col, board)
        
        # Knight positioning
        elif piece.type == 'night':
            bonus += self.knight_bonus(row, col, board)
        
        # Bishop positioning
        elif piece.type == 'bishop':
            bonus += self.bishop_bonus(row, col, board)
        
        # Rook positioning
        elif piece.type == 'rook':
            bonus += self.rook_bonus(row, col, board)
        
        # Queen positioning
        elif piece.type == 'queen':
            bonus += self.queen_bonus(row, col, board)
        
        # King positioning
        elif piece.type == 'king':
            bonus += self.king_bonus(piece, row, col, board)
        
        # General centralization bonus
        bonus += self.centralization_bonus(row, col)
        
        return bonus
    
    def pawn_bonus(self, pawn, row, col, board):
        """Evaluate pawn position"""
        bonus = 0
        
        # Advancement bonus (pawns near opponent side are better)
        if pawn.color == 'white':
            bonus += (7 - row) * 0.5  # White pawns going down
        else:
            bonus += row * 0.5  # Black pawns going up
        
        # Passed pawn bonus (no enemy pawns ahead on same or adjacent files)
        is_passed = self.is_passed_pawn(pawn, row, col, board)
        if is_passed:
            bonus += 2
        
        # Doubled pawn penalty
        for r in range(8):
            if r != row and board[r][col] is not None:
                piece = board[r][col]
                if piece.type == 'pawn' and piece.color == pawn.color:
                    bonus -= 1
        
        return bonus
    
    def is_passed_pawn(self, pawn, row, col, board):
        """Check if a pawn is passed (no enemy pawns can stop it)"""
        direction = -1 if pawn.color == 'white' else 1
        enemy_color = 'black' if pawn.color == 'white' else 'white'
        
        # Check forward files for enemy pawns
        for adjacent_col in [col - 1, col, col + 1]:
            if 0 <= adjacent_col < 8:
                for r in range(row + direction, 8 if direction > 0 else -1, direction):
                    if 0 <= r < 8:
                        piece = board[r][adjacent_col]
                        if piece is not None and piece.type == 'pawn' and piece.color == enemy_color:
                            return False
        
        return True
    
    def knight_bonus(self, row, col, board):
        """Evaluate knight position"""
        bonus = 0
        
        # Knights are better on central, outpost squares
        center_distance = self.distance_to_center(row, col)
        bonus += (4 - center_distance) * 0.5
        
        # Bonus for being protected
        bonus += self.piece_protection_bonus(row, col, board)
        
        return bonus
    
    def bishop_bonus(self, row, col, board):
        """Evaluate bishop position"""
        bonus = 0
        
        # Bonus for long diagonals (more mobility)
        long_diagonal = min(row, col) + min(7 - row, 7 - col)
        bonus += long_diagonal * 0.1
        
        # Bonus for being protected
        bonus += self.piece_protection_bonus(row, col, board)
        
        return bonus
    
    def rook_bonus(self, row, col, board):
        """Evaluate rook position"""
        bonus = 0
        
        # Bonus for open files (no pawns blocking)
        is_open_file = True
        for r in range(8):
            piece = board[r][col]
            if piece is not None and piece.type == 'pawn':
                is_open_file = False
                break
        
        if is_open_file:
            bonus += 1
        
        # Bonus for 7th rank (very strong position)
        if row == 6:
            bonus += 1
        
        # Bonus for being protected
        bonus += self.piece_protection_bonus(row, col, board)
        
        return bonus
    
    def queen_bonus(self, row, col, board):
        """Evaluate queen position"""
        bonus = 0
        
        # Queens are valuable in the center
        center_distance = self.distance_to_center(row, col)
        bonus += (4 - center_distance) * 0.3
        
        # Bonus for being protected
        bonus += self.piece_protection_bonus(row, col, board)
        
        return bonus
    
    def king_bonus(self, king, row, col, board):
        """Evaluate king position (safety is important)"""
        bonus = 0
        
        # Early game: king should be safe in corner (after castling)
        # Late game: king should be active in center
        
        # Bonus for castling
        if king.has_moved:
            bonus -= 0.5  # Slight penalty for moving king early
        
        # Penalty for being exposed
        exposed = True
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = row + dr, col + dc
                if 0 <= nr < 8 and 0 <= nc < 8:
                    piece = board[nr][nc]
                    if piece is not None and piece.type == 'pawn' and piece.color == king.color:
                        bonus += 0.5  # Pawn shield bonus
        
        return bonus
    
    def piece_protection_bonus(self, row, col, board):
        """Check if piece is protected by friendly pieces"""
        bonus = 0
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = row + dr, col + dc
                if 0 <= nr < 8 and 0 <= nc < 8:
                    piece = board[nr][nc]
                    if piece is not None and piece.color == board[row][col].color:
                        bonus += 0.2
        
        return bonus
    
    def centralization_bonus(self, row, col):
        """Bonus for being near the center"""
        center_distance = self.distance_to_center(row, col)
        return (4 - center_distance) * 0.1
    
    def make_move(self):
        """Execute the best move for the AI"""
        move = self.get_best_move()
        if move:
            from_pos, to_pos = move
            self.game.move_piece(from_pos, to_pos)
            return True
        return False