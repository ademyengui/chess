from pieces import *
class ChessGame:
    def __init__(self):
        self.board = self.create_board()
        self.selected_piece = None
        self.selected_pos = None
        self.current_turn = 'white'
        self.valid_moves = []
        self.last_move = None
        self.game_over = False
        self.checkmate = False
        self.move_history = []  # Track all board states for repetition
        self.halfmove_clock = 0  # Moves since last capture or pawn move (50-move rule)
    
    def create_board(self):
        """Initialize the chess board with actual Piece objects"""
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
        col = x // 75
        row = y // 75
        return row, col
    
    def board_to_chess_notation(self, row, col):
        """Convert board coordinates to standard chess notation (e.g., 'e2')"""
        file = chr(ord('a') + col)
        rank = str(8 - row)
        return f"{file}{rank}"
    
    def chess_notation_to_board(self, notation):
        """Convert chess notation (e.g., 'e2') to board coordinates"""
        file = ord(notation[0]) - ord('a')
        rank = int(notation[1])
        row = 8 - rank
        return row, file
    
    def find_king(self, color, board=None):
        """Find the king of a given color on the board"""
        if board is None:
            board = self.board
        
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if isinstance(piece, King) and piece.color == color:
                    return row, col
        return None
    
    def is_square_attacked(self, row, col, by_color, board=None):
        """Check if a square is attacked by pieces of a given color"""
        if board is None:
            board = self.board
        
        # Check all opponent pieces
        for r in range(8):
            for c in range(8):
                piece = board[r][c]
                if piece is not None and piece.color == by_color:
                    # Get raw moves without checking for check
                    moves = piece.get_valid_moves(board)
                    if (row, col) in moves:
                        return True
        
        return False
    
    def is_in_check(self, color, board=None):
        """Check if a color's king is in check"""
        if board is None:
            board = self.board
        
        king_pos = self.find_king(color, board)
        if king_pos is None:
            return False
        
        row, col = king_pos
        enemy_color = 'black' if color == 'white' else 'white'
        return self.is_square_attacked(row, col, enemy_color, board)
    
    def handle_click(self, pos):
        """Handle mouse clicks for piece selection and movement"""
        if self.game_over:
            print("Game is over!")
            return
        
        row, col = self.pixel_to_board_coords(pos)
        
        if not (0 <= row < 8 and 0 <= col < 8):
            return
        
        clicked_piece = self.board[row][col]
        chess_pos = self.board_to_chess_notation(row, col)
        
        if self.selected_piece is not None:
            if (row, col) in self.valid_moves:
                self.move_piece(self.selected_pos, (row, col))
                self.selected_piece = None
                self.selected_pos = None
                self.valid_moves = []
            elif clicked_piece is not None and clicked_piece.color == self.current_turn:
                self.selected_piece = clicked_piece
                self.selected_pos = (row, col)
                self.valid_moves = self.get_legal_moves(clicked_piece)
                selected_chess_pos = self.board_to_chess_notation(row, col)
                print(f"Selected {clicked_piece.type} at {selected_chess_pos}")
            else:
                self.selected_piece = None
                self.selected_pos = None
                self.valid_moves = []
        else:
            if clicked_piece is not None and clicked_piece.color == self.current_turn:
                self.selected_piece = clicked_piece
                self.selected_pos = (row, col)
                self.valid_moves = self.get_legal_moves(clicked_piece)
                print(f"Selected {clicked_piece.type} at {chess_pos}")
                print(f"Valid moves: {[self.board_to_chess_notation(r, c) for r, c in self.valid_moves]}")
    
    def get_legal_moves(self, piece, board=None):
        """Get valid moves that don't leave the king in check"""
        if board is None:
            board = self.board
        
        moves = piece.get_valid_moves(board)
        legal_moves = []
        
        for move in moves:
            # Simulate the move
            temp_board = [row[:] for row in board]
            from_row, from_col = piece.row, piece.col
            to_row, to_col = move
            
            temp_board[from_row][from_col] = None
            temp_board[to_row][to_col] = piece
            
            # Check if king is in check after the move
            if not self.is_in_check(piece.color, temp_board):
                legal_moves.append(move)
        
        # Add special moves only if they don't leave king in check
        if isinstance(piece, Pawn):
            en_passant_moves = self.get_en_passant_moves(piece)
            for move in en_passant_moves:
                # Simulate en passant
                temp_board = [row[:] for row in board]
                from_row, from_col = piece.row, piece.col
                to_row, to_col = move
                
                temp_board[from_row][from_col] = None
                temp_board[to_row][to_col] = piece
                temp_board[from_row][to_col] = None  # Remove captured pawn
                
                if not self.is_in_check(piece.color, temp_board):
                    legal_moves.append(move)
        
        if isinstance(piece, King):
            castling_moves = self.get_castling_moves(piece)
            for move in castling_moves:
                # Simulate castling
                temp_board = [row[:] for row in board]
                from_row, from_col = piece.row, piece.col
                to_row, to_col = move
                
                # Move king
                temp_board[from_row][from_col] = None
                temp_board[to_row][to_col] = piece
                
                # Check if king passes through or lands in check
                if not self.is_in_check(piece.color, temp_board):
                    # Also check intermediate square for castling
                    if abs(to_col - from_col) == 2:
                        intermediate_col = (from_col + to_col) // 2
                        if not self.is_square_attacked(from_row, intermediate_col, 
                                                       'black' if piece.color == 'white' else 'white', temp_board):
                            legal_moves.append(move)
                    else:
                        legal_moves.append(move)
        
        return legal_moves
    
    def get_en_passant_moves(self, pawn):
        """Get en passant capture moves for a pawn"""
        moves = []
        if not self.last_move:
            return moves
        
        last_from, last_to = self.last_move
        last_from_row, last_from_col = last_from
        last_to_row, last_to_col = last_to
        
        if abs(last_from_row - last_to_row) == 2 and isinstance(self.board[last_to_row][last_to_col], Pawn):
            direction = -1 if pawn.color == 'white' else 1
            
            for dc in [-1, 1]:
                adjacent_col = pawn.col + dc
                if 0 <= adjacent_col < 8:
                    adjacent_piece = self.board[pawn.row][adjacent_col]
                    
                    if (isinstance(adjacent_piece, Pawn) and 
                        adjacent_piece.color != pawn.color and
                        adjacent_piece.col == last_to_col and
                        adjacent_piece.row == last_to_row):
                        
                        capture_row = pawn.row + direction
                        if 0 <= capture_row < 8:
                            moves.append((capture_row, adjacent_col))
        
        return moves
    
    def get_castling_moves(self, king):
        """Get castling moves for a king (not in check, not through check)"""
        moves = []
        
        if king.has_moved or self.is_in_check(king.color):
            return moves
        
        # Kingside castling (right)
        rook_col = 7
        if self.board[king.row][rook_col] is not None:
            rook = self.board[king.row][rook_col]
            if isinstance(rook, Rook) and rook.color == king.color and not rook.has_moved:
                if (self.board[king.row][5] is None and 
                    self.board[king.row][6] is None):
                    moves.append((king.row, 6))
        
        # Queenside castling (left)
        rook_col = 0
        if self.board[king.row][rook_col] is not None:
            rook = self.board[king.row][rook_col]
            if isinstance(rook, Rook) and rook.color == king.color and not rook.has_moved:
                if (self.board[king.row][1] is None and 
                    self.board[king.row][2] is None and
                    self.board[king.row][3] is None):
                    moves.append((king.row, 2))
        
        return moves
    
    def is_checkmate(self, color, board=None):
        """Check if a color is in checkmate"""
        if board is None:
            board = self.board
        
        if not self.is_in_check(color, board):
            return False
        
        # Check if there are any legal moves
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece is not None and piece.color == color:
                    legal_moves = self.get_legal_moves(piece, board)
                    if legal_moves:
                        return False
        
        return True
    
    def is_stalemate(self, color, board=None):
        """Check if a color is in stalemate (not in check but no legal moves)"""
        if board is None:
            board = self.board
        
        # Must NOT be in check
        if self.is_in_check(color, board):
            return False
        
        # Check if there are any legal moves
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece is not None and piece.color == color:
                    legal_moves = self.get_legal_moves(piece, board)
                    if legal_moves:
                        return False
        
        return True
    
    def board_to_hashable(self):
        """Convert board state to a hashable representation for move history"""
        state = []
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece is None:
                    state.append('.')
                else:
                    code = piece.get_code()
                    state.append(code)
        return tuple(state)
    
    def is_draw_by_repetition(self):
        """Check if the same position has occurred 3 times"""
        current_state = self.board_to_hashable()
        repetitions = self.move_history.count(current_state)
        return repetitions >= 3
    
    def move_piece(self, from_pos, to_pos):
        """Move a piece from one square to another, handling special moves"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        piece = self.board[from_row][from_col]
        from_notation = self.board_to_chess_notation(from_row, from_col)
        to_notation = self.board_to_chess_notation(to_row, to_col)
        
        # Handle en passant
        if isinstance(piece, Pawn) and self.board[to_row][to_col] is None and from_col != to_col:
            captured_pawn = self.board[from_row][to_col]
            self.board[from_row][to_col] = None
            print(f"En passant! Captured pawn at {self.board_to_chess_notation(from_row, to_col)}")
        
        # Handle castling
        elif isinstance(piece, King) and abs(from_col - to_col) == 2:
            if to_col > from_col:  # Kingside
                rook = self.board[from_row][7]
                self.board[from_row][7] = None
                self.board[from_row][5] = rook
                rook.col = 5
                rook.has_moved = True
                print("Kingside castling!")
            else:  # Queenside
                rook = self.board[from_row][0]
                self.board[from_row][0] = None
                self.board[from_row][3] = rook
                rook.col = 3
                rook.has_moved = True
                print("Queenside castling!")
        
        # Normal move
        self.board[from_row][from_col] = None
        self.board[to_row][to_col] = piece
        
        piece.row = to_row
        piece.col = to_col
        piece.has_moved = True
        
        # Handle pawn promotion
        if isinstance(piece, Pawn):
            if (piece.color == 'white' and to_row == 0) or (piece.color == 'black' and to_row == 7):
                self.board[to_row][to_col] = Queen(piece.color, to_row, to_col)
                print(f"Pawn promoted to Queen at {to_notation}!")
        
        self.last_move = (from_pos, to_pos)
        self.current_turn = 'black' if self.current_turn == 'white' else 'white'
        
        # Track move history and halfmove clock
        self.move_history.append(self.board_to_hashable())
        
        # Reset halfmove clock on pawn moves or captures
        if isinstance(piece, Pawn) or self.board[to_row][to_col] is not None:
            self.halfmove_clock = 0
        else:
            self.halfmove_clock += 1
        
        # Check game state
        if self.is_stalemate(self.current_turn):
            self.game_over = True
            print(f"Stalemate! The game is a draw.")
        elif self.is_draw_by_repetition():
            self.game_over = True
            print(f"Draw by repetition!")
        elif self.halfmove_clock >= 100:  # 50-move rule
            self.game_over = True
            print(f"Draw by 50-move rule!")
        elif self.is_checkmate(self.current_turn):
            self.game_over = True
            self.checkmate = True
            print(f"Checkmate! {self.current_turn.capitalize()} loses!")
        elif self.is_in_check(self.current_turn):
            print(f"{self.current_turn.capitalize()} is in check!")
        else:
            print(f"Moved {piece.type} from {from_notation} to {to_notation}. {self.current_turn.capitalize()}'s turn.")