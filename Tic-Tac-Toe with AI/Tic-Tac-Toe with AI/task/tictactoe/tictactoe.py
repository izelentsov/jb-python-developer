# write your code here
import random

SIDE_X = 'X'
SIDE_O = 'O'
BLANK = '_'

ST_NONE = 0
ST_DRAW = 1
ST_X_WINS = 2
ST_O_WINS = 3

PLAYERS = {
    "user": lambda field, ui, side: UserPlayer(field, ui, "user", side),
    "easy": lambda field, ui, side: EasyAiPlayer(field, ui, "easy", side),
    "medium": lambda field, ui, side: MediumAiPlayer(field, ui, "medium", side),
    "hard": lambda field, ui, side: HardAiPlayer(field, ui, "hard", side)
}

CMD_START = 0
CMD_EXIT = 1


def main():
    ui = UI()
    cmd, player1, player2 = ui.menu()
    if cmd == CMD_START:
        field = empty_field()
        p1 = make_player(player1, field, ui, SIDE_X)
        p2 = make_player(player2, field, ui, SIDE_O)
        game = Game(field, ui, p1, p2)
        game.play()


def empty_field():
    return Field(list("_________"))


def make_player(player_type, field, ui, side):
    return PLAYERS[player_type](field, ui, side)


class Player:
    def __init__(self, field, ui, level, side):
        self.field = field
        self.ui = ui
        self.level = level
        self.side = side


class UserPlayer(Player):
    def move(self):
        move = None
        while not move:
            move = self.ui.ask_move()
            if self.field.is_occupied(move[0], move[1]):
                print('This cell is occupied! Choose another one!')
                move = None
            else:
                break
        return move


class EasyAiPlayer(Player):
    def move(self):
        self.ui.print_move(self)
        move = random.choice(self.field.empty_cells())
        return move.x, move.y


class MediumAiPlayer(Player):
    def move(self):
        self.ui.print_move(self)

        lines = self.field.lines()

        win_lines = [line for line in lines if self.almost_won(line)]
        if len(win_lines) > 0:
            win_line = win_lines[0]
            move = win_line.find(BLANK)
            return move.x, move.y

        lose_lines = [line for line in lines if self.almost_lose(line)]
        if len(lose_lines) > 0:
            lose_line = lose_lines[0]
            move = lose_line.find(BLANK)
            return move.x, move.y

        move = random.choice(self.field.empty_cells())
        return move.x, move.y

    def almost_won(self, line):
        return self.almost_won_side(line, self.side)

    def almost_lose(self, line):
        return self.almost_won_side(line, self.op_side())

    def almost_won_side(self, line, side):
        return line.count_side(side) == 2 and line.count_side(BLANK) == 1

    def op_side(self):
        return SIDE_O if self.side == SIDE_X else SIDE_X


class HardAiPlayer(Player):
    def move(self):
        self.ui.print_move(self)
        if len(self.field.empty_cells()) == 9:
            move = random.choice(self.field.empty_cells())
        else:
            move = self.minimax(self.field, self.side).cell
        return move.x, move.y

    def minimax(self, field, cur_side):
        other_side = SIDE_X if cur_side == SIDE_O else SIDE_O

        winner = get_winner(field)
        if not field.has_blanks():
            if winner == self.side:
                return ScoredMove(None, 10)
            if winner == other_side:
                return ScoredMove(None, -10)
            return ScoredMove(None, 0)

        moves = [(cell, self.next_field(field, cell, cur_side)) for cell in field.empty_cells()]
        scored = [ScoredMove(move[0], self.minimax(move[1], other_side).score) for move in moves]
        best = self.best_move(scored, cur_side)
        return best

    def next_field(self, field, cell, side):
        res = field.clone()
        res.put(side, cell.x, cell.y)
        return res

    def best_move(self, scored, cur_side):
        best_score = -100 if cur_side == self.side else 100
        best_move = None
        for s in scored:
            if (cur_side == self.side and s.score > best_score) or \
                    (cur_side != self.side and s.score < best_score):
                best_score = s.score
                best_move = s
        return best_move


class ScoredMove:
    def __init__(self, cell, score):
        self.cell = cell
        self.score = score

    def __str__(self):
        return f"ScoredMove({str(self.cell)}, {self.score})"


