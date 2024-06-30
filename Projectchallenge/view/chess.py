#we are making game a chess with python by using pygame module
import pygame
from constants import *

#draw main game board
def draw_board():
    for i in range(32):     # 32/4 = 8 which means it is making a chess board
        column=i%4
        row=i//4
        if row%2==0:
            pygame.draw.rect(screen,'GRAY',[600-(column*200), row*100,100,100]) # this is for drawing the boxes in chess game
        else:
            pygame.draw.rect(screen,'GRAY',[700-(column*200), row*100,100,100])
    # this is written as[x position,y position, width of screen or board,tall/height of board or screen]
    # height is 900 and boxes cover 800 so 100 is left whight is taken as rect
    # widht=1000 and height=900 and 5 here is border size
    #same case here for width
        pygame.draw.rect(screen,'gray',[0,800,width,100])   
        pygame.draw.rect(screen,'gray',[800,0,200,height])   
        pygame.draw.rect(screen,'black',[0,800,width,100],5) 
        pygame.draw.rect(screen,'black',[800,0,200,height],5)
        status_text=['White: Select a Piece to move!','White: Select a Destination!',
                     'Black: Select a Piece to move!','Black: Select a Destination!'] 
        screen.blit(big_font.render(status_text[turn_step],True,'black'),(20,820))  #the above text is written in rect inside border part
        for i in range(9): #start from 0 and end to 8 hence 0 to 800(for chess pieces boxes)
            pygame.draw.line(screen,'black',(0,100*i),(800,100*i),2)   #drawing border on boxes of chess piece
            pygame.draw.line(screen,'black',(100*i,0),(100*i,800),2)   # this is also same as x position and y position type
        screen.blit(medium_font.render('RESIGN',True,'black'),(825,830))
        if white_promo or black_promo:
            pygame.draw.rect(screen,'gray',[0,800,width - 200,100])  
            pygame.draw.rect(screen,'snow',[0,800,width - 200,100],5)  
            screen.blit(big_font.render('SELECT PIECE TO PROMOTE',True,'black'),(20,820))  #the above text is written in rect inside border part

# draw pieces onto board
def draw_pieces():
    for i in range(len(white_pieces)):
        index = piece_list.index(white_pieces[i])   #the piece that we had made is not in order but white_pieces is in order 
                                                    #so we had arranged piece_list according to white pieces by taking it in loop
        if white_pieces[i] == 'pawn':
            screen.blit(white_pawn, (white_location[i][0] * 100 + 13, white_location[i][1] *100 +19)) # 13(x position) and 19(y position) type will gives pieces location just centre in boxes and this can differnt in different devices.
        else:           # above is for pawns and below is for rook, knight ,etc.
            screen.blit(white_images[index], (white_location[i][0] * 100 + 15, white_location[i][1] *100 +20))
        if turn_step <2:
            if selection ==i:
                pygame.draw.rect(screen,'red',[white_location[i][0]*100+1 , white_location[i][1]*100+1,100,100],2)
    
    
    for i in range(len(black_pieces)):
        index = piece_list.index(black_pieces[i])   #the piece that we had made is not in order but black_pieces is in order 
                                                    #so we had arranged piece_list according to black pieces by taking it in loop
        if black_pieces[i] == 'pawn':
            screen.blit(black_pawn, (black_location[i][0] * 100 + 13, black_location[i][1] *100 +19)) # 13(x position) and 19(y position) type will gives pieces location just centre in boxes and this can differnt in different devices.
        else:           # above is for pawns and below is for rook, knight ,etc.
            screen.blit(black_images[index], (black_location[i][0] * 100 + 15, black_location[i][1] *100 +20))
        if turn_step >=2:
            if selection ==i:
                pygame.draw.rect(screen,'purple',[black_location[i][0]*100+1 , black_location[i][1]*100+1,100,100],2)
            
