import pygame
from pieces import *
from game import *
from ai import ChessAI
import time

pygame.init()
WIDTH, HEIGHT = 600, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("chess")
WHITE = (255,255,255)
SQUARE_SIZE = 600 // 8
DARK = (100, 150, 237)
LIGHT = (238, 238, 210)

def read_png(piece):
    img = pygame.image.load(f"assets/pieces/{piece}.png")
    img = pygame.transform.smoothscale(img, (SQUARE_SIZE, SQUARE_SIZE))
    return img

pieces_map = {
    "bb": read_png('bb'),
    "bk": read_png('bk'),
    "bn": read_png('bn'),
    "bq": read_png('bq'),
    "bp": read_png('bp'),
    "br": read_png('br'),
    "wb": read_png('wb'),
    "wp": read_png('wp'),
    "wk": read_png('wk'),
    "wq": read_png('wq'),
    "wn": read_png('wn'),
    "wr": read_png('wr')
}

def draw_pieces(board):
    """Draw all pieces on the board"""
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece is not None:
                x = col * SQUARE_SIZE
                y = row * SQUARE_SIZE
                piece_code = piece.get_code()
                SCREEN.blit(pieces_map[piece_code], (x, y))

def draw_board():
    """Draw the checkerboard pattern"""
    for row in range(8):
        for col in range(8):
            x = col * SQUARE_SIZE
            y = row * SQUARE_SIZE
            color = LIGHT if (row + col) % 2 == 0 else DARK
            pygame.draw.rect(SCREEN, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))

def draw_valid_moves(valid_moves):
    """Highlight valid moves on the board"""
    for row, col in valid_moves:
        x = col * SQUARE_SIZE
        y = row * SQUARE_SIZE
        pygame.draw.circle(SCREEN, (255, 0, 0), (x + SQUARE_SIZE // 2, y + SQUARE_SIZE // 2), 5)

def main():
    game = ChessGame()
    ai = ChessAI('black', game)
    running = True
    clock = pygame.time.Clock()
    ai_thinking = False
    ai_move_time = 0
    last_move = None  # Track last move to avoid duplicate tracking
    
    while running:
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not game.game_over and game.current_turn == 'white':
                    game.handle_click(event.pos)
        
        # Track player moves
        if game.last_move and game.last_move != last_move:
            ai.track_move(game.last_move[0], game.last_move[1])
            last_move = game.last_move
        
        # AI's turn
        if game.current_turn == 'black' and not game.game_over and not ai_thinking:
            ai_thinking = True
            ai_move_time = time.time()
        
        if ai_thinking:
            # Give AI time to "think" (at least 0.5 seconds for realism)
            if time.time() - ai_move_time > 0.5:
                eval_score = ai.evaluate_position(game.board)
                print(f"Position evaluation: {eval_score:.2f}")
                ai.make_move()
                ai_thinking = False
        
        draw_board()
        draw_pieces(game.board)
        draw_valid_moves(game.valid_moves)
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()