class Game:
    def __init__(self, field, ui, p_x, p_o):
        self.field = field
        self.ui = ui
        self.p_x = p_x
        self.p_o = p_o

    def play(self):
        self.ui.print_field(self.field)
        state = self.game_state()

        while state == ST_NONE:
            side = self.whose_turn()
            move = self.next_move(side)
            if move:
                self.field.put(side, move[0], move[1])
                self.ui.print_field(self.field)
                state = self.game_state()
        self.ui.print_state(state)

    def whose_turn(self):
        xs = self.field.count_side(SIDE_X)
        os = self.field.count_side(SIDE_O)
        return SIDE_X if xs <= os else SIDE_O

    def next_move(self, side):
        p = self.p_x if side == SIDE_X else self.p_o
        return p.move()

    def game_state(self):
        winner = get_winner(self.field)
        if winner == SIDE_O:
            return ST_O_WINS
        if winner == SIDE_X:
            return ST_X_WINS
        if self.field.has_blanks():
            return ST_NONE
        return ST_DRAW


def get_winner(field):
    for line in field.lines():
        winner = who_strikes(line)
        if winner:
            return winner
    return None


def who_strikes(line):
    if line.count_side(SIDE_X) == 3:
        return SIDE_X
    if line.count_side(SIDE_O) == 3:
        return SIDE_O
    return None


class Field:
    def __init__(self, values):
        self.values = values

    def clone(self):
        return Field(list(self.values))

    def has_blanks(self):
        return any(c == BLANK for c in self.values)

    def count_side(self, side):
        return self.values.count(side)

    def ind(self, x, y):
        return y * 3 + x

    def get(self, x, y):
        return self.values[self.ind(x, y)]

    def cell(self, x, y):
        return Cell(x, y, self.get(x, y))

    def put(self, side, x, y):
        self.values[self.ind(x, y)] = side

    def is_occupied(self, x, y):
        return self.get(x, y) != BLANK

    def empty_cells(self):
        return [self.cell(x, y) for y in range(3) for x in range(3) if self.get(x, y) == BLANK]

    def rows(self):
        return [Line([self.cell(x, y) for x in range(3)]) for y in range(3)]

    def cols(self):
        return [Line([self.cell(x, y) for y in range(3)]) for x in range(3)]

    def diags(self):
        diag1 = Line([self.cell(x, x) for x in range(3)])
        diag2 = Line([self.cell(x, 2 - x) for x in range(3)])
        return [diag1, diag2]

    def lines(self):
        res = []
        res.extend(self.rows())
        res.extend(self.cols())
        res.extend(self.diags())
        return res


class Cell:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value

    def __str__(self):
        return f"Cell({self.x}, {self.y}, {self.value})"

    def __repr__(self):
        return f"Cell({self.x}, {self.y}, {self.value})"


class Line:
    def __init__(self, cells):
        self.cells = cells

    def count_side(self, side):
        return sum([cell.value == side for cell in self.cells])

    def find(self, side):
        for cell in self.cells:
            if cell.value == side:
                return cell
        return None

    def __repr__(self):
        return "Line({})".format(", ".join(str(cell) for cell in self.cells))


class UI:
    def __init__(self):
        pass

    def menu(self):
        cmd = None
        while cmd is None:
            inp = input("Input command: ")
            cmd, p1, p2 = self.parse_menu_input(inp)
            if cmd is not None:
                return cmd, p1, p2
            print("Bad Parameters!")

    def parse_menu_input(self, inp):
        toks = inp.split()
        if len(toks) == 0:
            return None, None, None
        cmd = toks[0]
        if cmd == "exit":
            return CMD_EXIT, None, None
        if cmd == "start":
            if len(toks) >= 3:
                p1 = toks[1]
                p2 = toks[2]
                if self.validate_players(p1, p2):
                    return CMD_START, p1, p2
        return None, None, None

    def validate_players(self, *players):
        return all(p in PLAYERS.keys() for p in players)

    def get_field(self):
        f = input('Enter cells: ')
        r1 = list(f[:3])
        r2 = list(f[3: 6])
        r3 = list(f[6:9])
        return Field([r1, r2, r3])

    def print_field(self, f):
        self.print_border()
        for r in f.rows():
            self.print_row(r)
        self.print_border()

    def print_border(self):
        print('-' * 9)

    def print_row(self, r):
        print('|', ' '.join([cell.value for cell in r.cells]), '|')

    def ask_move(self):
        move = None
        while not move:
            inp = input('Enter the coordinates: ')
            ux, uy = self.parse_input(inp)
            if ux is not None:
                return self.to_field_coords(ux, uy)

    def parse_input(self, inp):
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

    def to_field_coords(self, ux, uy):
        return ux - 1, 3 - uy

    def print_state(self, state):
        if state == ST_NONE:
            print('Game not finished')
        if state == ST_DRAW:
            print("Draw")
        if state == ST_X_WINS:
            print("X wins")
        if state == ST_O_WINS:
            print("O wins")

    def print_move(self, player):
        print(f'Making move level "{player.level}"')


main()
