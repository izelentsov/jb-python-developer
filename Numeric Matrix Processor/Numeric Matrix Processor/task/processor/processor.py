def main():
    m1 = read_matrix()
    m2 = read_matrix()
    res = msum(m1, m2)
    if res is not None:
        print_matrix(res)
    else:
        print('ERROR')


def read_matrix():
    rows, cols = [int(s) for s in input().split()[:2]]
    m = []
    for r in range(rows):
        row = [int(n) for n in input().split()[:cols]]
        m.append(row)
    return m


def msum(m1, m2):
    rows = len(m1)
    cols = len(m1[0])
    if rows == len(m2) and cols == len(m2[0]):
        return [[(m1[i][j] + m2[i][j]) for j in range(cols)] for i in range(rows)]
    else:
        return None


def print_matrix(m):
    for row in m:
        print(' '.join([str(n) for n in row]))


main()
