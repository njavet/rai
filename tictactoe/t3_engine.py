"""
Game engine for Tic-Tac-Toe

Description of the game state:
------------------------------
    
The fields in the board are addressed with single numbers in the following way:

   0|1|2
   -----
   3|4|5
   -----
   6|7|8

A board is encoded as a string of single characters of length 9, for example:
    
   '   XO    '
    012345678 (<- field numbers)

where empty fields are marked by ' ', Xs are marked by 'X' and Os by 'O'. In
the example, there's X on field 4 and an O on field 5 (the middle position).

The complete game state equals the current board configuration because the 
question who's turn it is can be deduced from the number of empty fields: it is 
X's turn iif the number of free fields is 9/7/5/3/1 -> uneven; otherwise it is 
O's turn.
"""
from rich.text import Text
from rich.console import Console


def insert_symbol(board, symbol, field):
    """
    Return a new BOARD by inserting the character SYMBOL at the index position 
    FIELD-1.
    """
    return board[:field] + symbol + board[field+1:]


def make_move(board, field, symbol):
    """
    make_move(board, field, symbol) executes the move indicated by its
    parameters:
        The SYMBOL ('X' or 'O') is put into the indicated FIELD (1-9) of a new 
        BOARD (encoding: see above), if this is a valid move.
        The function returns the new BOARD if the move is valid; '' otherwise.
    """
    i_field = int(field)
    if 0 <= i_field < 9:
        if symbol == 'X' or symbol == 'O':
            # valid move if field is still empty
            if board[i_field] == ' ':
                return insert_symbol(board, symbol, i_field)
    # something was invalid
    return '' 


def evaluate(board):

    # check rows
    rows = [board[0:3], board[3:6], board[6:9]]
    if any(r == 'XXX' for r in rows):
        return True, 'X', 1
    elif any(r == 'OOO' for r in rows):
        return True, 'O', -1

    # check cols
    cols = [board[::3], board[1::3], board[2::3]]
    if any(c == 'XXX' for c in cols):
        return True, 'X', 1
    elif any(c == 'OOO' for c in cols):
        return True, 'O', -1

    # check diags
    diags = [board[::4], board[2:-1:2]]
    if any(d == 'XXX' for d in diags):
        return True, 'X', 1
    elif any(d == 'OOO' for d in diags):
        return True, 'O', -1

    # check draw (board full):
    if count_symbol(board, ' ') == 0:
        return True, 'Nobody', 0

    # otherwise: game not over
    return False, 'Nobody', 0


def evaluate_prof(board):
    """
    evluate(board) indicates if a game is over, and if so, who has won. To 
    simplify things, a game is only over when one either player has won (3 in a 
    row / column / diagonal), or the board is full (in this case it is draw).
    evaluate(board) returns a tupel (OVER?, WHO_WON, REWARD):
        The first entry indicates (TRUE/FALSE) if the game has reached a final 
        state.
        The second entry indicates who one (either 'X' or 'O').
        The third entry indicates who has won (from X's perspective, if the 
        first entry is TRUE): +1 indicates a win for X, -1 a win for O, an 0 a 
        draw
    """
    # check rows:
    for i in range(3):    
        if board[i*3]==board[i*3+1] and board[i*3]==board[i*3+2] and board[i*3]!=' ':
            if board[i*3]=='X':
                return (True, 'X', +1)
            else:
                return (True, 'O', -1)
            
    # check cols:
    for i in range(3):    
        if board[i]==board[i+3] and board[i]==board[i+6] and board[i]!=' ':
            if board[i]=='X':
                return (True, 'X', +1)
            else:
                return (True, 'O', -1)
            
    # check diagonals:
    if board[0]==board[4] and board[0]==board[8] and board[0]!=' ': #down diag
        if board[0]=='X':
            return (True, 'X', +1)
        else:
            return (True, 'O', -1)                
    if board[6]==board[4] and board[6]==board[2] and board[6]!=' ': #up diag
        if board[6]=='X':
            return (True, 'X', +1)
        else:
            return (True, 'O', -1)
        
    # check draw (board full):
    if count_symbol(board, ' ') == 0:
        return True, 'Nobody', 0
    
    # otherwise: game not over
    return False, 'Nobody', 0


def count_symbol(board, symbol):
    """
    Returns the number SYMBOLs on the BOARD
    """
    return board.count(symbol)


def whos_turn(board):
    """
    Returns the SYMBOL of the player who's turn it is: it is X's turn iif the 
    number of free fields is 9/7/5/3/1 -> uneven; otherwise it is O's turn.
    """
    free_fields = count_symbol(board, ' ')
    # i.e., free_field is uneven
    if free_fields % 2 == 0:
        return 'O'
    else:
        return 'X'

    
def get_initial_board():
    """
    Returns an empty BOARD so that a user does not need to have knowledge of 
    its encoding.
    """
    return 9 * ' '


def print_board(board, console=None, with_numbers=True):
    """
    Pretty-prints the BOARD in the way described above (Description of the game 
    state). If IF_NUMBERS == True, the emtpy fields are printed with their 
    respective field numbers.
    """
    if console is None:
        console = Console()
    if with_numbers:
        # replace ' ' by field-number
        board = ''.join([str(i) if board[i] == ' ' else board[i] for i in range(9)])

    t0 = Text('|'.join([*board[0:3]]) + '\n-----\n')
    t1 = Text('|'.join([*board[3:6]]) + '\n-----\n')
    t2 = Text('|'.join([*board[6:9]]))
    console.print('\n-----\n'.join([
        '|'.join([*board[0:3]]),
        '|'.join([*board[3:6]]),
        '|'.join([*board[6:9]])
    ]))


def print_help(console=None):
    """
    Print a help text for a potential user as how to address fields in the 
    board.
    """
    if console is None:
        console = Console()

    console.print("The fields in the board are addressed with "
                  "single numbers in the following way:")
    console.print('0|1|2')
    console.print('-----')
    console.print('3|4|5')
    console.print('-----')
    console.print('6|7|8')

