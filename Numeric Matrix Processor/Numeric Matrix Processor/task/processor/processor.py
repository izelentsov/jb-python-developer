ACT_EXIT = 0
ACT_ADD = 1
ACT_SCALE = 2
ACT_MULT = 3
ACT_TRANSPOSE = 4
ACT_DETERMINANT = 5
ACT_INVERSE = 6

TRANS_MAIN = 1
TRANS_SIDE = 2
TRANS_VERT = 3
TRANS_HOR = 4


class Matrix:
    def __init__(self, cells):
        self.cells = cells
        self.rows = len(cells)
        self.cols = len(cells[0])

    def add(self, m2):
        if self.rows == m2.rows and self.cols == m2.cols:
            res = [[(self.cells[i][j] + m2.cells[i][j]) for j in range(self.cols)]
                   for i in range(self.rows)]
            return Matrix(res)
        else:
            return None

    def scale(self, c):
        return Matrix([[(cell * c) for cell in row] for row in self.cells])

    def mult(self, m2):
        if self.cols != m2.rows:
            return None
        res = []
        for i in range(self.rows):
            row = []
            for j in range(m2.cols):
                cell = sum([(self.cells[i][k] * m2.cells[k][j]) for k in range(self.cols)])
                row.append(cell)
            res.append(row)
        return Matrix(res)

    def transpose_main(self):
        res = [[self.cells[i][j] for i in range(self.rows)] for j in range(self.cols)]
        return Matrix(res)

    def transpose_side(self):
        res = [[self.cells[-i - 1][-j - 1] for i in range(self.rows)] for j in range(self.cols)]
        return Matrix(res)

    def transpose_vert(self):
        res = [[self.cells[i][-j - 1] for j in range(self.cols)] for i in range(self.rows)]
        return Matrix(res)

    def transpose_hor(self):
        res = [[self.cells[-i - 1][j] for j in range(self.cols)] for i in range(self.rows)]
        return Matrix(res)

    def det(self):
        if self.rows != self.cols:
            return None
        if self.rows == 1:
            return self.cells[0][0]
        if self.rows == 2:
            return self.cells[0][0] * self.cells[1][1] - \
                   self.cells[0][1] * self.cells[1][0]
        return sum([self.cells[i][0] * self.cofactor(i, 0) for i in range(self.rows)])

    def cofactor(self, i, j):
        return self.minor(i, j) * ((-1) ** (i + j))

    def minor(self, i, j):
        return self.submatrix(i, j).det()

    def submatrix(self, row, col):
        res = [[self.cells[i][j] for j in range(self.cols) if j != col]
               for i in range(self.rows) if i != row]
        return Matrix(res)

    def inverse(self):
        det = self.det()
        if det == 0:
            return None
        c = self.all_cofactors()
        return c.transpose_main().scale(1.0 / det)

    def all_cofactors(self):
        c = [[self.cofactor(i, j) for j in range(self.cols)] for i in range(self.rows)]
        return Matrix(c)

    def __str__(self):
        res = ''
        for row in self.cells:
            res += (' '.join([str(n) for n in row]) + '\n')
        return res


def main():
    while True:
        action = menu()
        if action == ACT_EXIT:
            break
        elif action == ACT_ADD:
            do_addition()
        elif action == ACT_SCALE:
            do_scale()
        elif action == ACT_MULT:
            do_mult()
        elif action == ACT_TRANSPOSE:
            transpose_menu()
        elif action == ACT_DETERMINANT:
            do_determinant()
        elif action == ACT_INVERSE:
            do_inverse()
        print()


def menu():
    print('1. Add matrices')
    print('2. Multiply matrix by a constant')
    print('3. Multiply matrices')
    print('4. Transpose matrix')
    print('5. Calculate determinant')
    print('6. Inverse matrix')
    print('0. Exit')
    return int(input('Your choice: '))


def do_addition():
    m1 = read_matrix('first')
    m2 = read_matrix('second')
    res = m1.add(m2)
    if res is not None:
        print('The result is:')
        print_matrix(res)
    else:
        print('ERROR')


def do_scale():
    m = read_matrix('')
    c = read_const()
    res = m.scale(c)
    print('The result is:')
    print_matrix(res)


def do_mult():
    m1 = read_matrix('first')
    m2 = read_matrix('second')
    res = m1.mult(m2)
    if res is not None:
        print('The result is:')
        print_matrix(res)
    else:
        print('ERROR')


def do_determinant():
    m = read_matrix('')
    res = m.det()
    print('The result is:')
    print_matrix(res)


def do_inverse():
    m = read_matrix('')
    res = m.inverse()
    if res is not None:
        print('The result is:')
        print_matrix(res)
    else:
        print("This matrix doesn't have an inverse.")


def read_matrix(label):
    msg = f'Enter size of {label} matrix: '
    rows, cols = [int(s) for s in input(msg).split()[:2]]

    print(f'Enter {label} matrix:')
    m = []
    for r in range(rows):
        row = [float(n) for n in input().split()[:cols]]
        m.append(row)
    return Matrix(m)


def read_const():
    return int(input('Enter constant: '))


def print_matrix(m):
    print(str(m))


def transpose_menu():
    print()
    print('1. Main diagonal')
    print('2. Side diagonal')
    print('3. Vertical line')
    print('4. Horizontal line')
    action = int(input('Your choice: '))
    m = read_matrix('')
    res = None
    if action == TRANS_MAIN:
        res = m.transpose_main()
    elif action == TRANS_SIDE:
        res = m.transpose_side()
    elif action == TRANS_VERT:
        res = m.transpose_vert()
    elif action == TRANS_HOR:
        res = m.transpose_hor()

    if res is not None:
        print('The result is:')
        print_matrix(res)


main()
