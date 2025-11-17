class ChessGame:
    def __init__(self):
        self.board = []
        self.selected_piece = None
        self.current_turn = 'white'
        self.valid_moves = []
    
    def get_square_from_pos(self, pos):
        x, y = pos
        row = x // 75
        col = y // 75
        return row , col
    
    def handle_click(self, pos):
        row, col = self.get_square_from_pos(pos)
        print(f' row {row}, col {col}')
        """
        DO IT LATEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEERRRRRRRRRRRRRRRRRRRRRRRRR
        """




