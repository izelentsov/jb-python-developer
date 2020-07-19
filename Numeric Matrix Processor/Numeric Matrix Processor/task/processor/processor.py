ACT_EXIT = 0
ACT_ADD = 1
ACT_SCALE = 2
ACT_MULT = 3


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
        print()


def menu():
    print('1. Add matrices')
    print('2. Multiply matrix by a constant')
    print('3. Multiply matrices')
    print('0. Exit')
    return int(input('Your choice: '))


def do_addition():
    m1 = read_matrix('first')
    m2 = read_matrix('second')
    res = msum(m1, m2)
    if res is not None:
        print('The result is:')
        print_matrix(res)
    else:
        print('ERROR')


def do_scale():
    m = read_matrix('')
    c = read_const()
    res = mscale(m, c)
    print('The result is:')
    print_matrix(res)


def do_mult():
    m1 = read_matrix('first')
    m2 = read_matrix('second')
    res = mmult(m1, m2)
    if res is not None:
        print('The result is:')
        print_matrix(res)
    else:
        print('ERROR')


def read_matrix(label):
    msg = f'Enter size of {label} matrix: '
    rows, cols = [int(s) for s in input(msg).split()[:2]]

    print(f'Enter {label} matrix:')
    m = []
    for r in range(rows):
        row = [float(n) for n in input().split()[:cols]]
        m.append(row)
    return m


def read_const():
    return int(input('Enter constant: '))


def msum(m1, m2):
    rows = len(m1)
    cols = len(m1[0])
    if rows == len(m2) and cols == len(m2[0]):
        return [[(m1[i][j] + m2[i][j]) for j in range(cols)] for i in range(rows)]
    else:
        return None


def mscale(m, c):
    return [[(cell * c) for cell in row] for row in m]


def mmult(m1, m2):
    rows1 = len(m1)
    cols1 = len(m1[0])
    rows2 = len(m2)
    cols2 = len(m2[0])
    if cols1 != rows2:
        return None

    res = []
    for i in range(rows1):
        row = []
        for j in range(cols2):
            cell = sum([(m1[i][k] * m2[k][j]) for k in range(cols1)])
            row.append(cell)
        res.append(row)
    return res


def print_matrix(m):
    for row in m:
        print(' '.join([str(n) for n in row]))


main()
