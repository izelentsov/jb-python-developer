# write your code here

SIDE_X = 'X'
SIDE_O = 'O'
BLANK = '_'

ST_NONE = 0
ST_DRAW = 1
ST_X_WINS = 2
ST_O_WINS = 3


def main():
    field = get_field()
    print_field(field)
    play(field)


def get_field():
    f = input('Enter cells: ')
    r1 = list(f[:3])
    r2 = list(f[3: 6])
    r3 = list(f[6:9])
    return [r1, r2, r3]


def print_field(f):
    print_line()
    for r in f:
        print_row(r)
    print_line()


def print_line():
    print('-' * 9)


def print_row(r):
    print('|', ' '.join(r), '|')


def play(f):
    side = whose_turn(f)
    move = ask_move(f)
    if move:
        make_move(f, side, move)
        print_field(f)
        state = game_state(f)
        print_state(state)


def whose_turn(f):
    xs = count_side(f, SIDE_X)
    os = count_side(f, SIDE_O)
    return SIDE_X if xs == os else SIDE_O


def count_side(f, side):
    return len([cell for row in f for cell in row if cell == side])


def ask_move(f):
    move = None
    while not move:
        inp = input('Enter the coordinates: ')
        ux, uy = parse_input(inp)
        if ux is not None:
            move = to_field_coords(ux, uy)
            if is_occupied(f, move):
                print('This cell is occupied! Choose another one!')
                move = None
            else:
                break
    return move


def parse_input(inp):
    # if any(not c.isdigit() for c in inp):
    #     print('You should enter numbers!')
    #     return None, None
    try:
        coords = [int(c) for c in inp.split(' ')]
    except ValueError:
        print('You should enter numbers!')
        return None, None

    if any(x < 1 or x > 3 for x in coords):
        print('Coordinates should be from 1 to 3!')
        return None, None

    return coords[0], coords[1]


def to_field_coords(ux, uy):
    return ux - 1, 3 - uy


def is_occupied(f, xy):
    return f[xy[1]][xy[0]] != BLANK


def make_move(f, side, move):
    f[move[1]][move[0]] = side


def game_state(f):
    winner = get_winner(f)
    if winner == SIDE_O:
        return ST_O_WINS
    if winner == SIDE_X:
        return ST_X_WINS
    if has_blanks(f):
        return ST_NONE
    return ST_DRAW


def get_winner(f):
    for row in f:
        winner = who_strikes(row)
        if winner:
            return winner

    for x in range(3):
        col = [row[x] for row in f]
        winner = who_strikes(col)
        if winner:
            return winner

    diag = [f[x][x] for x in range(3)]
    winner = who_strikes(diag)
    if winner:
        return winner

    diag = [f[x][2 - x] for x in range(3)]
    winner = who_strikes(diag)
    if winner:
        return winner

    return None


def has_blanks(f):
    return any(c == BLANK for row in f for c in row)


def who_strikes(line):
    if all(c == SIDE_X for c in line):
        return SIDE_X
    if all(c == SIDE_O for c in line):
        return SIDE_O
    return None


def print_state(state):
    if state == ST_NONE:
        print('Game not finished')
    if state == ST_DRAW:
        print("Draw")
    if state == ST_X_WINS:
        print("X wins")
    if state == ST_O_WINS:
        print("O wins")


main()
