import pygame
from pieces import *
from game import *
pygame.init()
WIDTH, HEIGHT = 600, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("chess")
WHITE = (255,255,255)
SQUARE_SIZE = 600 //8
DARK = (100, 150, 237)
LIGHT = (238, 238, 210)
def read_png(piece):
    img = pygame.image.load(f"assets/pieces/{piece}.png")
    img = pygame.transform.smoothscale(img, (SQUARE_SIZE,SQUARE_SIZE))
    return img

pieces_map = {
    "bb":read_png('bb'),
    "bk":read_png('bk'),
    "bn":read_png('bn'),
    "bq":read_png('bq'),
    "bp":read_png('bp'),
    "br":read_png('br'),
    "wb":read_png('wb'),
    "wp":read_png('wp'),
    "wk":read_png('wk'),
    "wq":read_png('wq'),
    "wn":read_png('wn'),
    "wr":read_png('wr')
}
initial_board = [
    ['br', 'bn', 'bb', 'bq', 'bk', 'bb', 'bn', 'br'],  # 8th rank (black back rank)
    ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],  # 7th rank (black pawns)
    ['', '', '', '', '', '', '', ''],                  # 6th rank
    ['', '', '', '', '', '', '', ''],                  # 5th rank  
    ['', '', '', '', '', '', '', ''],                  # 4th rank
    ['', '', '', '', '', '', '', ''],                  # 3rd rank
    ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],  # 2nd rank (white pawns)
    ['wr', 'wn', 'wb', 'wq', 'wk', 'wb', 'wn', 'wr']   # 1st rank (white back rank)
]


def draw_pieces():
    for row in range(8):
        for col in range(8):
            if initial_board[row][col] != "" :
                x = col * SQUARE_SIZE
                y = row * SQUARE_SIZE
                SCREEN.blit(pieces_map[initial_board[row][col]], (x,y))

def draw_board():
    for row in range(8):
        for col in range(8):
            x = col * SQUARE_SIZE
            y = row * SQUARE_SIZE
            color = LIGHT if (row+col)%2==0 else DARK
            pygame.draw.rect(SCREEN, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))





def main():
    game = ChessGame()
    running=True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    game.handle_click(event.pos)
                    
        
        draw_board()
        #draw_pieces(game.board)
        draw_pieces()
        pygame.display.flip()
    

    pygame.quit()






if __name__ == "__main__":
    main()