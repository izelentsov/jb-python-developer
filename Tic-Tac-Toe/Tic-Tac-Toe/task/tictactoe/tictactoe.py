# write your code here


def print_border():
    print('---------')


def print_row(state):
    print('|', ' '.join(state), "|")


def print_field(state):
    print_border()
    for row in state:
        print_row(row)
    print_border()


def str_to_state(s):
    cells = list(s)
    return [cells[0:3], cells[3:6], cells[6:9]]


def has_empty(state):
    for row in state:
        if '_' in row:
            return True
    return False


def all_three(row, side):
    for x in row:
        if x != side:
            return False
    return True


def column(state, i):
    return [x for row in state for x in row[i]]


def diag_top_left(state):
    d = []
    for i in range(len(state)):
        d.append(state[i][i])
    return d


def diag_top_right(state):
    d = []
    for i in range(len(state)):
        row = state[i]
        d.append(row[len(row) - i - 1])
    return d


def has_three(state, side):
    return all_three(state[0], side) or \
            all_three(state[1], side) or \
            all_three(state[2], side) or \
            all_three(column(state, 0), side) or \
            all_three(column(state, 1), side) or \
            all_three(column(state, 2), side) or \
            all_three(diag_top_left(state), side) or \
            all_three(diag_top_right(state), side)


def count(state, side):
    return len([x for row in state for x in row if x == side])


def game_status(state):
    x_wins = has_three(state, 'X')
    o_wins = has_three(state, 'O')
    finished = not has_empty(state)
    x_num = count(state, 'X')
    o_num = count(state, 'O')

    if abs(x_num - o_num) > 1 or (x_wins and o_wins):
        return 'Impossible'
    if x_wins:
        return 'X wins'
    if o_wins:
        return 'O wins'
    if finished:
        return 'Draw'
    else:
        return 'Game not finished'


def is_occupied(st, row, col):
    return st[row][col] != '_'


def parse_input(s, st):
    tokens = s.split()
    if len(tokens) != 2:
        return None, None, 'You should enter numbers!'
    if False in [t.isdigit() for t in tokens]:
        return None, None, 'You should enter numbers!'
    ux, uy = [int(t) for t in tokens]
    if ux < 1 or ux > 3 or uy < 1 or uy > 3:
        return None, None, 'Coordinates should be from 1 to 3!'

    row = 3 - uy
    col = ux - 1
    if is_occupied(st, row, col):
        return None, None, 'This cell is occupied! Choose another one!'
    else:
        return row, col, None


def move(st, row, col, side):
    st[row][col] = side


def make_move(st, side):
    while True:
        inp = input('Enter the coordinates: ')
        row, col, error = parse_input(inp, st)
        if error is not None:
            print(error)
            continue
        else:
            move(st, row, col, side)
            break


def turn(st, side):
    make_move(st, side)
    print_field(st)
    return game_status(st)

def run():
    st = str_to_state('_________')
    print_field(st)
    side = 'X'

    while True:
        status = turn(st, side)
        if status != 'Game not finished':
            break
        side = 'X' if side == 'O' else 'O'

    print(status)


run()