# function to check all pieces valid options on board
def check_options(pieces,locations,turn):
    global castling_moves
    moves_list = []
    all_moves_list = []
    castling_moves = []
    for i in range((len(pieces))):
        location = locations[i]
        piece = pieces[i]
        if piece =="pawn":
            moves_list = check_pawn(location,turn)
        elif piece == "rook":                             #this is done for moving valid piece from its location and turn.
             moves_list=check_rook(location,turn)
        elif piece == "knight":
            moves_list=check_knight(location,turn)
        elif piece == "bishop":
            moves_list=check_bishop(location,turn)  #all check_piece(name) are a function which is made after this every piece
        elif piece == "king":
            moves_list, castling_moves = check_king(location,turn)  # two variables are returning   
        elif piece == "queen":
            moves_list = check_queen(location,turn)
        all_moves_list.append(moves_list)
    return all_moves_list

#check rook moves
def check_rook(position, color):    #when rook moves up then y coordinate will decrease and for down it increase(remember)
    moves_list = []
    if color == 'white':
        enemies_list = black_location
        friends_list = white_location  # this is for giving idea to rook who is enemy
    else:
        friends_list = black_location
        enemies_list = white_location
        
    for i in range(4): # this is for rook movement(down=0, up=1, right=2, left=3)
        path = True
        chain = 1 # this is for moving straight (either vertical or horizontal move by multiplyting with how many squares)
        if i == 0:  #for down
            x = 0
            y = 1 #increasing
        elif i == 1: #for up
            x = 0   
            y = -1  #decreasing
        elif i == 2:    #for right
            x = 1   #increasing
            y = 0
        else:
            x = -1              # for horizontal direction we know y =0 and hence chain*y=0 and similarly for vertical x=0 and hence chain*x=0
            y = 0               
        while path:
            if(position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and\
                0 <= position[0] + (chain*x) <= 7 and 0 <= position[1] + (chain*y) <= 7: #position[0] is for x position and position[1] is for y position 
                moves_list.append((position[0] + (chain * x) , position[1] + (chain*y))) # and we have give range in between it is applicable that is 0 to 7 
                if(position[0] + (chain * x), position[1] + (chain * y)) in enemies_list: # and this x and y multiply with chain to move more squares
                    path = False    # this is for when enemy is there in rook side then it not move in that direction (only it can terminate it) 
                chain+=1   # this is for next chain(path) where it will move and again it will come into while loop and again condition will run 
            else:              
                path = False
                    
    return moves_list
    
# check valid piece move of pawn
def check_pawn(position, color):
    moves_list = []
    if color == 'white':    # for white pawn
        if (position[0], position[1] + 1) not in white_location and \
                (position[0], position[1] + 1) not in black_location and position[1] < 7:   # this is pawn first one move
            moves_list.append((position[0], position[1] + 1))
            if (position[0], position[1] + 2) not in white_location and \
                    (position[0], position[1] + 2) not in black_location and position[1] == 1:  #this is pawn first two moves
                moves_list.append((position[0], position[1] + 2))
        if (position[0] + 1, position[1] + 1) in black_location:   
            moves_list.append((position[0] + 1, position[1] + 1))    # this is for taking any opponent piece(black) diagonally
        if (position[0] - 1, position[1] + 1) in black_location:
            moves_list.append((position[0] - 1, position[1] + 1))
        # for en-passant move checking and adding of black piece capturing by white piece
        if (position[0] + 1, position[1] + 1) == black_ep:   
            moves_list.append((position[0] + 1, position[1] + 1))    # this is for taking any opponent piece(black) diagonally
        if (position[0] - 1, position[1] + 1) == black_ep:  # white pawn will take black pawn if black pawn moved only starting two move
            moves_list.append((position[0] - 1, position[1] + 1))
    else:
        if (position[0], position[1] - 1) not in white_location and \
                (position[0], position[1] - 1) not in black_location and position[1] > 0:
            moves_list.append((position[0], position[1] - 1))   #for black pawn
            if (position[0], position[1] - 2) not in white_location and \
                    (position[0], position[1] - 2) not in black_location and position[1] == 6:
                moves_list.append((position[0], position[1] - 2))
        if (position[0] + 1, position[1] - 1) in white_location:
            moves_list.append((position[0] + 1, position[1] - 1))
        if (position[0] - 1, position[1] - 1) in white_location:
            moves_list.append((position[0] - 1, position[1] - 1))
        # adding en passant move of black capturing of white 
        if (position[0] + 1, position[1] - 1) == white_ep:  # this is for taking any opponent piece(white) diagonally
            moves_list.append((position[0] + 1, position[1] - 1))
        if (position[0] - 1, position[1] - 1) == white_ep:  # black pawn will take white pawn if white pawn moved only starting two move
            moves_list.append((position[0] - 1, position[1] - 1))
    return moves_list

#checking if there is an en-passant popular move or not (en-passant occur only in pawn with opponent pawn not with other pieces)
def check_en(old_coords, new_coords):
    if turn_step <= 1:  #for white turn and this will check en passant move when white move starting two move only and black is there 
        index = white_location.index(old_coords)    #at adjacent of white then black will move forward(just behind of that white) which called en-passant
        ep_coords = (new_coords[0], new_coords[1] - 1)  #that's why this coordinate is used which see by black for enpassant check of white
        piece = white_pieces[index] # this is in tuple(X,Y) (in which we cannot update or modify)
    else:   #for black turn 
        index = black_location.index(old_coords)
        ep_coords = (new_coords[0], new_coords[1] + 1)  # this is also in tuple(X,Y) in which it moves 1 forth
        piece = black_pieces[index] # here white will see en passant move of black which is 1 move more like black is on 5th and white see e.p. as 6th coordin.
    if piece == 'pawn' and abs(old_coords[1] - new_coords[1]) > 1:
        pass
    else:
        ep_coords = (100,100)   # this we are giving default when there will be no en passant move
    return ep_coords    
        
#check valid piece move of knight..
def check_knight(position,color):
    moves_list=[]
    if color == 'white':
        enemies_list = black_location
        friends_list = white_location  # this is for giving idea to knight who is enemy on our side
    else:
        friends_list = black_location
        enemies_list = white_location
        # we know knight has 8 squares to check, they can go 2 squares in one direction and one in adjacent (means two up or down and one in right or left )
    targets = [(1,2),(1,-2),(2,1),(2,-1),(-1,2),(-1,-2),(-2,1),(-2,-1)] # THESE are 8 corners where night can go (x,y) form it is 
                                                                            # in (1,2)-> 2 is in downward position and it cannot be (2,1) {REMEMBER}
    for i in range(8):
        target = (position[0] + targets[i][0] , position[1] + targets[i][1]) #this will give all direction where knight can move target[i][0] give x side direction 
                    # and target[i][1] will give y side direction   ( is i=0 then (1,2) will come) and in targets[i][0] if i=0 and (1,2) come then it will take x coordinate only
                # and similarly y side take y coordinate only due to [0] and [1] written after [i]    
        if target not in friends_list and 0 <= target[0] <=7 and 0 <= target[1] <= 7:
             moves_list.append(target)
    return moves_list                                                               

#check valid piece move of bishop
def check_bishop(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_location
        friends_list = white_location  # this is for giving idea to bishop who is enemy on our side
    else:
        friends_list = black_location
        enemies_list = white_location
    for i in range(4): # this is for bishop movement(up-right=0, up-left=1, down-right=2, down-left=3)
        path = True
        chain = 1 
        if i == 0:  #for down
            x = 1
            y = -1 #increasing
        elif i == 1: #for up
            x = -1  
            y = -1  #decreasing
        elif i == 2:    #for right
            x = 1   #increasing
            y = 1
        else:
            x = -1            
            y = 1
        while path:
            if(position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and\
                0 <= position[0] + (chain*x) <= 7 and 0 <= position[1] + (chain*y) <= 7: #position[0] is for x position and position[1] is for y position 
                moves_list.append((position[0] + (chain * x) , position[1] + (chain*y))) # and we have give range in between it is applicable that is 0 to 7 (valid squares)
                if(position[0] + (chain * x), position[1] + (chain * y)) in enemies_list: # and this x and y multiply with chain to move more squares
                    path = False    # this is for when enemy is there in bishop side then it not move in that direction (only it can terminate it) 
                chain+=1   # this is for next chain(path) where it will move and again it will come into while loop and again condition will run 
            else:              
                path = False
    return moves_list

#CHECK valid piece move of king
def check_king(position,color):  #it is like queen but can take only 1 square
    moves_list = []
    castle_moves = check_castling()
    if color == 'white':
        enemies_list = black_location
        friends_list = white_location  # this is for giving idea to king who is enemy
    else:
        friends_list = black_location
        enemies_list = white_location
        # we know knight has 8 squares to check in which it can take only 1 square in any direction (all things are same as knight only coordinates is changes)
    targets = [(1,0),(-1,0),(0,1),(0,-1),(-1,1),(-1,-1),(1,1),(1,-1)] # THESE are 8 corners where king can go (x,y) form it is 
    for i in range(8):
        target = (position[0] + targets[i][0] , position[1] + targets[i][1]) #this will give all direction where king can move(target[i][0] give x side direction
        #and target[i][1] give y side direction 
        if target not in friends_list and 0 <= target[0] <=7 and 0 <= target[1] <= 7:
             moves_list.append(target)
    return moves_list, castle_moves

#check valid piece move of queen
def check_queen(position,color):    #queen moves is a combination of rook and bishop moves so that's why two list is taken 
    moves_list=check_bishop(position,color)
    second_list=check_rook(position,color)  #at last we appended second_list to moves_list and become a single list.
    for i in range(len(second_list)):
        moves_list.append(second_list[i])
    
    return moves_list

#check for valid moves for a selected piece.
def check_valid_moves():
    if turn_step < 2:
        options_list = white_options
    else:
        options_list = black_options
    valid_options = options_list[selection]
    return valid_options

#draw valid moves on screen
def draw_valid(moves):
    if turn_step < 2:
        color = 'red'
    else:
        color = 'blue'
    for i in range(len(moves)):
        pygame.draw.circle(screen, color, (moves[i][0] * 100 + 50, moves[i][1] * 100 + 50), 5)
        
#draw captured pieces on side of screen
def draw_captured():
    # for black piece captured
    for i in range(len(captured_pieces_white)):
        captured_piece = captured_pieces_white[i]
        index = piece_list.index(captured_piece)
        screen.blit(small_black_images[index], (825, 5 + 50 * i)) #this is coordination of black piece captured
    #for white piece captured
    for i in range(len(captured_pieces_black)):
        captured_piece = captured_pieces_black[i]
        index = piece_list.index(captured_piece)
        screen.blit(small_white_images[index], (925, 5 + 50 * i))   #this is coordination of white piece captured

#draw a flashing square around king when it is in check
def draw_check():
    global check
    check = False
    if turn_step < 2: #for white moves
        if 'king' in white_pieces:
            king_index = white_pieces.index('king') #for white king
            king_location = white_location[king_index] # for white king location 
            for i in range(len(black_options)): # this black options include all black pieces with location and moves.
                if king_location in black_options[i]:   # when black covered white king
                    check = True
                    if counter < 15:
                        pygame.draw.rect(screen, 'dark red', [white_location[king_index][0] * 100 + 1, white_location[king_index][1] * 100 + 1, 100, 100], 5) # 0 is for x coordinate and 1 is for y coordinate
    # this maths is written in [xcoordinate, ycoordinate,width, height]
    else: #for black moves
        if 'king' in black_pieces:
            king_index = black_pieces.index('king') #for black king
            king_location = black_location[king_index] # for black king location 
            for i in range(len(white_options)): # this white options include all white pieces with location and moves.
                if king_location in white_options[i]:   # when white covered black king
                    check = True
                    if counter < 15:
                        pygame.draw.rect(screen, 'dark blue', [black_location[king_index][0] * 100 + 1, black_location[king_index][1] * 100 + 1, 100, 100], 5) # 0 is for x coordinate and 1 is for y coordinate

def draw_game_over():
    pygame.draw.rect(screen,'black', [200,400,400,70])
    screen.blit(font.render(f'{winner} WON THE GAME',True,'white'), (210,410))
    screen.blit(font.render(f'PRESS ENTER TO RESTART THE GAME',True,'white'), (210,440))
    
# check and add castling
def check_castling():
    #before castling here are rules: - 
    ''' 1 -> king should not be in checked  2-> both rook and king not moved any one step previously 3-> nothing between and the king does not 
    pass through or finished on an attacked piece '''
    castle_moves = []   #stores each valid castle moves [((king_coords, castle_coords))]    because we have sides to castle one is short and other is long
    rook_indexes = []
    rook_location = []
    king_index = 0  # this we giving initial for castling
    king_location = (0,0)   # this is taken as let type for castling
    if turn_step > 1: # for white
        for i in range(len(white_pieces)):
            if white_pieces[i] == 'rook':
                rook_indexes.append(white_moved[i]) # used to check whether rook is moved or not
                rook_location.append(white_location[i]) # used to get that white location at index i
            if white_pieces[i] == 'king':
                king_index = i
                king_location = white_location[i]   #same as rook
        if not white_moved[king_index] and False in rook_indexes and not check: # this is that where castling is valid and here check is variable which tells whether king is not in check
            for i in range(len(rook_indexes)):
                castle = True
                if rook_location[i][0] > king_location[0]:  # this is rook 1st and 2nd and comparison is between king with rook right side of king long side
                    empty_squares = [(king_location[0] + 1, king_location[1]),( king_location[0] + 2, king_location[1]), (king_location[0] + 3, king_location[1])]
                    # this is king all right side which needs to be empty for castling  here we overwrite coordinates of king as 0,0 but these not include pieces
                else:   # this is king left side where 2 pieces is there in between of rook and king
                    empty_squares = [(king_location[0] - 1, king_location[1]), (king_location[0] - 2, king_location[1])]
                for j in range(len(empty_squares)):
                    if empty_squares[j] in white_location or empty_squares[j] in black_location or empty_squares[j] in black_options or rook_indexes[i]:
                        castle = False  # these are False because if there is any piece exist between an king and rook then castle should not done
                if castle:
                    castle_moves.append((empty_squares[1], empty_squares[0]))
    else: # for black
        for i in range(len(black_pieces)):
            if black_pieces[i] == 'rook':
                rook_indexes.append(black_moved[i]) 
                rook_location.append(black_location[i]) # used to get that black location at index i
            if black_pieces[i] == 'king':
                king_index = i
                king_location = black_location[i]   #same as rook
        if not black_moved[king_index] and False in rook_indexes and not check: 
            for i in range(len(rook_indexes)):
                castle = True
                if rook_location[i][0] > king_location[0]:  
                    empty_squares = [(king_location[0] + 1, king_location[1]),( king_location[0] + 2, king_location[1]), (king_location[0] + 3, king_location[1])]
                    #this will same as white
                else:   
                    empty_squares = [(king_location[0] - 1, king_location[1]), (king_location[0] - 2, king_location[1])]
                for j in range(len(empty_squares)):
                    if empty_squares[j] in black_location or empty_squares[j] in white_location or empty_squares[j] in white_options or rook_indexes[i]:
                        castle = False  # these are False because if there is any piece exist between an king and rook then castle should not done
                if castle:
                    castle_moves.append((empty_squares[1], empty_squares[0]))
    return castle_moves

#draw castling
def draw_castling(moves):
    if turn_step > 2:
        color = 'blue'
    else:
        color = 'red'
    for i in range(len(moves)):
        pygame.draw.circle(screen, color, (moves[i][0][0] * 100 + 50, moves[i][0][1] * 100 + 70), 8)
        screen.blit(font.render('king', True, 'black'), (moves[i][0][0] * 100 + 30, moves[i][0][1] * 100 + 70)) # this is drawing circles at moves (sides of king)
        pygame.draw.circle(screen, color, (moves[i][1][0] * 100 + 50, moves[i][1][1] * 100 + 70), 8)
        screen.blit(font.render('rook', True, 'black'),(moves[i][1][0] * 100 + 30, moves[i][1][1] * 100 + 70))  # this is drawing circles at moves (sides of king)
        pygame.draw.line(screen, color, (moves[i][0][0] * 100 + 50, moves[i][0][1] * 100 + 70),(moves[i][1][0] * 100 + 50, moves[i][1][1] * 100 + 70), 2)

#add pawn promotion 
def check_promotion():
    pawn_indexes = []   # this is simple pawn index 
    white_promotion = False # for white piece promotion
    black_promotion = False  # for black piece promotion
    promote_index = 100     # index where it promote
    for i in range(len(white_pieces)):
        if white_pieces[i] == 'pawn':
            pawn_indexes.append(i)  # this will take index of pawn not coordinates
    for i in range(len(pawn_indexes)):  # promotion/simple pawn indexes
        if white_location[pawn_indexes[i]][1] == 7: # this will take coordinate of one by one pawn_index[i] means all pawns index one by one 
            white_promotion = True                  # and if any become equal to 7 then that pawn will be promoted to any powerful white piece
            promote_index = pawn_indexes[i] # this will take promoted pawn index (because it is in if condition)
    pawn_indexes = []
    
    for i in range(len(black_pieces)):
        if black_pieces[i] == 'pawn':
            pawn_indexes.append(i)      # this is for black pawn promotion difference is index where pawn promoted is at white side i.e 0.
    for i in range(len(pawn_indexes)):  
        if black_location[pawn_indexes[i]][1] == 0: 
            black_promotion = True                  
            promote_index = pawn_indexes[i] 
    pawn_indexes = []
    return white_promotion, black_promotion, promote_index        
            
def draw_promotion():
    pygame.draw.rect(screen, 'dark gray', [800, 0 , 200, 420])
    if white_promo:
        color = 'white'
        for i in range(len(white_promotions_pieces)):
            piece = white_promotions_pieces[i]  # this will store pieces
            index = piece_list.index(piece) # this will take index of above specific pieces from main piece_list because it is stored as images also
            screen.blit(white_images[index], (860, 5 + 100 * i))    # here we are taking images of specific pieces and storing it in box which we made
    elif black_promo:
        color = 'black'
        for i in range(len(black_promotions_pieces)):
            piece = black_promotions_pieces[i]  # this will store pieces
            index = piece_list.index(piece) # this will take index of above specific pieces from main piece_list because it is stored as images also
            screen.blit(black_images[index], (860, 5 + 100 * i))
    pygame.draw.rect(screen, color , [800, 0 , 200, 420], 6)
    
def check_promo_select():
    mouse_pos = pygame.mouse.get_pos()
    left_click = pygame.mouse.get_pressed()[0]  # this is for clicking with mouse of promoting pieces
    x_pos = mouse_pos[0] // 100
    y_pos = mouse_pos[1] // 100
    if white_promo and left_click and x_pos > 7 and y_pos < 4:  # in this x_pos > 7 means that it will click inside promoting pieces boxes
        white_pieces[promo_index] = white_promotions_pieces[y_pos] # and y_pos < 4 means to click only that specific four pieces
        # this will click on specific pieces and select that piece and overwrite on pawn piece which is promoted
    elif black_promo and left_click and x_pos > 7 and y_pos < 4:  # in this x_pos > 7 means that it will click inside promoting pieces boxes
        black_pieces[promo_index] = black_promotions_pieces[y_pos] # and y_pos < 4 means to click only that specific four pieces
        
# main game tool
black_options = check_options(black_pieces, black_location,'black')
white_options = check_options(white_pieces, white_location,'white')
run=True
while run:
    timer.tick(fps)
    if counter < 30:
        counter += 1
    else:
        counter = 0
    screen.fill("SKY BLUE")    # no other colour it will give error 
    draw_board()
    draw_pieces()
    draw_captured()
    draw_check()
    if not game_over:   # this is made because if pawn is at promotion promotion and if game over then due to iteration it will run again 
        #that's why we made this which will run only when there is no game over
        white_promo , black_promo, promo_index = check_promotion()  # white_promo get white_promotion value and so on...
    if white_promo or black_promo:
        draw_promotion()    # this is for giving only image of pieces at pawn promotion
        check_promo_select()    # this is for promote piece selection 
    if selection!=100:
        valid_moves=check_valid_moves()
        draw_valid(valid_moves) 
        if selected_piece == 'king':
            draw_castling(castling_moves)
          
#event handling
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:
            x_coord=event.pos[0]//100
            y_coord=event.pos[1]//100
            click_coords = (x_coord,y_coord)    # this is all about handling player piece selection.(means when player click piece then it should only move)

# turn step=0 is for white_piece and turn_step=2 is for black_piece
    #this whole includes movement of pieces and taking pieces by different methode
            if turn_step<=1:
                if click_coords == (8,8) or click_coords == (9,8):
                    winner = 'BLACK'
                if click_coords in white_location:                  # at line 31 taken turn_step = 0
                    selection = white_location.index(click_coords)  # at line 32 we had taken selection = 100
                    #checking that which piece is selected for castling move so we do castling when at end king is selected
                    selected_piece = white_pieces[selection]
                    if turn_step == 0:
                        turn_step=1
                if click_coords in valid_moves and selection != 100:    # at line 33 valid moves = []
                    white_ep = check_en(white_location[selection],click_coords)# here selection give old coordinates and after we click give new_coordinate
                    white_location[selection]=click_coords  # this is used for checking any piece is moved at index before castling 
                                                            #because for castling we need king and rook and between both no piece should be there
                    white_moved[selection] = True   
                    if click_coords in black_location:
                        black_piece = black_location.index(click_coords)    # both captures_pieces_white and captured_pieces_black is empty that's why we first putting value in black_piece and then append in captured
                        captured_pieces_white.append(black_pieces[black_piece])  # this is for black piece which is captured by white piece
                        if black_pieces[black_piece] == 'king':
                            winner = 'WHITE'
                        black_pieces.pop(black_piece)  #pop is used to eliminate hence black piece is eliminated
                        black_location.pop(black_piece) # black_location is also eliminated
                        black_moved.pop(black_piece)
                        
                    # for en-passant of white which is checking by black
                    if click_coords == black_ep:
                        black_piece = black_location.index((black_ep[0], black_ep[1] - 1)) 
                        captured_pieces_white.append(black_pieces[black_piece]) 
                        black_pieces.pop(black_piece)  
                        black_location.pop(black_piece) 
                        black_moved.pop(black_piece)
                    black_options = check_options(black_pieces, black_location,'black')
                    white_options = check_options(white_pieces, white_location, 'white') 
                    turn_step = 2
                    selection =100  # this again written for new turn/move
                    valid_moves = []
            
                # add option to castling in white
                elif selection != 100 and selected_piece == 'king':  # this is added because castling will not come in valid move its has its own move in between two and three squares.
                    for q in range(len(castling_moves)):
                        if click_coords == castling_moves[q][0]:
                            white_location[selection] = click_coords     
                            white_moved[selection] = True # this is for not doing castling again
                            if click_coords == (1,0):
                                rook_coords = (0,0)
                            else:
                                rook_coords = (7,0)
                            rook_indexes = white_location.index(rook_coords)
                            white_location[rook_indexes] = castling_moves[q][1]    #this is for applying the castling..
                            black_options = check_options(black_pieces, black_location,'black')
                            white_options = check_options(white_pieces, white_location, 'white') 
                            turn_step = 2
                            selection =100  # this again written for new turn/move
                            valid_moves = []
                      
        #this whole includes movement of pieces and taking pieces by different methode                              
            if turn_step > 1:
                if click_coords == (8,8) or click_coords == (9,8):
                    winner = 'WHITE'
                if click_coords in black_location:                  # above line taken turn_step = 2
                    selection = black_location.index(click_coords)  # above line  we had taken selection = 100
                    #checking that which piece is selected for castling move so we do castling when at end king is selected
                    selected_piece = black_pieces[selection]
                    if turn_step == 2:
                        turn_step=3
                if click_coords in valid_moves and selection != 100:    # above line valid moves = []
                    black_ep = check_en(black_location[selection],click_coords)
                    black_location[selection]=click_coords
                    black_moved[selection] = True
                    if click_coords in white_location:
                        white_piece = white_location.index(click_coords)    # both captures_pieces_white and captured_pieces_black is empty that's why we first putting value in white_piece and then append in captured
                        captured_pieces_black.append(white_pieces[white_piece])  # this is for black piece which is captured by white piece
                        if white_pieces[white_piece] == 'king':
                            winner = 'BLACK'
                        white_pieces.pop(white_piece)  #pop is used to eliminate hence white piece is eliminated
                        white_location.pop(white_piece) # white_location is also eliminated
                        white_moved.pop(white_piece)
                    # for en-passant of black which is checking by white
                    if click_coords == white_ep:
                        white_piece = white_location.index((white_ep[0], white_ep[1] + 1))  
                        captured_pieces_black.append(white_pieces[white_piece])
                        white_pieces.pop(white_piece)  
                        white_location.pop(white_piece) 
                        white_moved.pop(white_piece)
                    black_options = check_options(black_pieces, black_location,'black')
                    white_options = check_options(white_pieces, white_location, 'white') 
                    turn_step = 0
                    selection =100  # this again written for new turn/move
                    valid_moves = []
            # add option to castling in black
                elif selection != 100 and selected_piece == 'king':  # this is added because castling will not come in valid move its has its own move in between two and three squares.
                    for q in range(len(castling_moves)):
                         if click_coords == castling_moves[q][0]:
                            black_location[selection] = click_coords     
                            black_moved[selection] = True # this is for not doing castling again
                            if click_coords == (1,7):
                                rook_coords = (0,7)
                            else:
                                rook_coords = (7,7)
                            rook_indexes = black_location.index(rook_coords)
                            black_location[rook_indexes] = castling_moves[q][1]    #this is for applying the castling..
                            black_options = check_options(black_pieces, black_location,'black')
                            black_options = check_options(black_pieces, black_location, 'black') 
                            turn_step = 0
                            selection =100  # this again written for new turn/move
                            valid_moves = []
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_RETURN:    # helps in returning to program by pressing enter key.
                game_over = False   #after coming to restarting game game_over must be false
                winner = ''         #same things will occur (hence all thing will be in loop)
                white_pieces=["rook","knight","bishop","king","queen","bishop","knight","rook",
                              "pawn","pawn","pawn","pawn","pawn","pawn","pawn","pawn"] 
                white_location=[(0,0),(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),
                                (0,1),(1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(7,1)]     #this is position of chess pieces.
                white_moved = [False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False]

                black_pieces=["rook","knight","bishop","king","queen","bishop","knight","rook",
                            "pawn","pawn","pawn","pawn","pawn","pawn","pawn","pawn"] 
                black_location=[(0,7),(1,7),(2,7),(3,7),(4,7),(5,7),(6,7),(7,7),
                                (0,6),(1,6),(2,6),(3,6),(4,6),(5,6),(6,6),(7,6)]
                black_moved = [False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False]
                
                captured_pieces_white=[]
                captured_pieces_black=[]
                turn_step=0
                selection=100           #storing same things to re-initialize the whole after game over and then restart
                valid_moves=[]
                black_options = check_options(black_pieces, black_location,'black')
                white_options = check_options(white_pieces, white_location,'white')
    if winner != '':
        game_over = True
        draw_game_over()
    pygame.display.flip()
pygame.quit()