# write your code here

CMD_EXIT = "exit"
CMD_HELP = "help"


def main():
    while True:
        cmd, expr = read_input()
        if cmd:
            stop = do_cmd(cmd)
            if stop:
                break
        if len(expr) > 0:
            try_process(expr)
    print('Bye!')


def read_input():
    line = input().strip()
    if line.startswith('/'):
        return line[1:], []
    tokens = line.split()
    if len(tokens) >= 1:
        return None, tokens
    return None, []


def do_cmd(cmd):
    if cmd == CMD_EXIT:
        return True
    if cmd == CMD_HELP:
        print_help()
    else:
        print("Unknown command")
    return False


def print_help():
    print('The program calculates expressions with additions and subtractions')


def try_process(expr):
    try:
        res = evaluate_expr(expr)
    except ValueError:
        res = None
    finally:
        if res is None:
            print("Invalid expression")
        else:
            print(res)


def evaluate_expr(expr):
    buf = None
    op = None
    for term in expr:
        if not buf:
            buf = int(term)
        elif not op:
            op = simplify_op(term)
            if not op:
                return None
        else:
            buf = evaluate(op, buf, int(term))
            op = None
    return buf


def simplify_op(op):
    if op.startswith("+") and all(c == "+" for c in op):
        return "+"
    if op.startswith("-") and all(c == "-" for c in op):
        return "-" if op.count("-") % 2 == 1 else "+"
    return None


def evaluate(op, a, b):
    if op == "-":
        return a - b
    if op == "+":
        return a + b
    return None


main()
