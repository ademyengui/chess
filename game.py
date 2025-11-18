from pieces import *

class ChessGame:
    def __init__(self):
        self.board = self.create_board()
        self.selected_piece = None
        self.selected_pos = None  # Will store as (row, col) in board coords
        self.current_turn = 'white'
        self.valid_moves = []
    
    def create_board(self):
        """Initialize the chess board with actual Piece objects
        Board indexing: row 0 = rank 8 (black back rank), row 7 = rank 1 (white back rank)
        Column indexing: col 0 = file a, col 7 = file h
        """
        board = [[None for _ in range(8)] for _ in range(8)]
        
        # Black pieces (top) - rank 8
        board[0][0] = Rook('black', 0, 0)
        board[0][1] = Knight('black', 0, 1)
        board[0][2] = Bishop('black', 0, 2)
        board[0][3] = Queen('black', 0, 3)
        board[0][4] = King('black', 0, 4)
        board[0][5] = Bishop('black', 0, 5)
        board[0][6] = Knight('black', 0, 6)
        board[0][7] = Rook('black', 0, 7)
        
        # Black pawns - rank 7
        for col in range(8):
            board[1][col] = Pawn('black', 1, col)
        
        # White pawns - rank 2
        for col in range(8):
            board[6][col] = Pawn('white', 6, col)
        
        # White pieces - rank 1
        board[7][0] = Rook('white', 7, 0)
        board[7][1] = Knight('white', 7, 1)
        board[7][2] = Bishop('white', 7, 2)
        board[7][3] = Queen('white', 7, 3)
        board[7][4] = King('white', 7, 4)
        board[7][5] = Bishop('white', 7, 5)
        board[7][6] = Knight('white', 7, 6)
        board[7][7] = Rook('white', 7, 7)
        
        return board
    
    def pixel_to_board_coords(self, pixel_pos):
        """Convert pixel coordinates to board row/col (0-7)"""
        x, y = pixel_pos
        col = x // 75  # 600 / 8 = 75
        row = y // 75
        return row, col
    
    def board_to_chess_notation(self, row, col):
        """Convert board coordinates to standard chess notation (e.g., 'e2')
        Top-left (0,0) = a8, so row increases down toward rank 1
        """
        file = chr(ord('a') + col)  # a-h (0-7)
        rank = str(8 - row)  # row 0 = rank 8, row 7 = rank 1
        return f"{file}{rank}"
    
    def chess_notation_to_board(self, notation):
        """Convert chess notation (e.g., 'e2') to board coordinates
        a8 = (0,0), h1 = (7,7)
        """
        file = ord(notation[0]) - ord('a')  # 0-7
        rank = int(notation[1])  # 1-8
        row = 8 - rank  # rank 8 = row 0, rank 1 = row 7
        return row, file
    
    def handle_click(self, pos):
        """Handle mouse clicks for piece selection and movement"""
        row, col = self.pixel_to_board_coords(pos)
        print(row, col)
        # Bounds check
        if not (0 <= row < 8 and 0 <= col < 8):
            return
        
        clicked_piece = self.board[row][col]
        chess_pos = self.board_to_chess_notation(row, col)
        
        # If a piece is already selected
        if self.selected_piece is not None:
            # Check if clicking on a valid move destination
            if (row, col) in self.valid_moves:
                self.move_piece(self.selected_pos, (row, col))
                self.selected_piece = None
                self.selected_pos = None
                self.valid_moves = []
            # Check if clicking on another piece of the same color to reselect
            elif clicked_piece is not None and clicked_piece.color == self.current_turn:
                self.selected_piece = clicked_piece
                self.selected_pos = (row, col)
                self.valid_moves = clicked_piece.get_valid_moves(self.board)
                selected_chess_pos = self.board_to_chess_notation(row, col)
                print(f"Selected {clicked_piece.type} at {selected_chess_pos}")
            # Otherwise deselect
            else:
                self.selected_piece = None
                self.selected_pos = None
                self.valid_moves = []
        
        # No piece is selected, try to select one
        else:
            if clicked_piece is not None and clicked_piece.color == self.current_turn:
                self.selected_piece = clicked_piece
                self.selected_pos = (row, col)
                self.valid_moves = clicked_piece.get_valid_moves(self.board)
                print(f"Selected {clicked_piece.type} at {chess_pos}")
                print(f"Valid moves: {[self.board_to_chess_notation(r, c) for r, c in self.valid_moves]}")
    
    def move_piece(self, from_pos, to_pos):
        """Move a piece from one square to another"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        piece = self.board[from_row][from_col]
        from_notation = self.board_to_chess_notation(from_row, from_col)
        to_notation = self.board_to_chess_notation(to_row, to_col)
        
        # Move the piece
        self.board[from_row][from_col] = None
        self.board[to_row][to_col] = piece
        
        # Update piece's position
        piece.row = to_row
        piece.col = to_col
        piece.has_moved = True
        
        # Switch turns
        self.current_turn = 'black' if self.current_turn == 'white' else 'white'
        print(f"Moved {piece.type} from {from_notation} to {to_notation}. {self.current_turn.capitalize()}'s turn.")