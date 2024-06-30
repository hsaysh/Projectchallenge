import pygame
pygame.init()
width=1000              #for chess game ratio on my screen
height=890
screen=pygame.display.set_mode([width,height])
pygame.display.set_caption("One V/S One Chess!")
font=pygame.font.Font("freesansbold.ttf",20)
big_font=pygame.font.Font("freesansbold.ttf",50)  #this font is inbuilt and number is size
medium_font=pygame.font.Font("freesansbold.ttf",40)  #this font is inbuilt and number is size
timer=pygame.time.Clock()
fps=60

#game variables and images
white_pieces=['rook','knight','bishop','king','queen','bishop','knight','rook',
              'pawn','pawn','pawn','pawn','pawn','pawn','pawn','pawn'] 
white_promotions_pieces = ['bishop', 'knight', 'rook', 'queen']
white_location=[(0,0),(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),    #this is position of chess pieces.
                (0,1),(1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(7,1)]     #on upper side of chess board
white_moved = [False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False]

black_pieces=['rook','knight','bishop','king','queen','bishop','knight','rook',
              'pawn','pawn','pawn','pawn','pawn','pawn','pawn','pawn'] 
black_promotions_pieces = ['bishop', 'knight', 'rook', 'queen']
black_location=[(0,7),(1,7),(2,7),(3,7),(4,7),(5,7),(6,7),(7,7),
                (0,6),(1,6),(2,6),(3,6),(4,6),(5,6),(6,6),(7,6)]    #on lower side
black_moved = [False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False]

captured_pieces_white=[]
captured_pieces_black=[]
# 0-for white turn but with no selection, 1-for white turn with piece selected,
# 2-for black turn but without selection, 3-for black turn with piece selected 

turn_step=0
selection=100           # for storing selection of piece by their index
valid_moves=[]

#load a game pieces images(king,bishop,knight,queen,king,pawn) 2 times-> one for black and other for white
black_queen=pygame.image.load('chess_assets/images/black queen.png')
black_queen=pygame.transform.scale(black_queen,(80,80))     #for queen
black_queen_small=pygame.transform.scale(black_queen,(45,45))
black_king=pygame.image.load('chess_assets/images/black king.png')
black_king=pygame.transform.scale(black_king,(80,80))       #for king
black_king_small=pygame.transform.scale(black_king,(45,45))
black_rook=pygame.image.load('chess_assets/images/black rook.png')
black_rook=pygame.transform.scale(black_rook,(80,80))       #for rook
black_rook_small=pygame.transform.scale(black_rook,(45,45))
black_knight=pygame.image.load('chess_assets/images/black knight.png')
black_knight=pygame.transform.scale(black_knight,(80,80))       #for knight
black_knight_small=pygame.transform.scale(black_knight,(45,45))
black_bishop=pygame.image.load('chess_assets/images/black bishop.png')
black_bishop=pygame.transform.scale(black_bishop,(80,80))       #for bishop
black_bishop_small=pygame.transform.scale(black_bishop,(45,45))
black_pawn=pygame.image.load('chess_assets/images/black pawn.png')
black_pawn=pygame.transform.scale(black_pawn,(65,65))       #for pawn
black_pawn_small=pygame.transform.scale(black_pawn,(45,45))

white_queen=pygame.image.load('chess_assets/images/white queen.png')
white_queen=pygame.transform.scale(white_queen,(80,80))     #for queen
white_queen_small=pygame.transform.scale(white_queen,(45,45))
white_king=pygame.image.load('chess_assets/images/white king.png')
white_king=pygame.transform.scale(white_king,(80,80))       #for king
white_king_small=pygame.transform.scale(white_king,(45,45))
white_rook=pygame.image.load('chess_assets/images/white rook.png')
white_rook=pygame.transform.scale(white_rook,(80,80))       #for rook
white_rook_small=pygame.transform.scale(white_rook,(45,45))
white_knight=pygame.image.load('chess_assets/images/white knight.png')
white_knight=pygame.transform.scale(white_knight,(80,80))       #for knight
white_knight_small=pygame.transform.scale(white_knight,(45,45))
white_bishop=pygame.image.load('chess_assets/images/white bishop.png')
white_bishop=pygame.transform.scale(white_bishop,(80,80))       #for bishop
white_bishop_small=pygame.transform.scale(white_bishop,(45,45))
white_pawn=pygame.image.load('chess_assets/images/white pawn.png')
white_pawn=pygame.transform.scale(white_pawn,(65,65))       #for pawn
white_pawn_small=pygame.transform.scale(white_pawn,(45,45))

white_images=[white_pawn, white_queen, white_king, white_knight, white_rook, white_bishop]
small_white_images=[white_pawn_small, white_queen_small, white_king_small, white_knight_small, white_rook_small, white_bishop_small]
black_images=[black_pawn, black_queen, black_king, black_knight, black_rook, black_bishop]
small_black_images=[black_pawn_small, black_queen_small, black_king_small, black_knight_small, black_rook_small, black_bishop_small]

piece_list = ['pawn','queen','king','knight','rook','bishop']
#check variables/ flashing counter.
counter = 0
winner = ''
game_over = False
white_ep = (100,100)
black_ep = (100,100)    #this is taken when we have to check en passant move (valid only for first two move of pawn not single move also)
white_promo = False
black_promo = False
promo_index = 100
check = False
castling_moves = []