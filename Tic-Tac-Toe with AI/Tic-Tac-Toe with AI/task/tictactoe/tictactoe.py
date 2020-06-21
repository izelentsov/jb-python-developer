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
    "user": lambda field, ui: UserPlayer(field, ui, "user"),
    "easy": lambda field, ui: EasyAiPlayer(field, ui, "easy"),
    "medium": lambda field, ui: MediumAiPlayer(field, ui, "medium")
}

CMD_START = 0
CMD_EXIT = 1


def main():
    ui = UI()
    cmd, player1, player2 = ui.menu()
    if cmd == CMD_START:
        field = empty_field()
        p1 = make_player(player1, field, ui)
        p2 = make_player(player2, field, ui)
        game = Game(field, ui, p1, p2)
        game.play()


def empty_field():
    return Field([list("___"), list("___"), list("___")])


def make_player(player_type, field, ui):
    print(f'Making player {player_type}')
    return PLAYERS[player_type](field, ui)


class Player:
    def __init__(self, field, ui, level):
        self.field = field
        self.ui = ui
        self.level = level


class UserPlayer(Player):
    def move(self):
        move = None
        while not move:
            move = self.ui.ask_move()
            if self.field.is_occupied(move):
                print('This cell is occupied! Choose another one!')
                move = None
            else:
                break
        return move


class EasyAiPlayer(Player):
    def move(self):
        self.ui.print_move(self)
        empty = self.field.empty_cells()
        return random.choice(empty)


class MediumAiPlayer(Player):
    def move(self):
        self.ui.print_move(self)
        empty = self.field.empty_cells()
        return random.choice(empty)


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
                self.field.put(side, move)
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
        winner = self.get_winner()
        if winner == SIDE_O:
            return ST_O_WINS
        if winner == SIDE_X:
            return ST_X_WINS
        if self.field.has_blanks():
            return ST_NONE
        return ST_DRAW

    def get_winner(self):
        for row in self.field.cells:
            winner = self.who_strikes(row)
            if winner:
                return winner

        for x in range(3):
            col = [row[x] for row in self.field.cells]
            winner = self.who_strikes(col)
            if winner:
                return winner

        diag = [self.field.cells[x][x] for x in range(3)]
        winner = self.who_strikes(diag)
        if winner:
            return winner

        diag = [self.field.cells[x][2 - x] for x in range(3)]
        winner = self.who_strikes(diag)
        if winner:
            return winner
        return None

    def who_strikes(self, line):
        if all(c == SIDE_X for c in line):
            return SIDE_X
        if all(c == SIDE_O for c in line):
            return SIDE_O
        return None


class Field:
    def __init__(self, cells):
        self.cells = cells

    def has_blanks(self):
        return any(c == BLANK for row in self.cells for c in row)

    def count_side(self, side):
        return len([cell for row in self.cells for cell in row if cell == side])

    def is_occupied(self, xy):
        return self.cells[xy[1]][xy[0]] != BLANK

    def put(self, side, xy):
        self.cells[xy[1]][xy[0]] = side

    def empty_cells(self):
        empty = []
        for y in range(3):
            for x in range(3):
                if self.cells[y][x] == BLANK:
                    empty.append((x, y))
        return empty


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
        for r in f.cells:
            self.print_row(r)
        self.print_border()

    def print_border(self):
        print('-' * 9)

    def print_row(self, r):
        print('|', ' '.join(r), '|')

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
