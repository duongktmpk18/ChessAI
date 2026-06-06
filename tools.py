

from define import *

def cal_rect(bool, rect0, rect1):
    if bool:
        return (rect1 * PIECE_SIZE, rect0 * PIECE_SIZE)
    else:
        return (rect1 * PIECE_SIZE + PIECE_SIZE//2, rect0 * PIECE_SIZE + PIECE_SIZE//2)

def rev_rect(pos):
    # Calculate the offset like in draw_board
    offset_x = (SCREEN_SIZE - (10 * PIECE_SIZE)) // 2
    offset_y = (SCREEN_SIZE - (10 * PIECE_SIZE)) // 2
    
    # Adjust click position by subtracting offset
    adj_x = pos[0] - offset_x
    adj_y = pos[1] - offset_y
    
    return (adj_y // PIECE_SIZE, adj_x // PIECE_SIZE)

def eq(a, b):
    if a[0] == b[0] and a[1] == b[1]:
        return True
    return False

def check_valid(n, m):
    if (n >= 0 and n <= 7) and (m >= 0 and m <= 7):
        return True
    return False

def print_ar(ar):
    print("================================================")
    for i in ar:
        print(i)
    print("================================================")

def clean_selected(ar):
    for i in range(8):
        for j in range(8):
            if ar[i][j] == '..' or ar[i][j] == '...':
                ar[i][j] = '  '
            if ar[i][j][:2] == '.w' or ar[i][j][:2] == '.b':
                ar[i][j] = ar[i][j][1:]

def king_position(ar, type):
    king = type + 'k'
    for i in range(8):
        for j in range(8):
            if ar[i][j] == king:
                return (i,j)

def check_position(pos, min1, max1, min2, max2):
    if pos[0] >= min1 and pos[0] <= max1 and pos[1] >= min2 and pos[1] <= max2:
        return True
    return False
