class Piece:
    def __init__(self, color, row, col):
        self.color=color
        self.row = row
        self.col = col
        self.has_moved=False
    def get_valid_moves():
        pass
    def get_code(self):
        """Return the string code for image loading (like 'wp', 'bk')"""
        color_char = 'w' if self.color == 'white' else 'b'
        return f"{color_char}{self.type[0]}"  



class Rook(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.type='rook'
    
    def get_valid_moves(self, board):
        moves = []

        directions = [(1,0), (-1,0), (0,1), (0,-1)]
        for dr, dc in directions:
            for distance in range(1,8):
                new_row = self.row + dr * distance
                new_col = self.col + dc * distance

                if not((0 <= new_row < 8) and (0 <= new_row< 8)):
                    break
                piece_at_pos = board[new_row][new_col]
                
                if piece_at_pos == None:
                    moves.append((new_row,new_col))

                elif (piece_at_pos.color != self.color):
                    moves.append((new_row,new_col))
                    break
                else:
                    break
        return moves
    

class Bishop(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.type='bishop'
    
    def get_valid_moves(self, board):
        moves = []

        directions = [(1,1), (-1,-1), (-1,1), (1,-1)]
        for dr, dc in directions:
            for distance in range(1,8):
                new_row = self.row + dr * distance
                new_col = self.col + dc * distance

                if not((0 <= new_row < 8) and (0 <= new_row< 8)):
                    break
                piece_at_pos = board[new_row][new_col]
                
                if piece_at_pos == None:
                    moves.append((new_row,new_col))

                elif (piece_at_pos.color != self.color):
                    moves.append((new_row,new_col))
                    break
                else:
                    break
        return moves


class Queen(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.type='queen'
    
    def get_valid_moves(self, board):
        moves = []

        directions = [(1,0), (-1,0), (0,1), (0,-1), (1,1), (-1,-1), (-1,1), (1,-1)]
        for dr, dc in directions:
            for distance in range(1,8):
                new_row = self.row + dr * distance
                new_col = self.col + dc * distance

                if not((0 <= new_row < 8) and (0 <= new_row< 8)):
                    break
                piece_at_pos = board[new_row][new_col]
                
                if piece_at_pos == None:
                    moves.append((new_row,new_col))

                elif (piece_at_pos.color != self.color):
                    moves.append((new_row,new_col))
                    break
                else:
                    break
        return moves


class King(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.type='king'
    
    def get_valid_moves(self, board):
        moves = []

        directions = [(1,0), (-1,0), (0,1), (0,-1), (1,1), (-1,-1), (-1,1), (1,-1)]
        for dr, dc in directions:
            
            new_row = self.row + dr 
            new_col = self.col + dc 

            if not((0 <= new_row < 8) and (0 <= new_row< 8)):
                continue
            piece_at_pos = board[new_row][new_col]
                
            if piece_at_pos == None:
                moves.append((new_row,new_col))

            elif (piece_at_pos.color != self.color):
                moves.append((new_row,new_col))
                
            
        return moves



class Knight(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.type='night'
    
    def get_valid_moves(self, board):
        moves = []

        directions = [(2,1), (2,-1), (-2,1), (-2,-1), (1,2), (-1,2), (1,-2), (-1,-2)]
        for dr, dc in directions:
        
            new_row = self.row + dr
            new_col = self.col + dc

            if not((0 <= new_row < 8) and (0 <= new_row< 8)):
                continue
            piece_at_pos = board[new_row][new_col]
                
            if piece_at_pos == None:
                moves.append((new_row,new_col))

            elif (piece_at_pos.color != self.color):
                moves.append((new_row,new_col))
            
                
        return moves


class Pawn(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.type='pawn'
    
    def get_valid_moves(self, board):
        moves = []

        directions = [(0,2),(0,1)]
        for dr, dc in directions:
        
            new_row = self.row + dr
            new_col = self.col + dc

            if not((0 <= new_row < 8) and (0 <= new_row< 8)):
                continue
            piece_at_pos = board[new_row][new_col]
                
            if piece_at_pos == None:
                moves.append((new_row,new_col))

            elif (piece_at_pos.color != self.color):
                moves.append((new_row,new_col))
            
                
        return moves