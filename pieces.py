class Piece:
    def __init__(self, color, row, col):
        self.color = color
        self.row = row
        self.col = col
        self.has_moved = False
    
    def get_code(self):
        """Return the string code for image loading (like 'wp', 'bk')"""
        color_char = 'w' if self.color == 'white' else 'b'
        return f"{color_char}{self.type[0]}"  


class Rook(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.type = 'rook'
    
    def get_valid_moves(self, board):
        moves = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        
        for dr, dc in directions:
            for distance in range(1, 8):
                new_row = self.row + dr * distance
                new_col = self.col + dc * distance
                
                if not (0 <= new_row < 8 and 0 <= new_col < 8):
                    break
                
                piece_at_pos = board[new_row][new_col]
                
                if piece_at_pos is None:
                    moves.append((new_row, new_col))
                elif piece_at_pos.color != self.color:
                    moves.append((new_row, new_col))
                    break
                else:
                    break
        
        return moves


class Bishop(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.type = 'bishop'
    
    def get_valid_moves(self, board):
        moves = []
        directions = [(1, 1), (-1, -1), (-1, 1), (1, -1)]
        
        for dr, dc in directions:
            for distance in range(1, 8):
                new_row = self.row + dr * distance
                new_col = self.col + dc * distance
                
                if not (0 <= new_row < 8 and 0 <= new_col < 8):
                    break
                
                piece_at_pos = board[new_row][new_col]
                
                if piece_at_pos is None:
                    moves.append((new_row, new_col))
                elif piece_at_pos.color != self.color:
                    moves.append((new_row, new_col))
                    break
                else:
                    break
        
        return moves


class Queen(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.type = 'queen'
    
    def get_valid_moves(self, board):
        moves = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (-1, 1), (1, -1)]
        
        for dr, dc in directions:
            for distance in range(1, 8):
                new_row = self.row + dr * distance
                new_col = self.col + dc * distance
                
                if not (0 <= new_row < 8 and 0 <= new_col < 8):
                    break
                
                piece_at_pos = board[new_row][new_col]
                
                if piece_at_pos is None:
                    moves.append((new_row, new_col))
                elif piece_at_pos.color != self.color:
                    moves.append((new_row, new_col))
                    break
                else:
                    break
        
        return moves


class King(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.type = 'king'
    
    def get_valid_moves(self, board):
        moves = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (-1, 1), (1, -1)]
        
        for dr, dc in directions:
            new_row = self.row + dr
            new_col = self.col + dc
            
            if not (0 <= new_row < 8 and 0 <= new_col < 8):
                continue
            
            piece_at_pos = board[new_row][new_col]
            
            if piece_at_pos is None:
                moves.append((new_row, new_col))
            elif piece_at_pos.color != self.color:
                moves.append((new_row, new_col))
        
        return moves


class Knight(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.type = 'night'
    
    def get_valid_moves(self, board):
        moves = []
        directions = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (-1, 2), (1, -2), (-1, -2)]
        
        for dr, dc in directions:
            new_row = self.row + dr
            new_col = self.col + dc
            
            if not (0 <= new_row < 8 and 0 <= new_col < 8):
                continue
            
            piece_at_pos = board[new_row][new_col]
            
            if piece_at_pos is None:
                moves.append((new_row, new_col))
            elif piece_at_pos.color != self.color:
                moves.append((new_row, new_col))
        
        return moves


class Pawn(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.type = 'pawn'
    
    def get_valid_moves(self, board):
        moves = []
        
        # Direction: white pawns move up (decreasing row), black pawns move down (increasing row)
        direction = -1 if self.color == 'white' else 1
        
        # One square forward
        new_row = self.row + direction
        if 0 <= new_row < 8:
            if board[new_row][self.col] is None:
                moves.append((new_row, self.col))
                
                # Two squares forward on first move
                if not self.has_moved:
                    new_row_two = self.row + direction * 2
                    if board[new_row_two][self.col] is None:
                        moves.append((new_row_two, self.col))
        
        # Captures (diagonal)
        for dc in [-1, 1]:
            new_row = self.row + direction
            new_col = self.col + dc
            
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                piece_at_pos = board[new_row][new_col]
                if piece_at_pos is not None and piece_at_pos.color != self.color:
                    moves.append((new_row, new_col))
        
        return moves