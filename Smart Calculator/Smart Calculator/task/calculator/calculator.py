# write your code here

TYPE_NONE = 0
TYPE_CMD = 1
TYPE_ASSIGN = 2
TYPE_EXPR = 3

CMD_EXIT = "exit"
CMD_HELP = "help"


def main():
    var = {}
    while True:
        inp_type, inp = read_input()
        stop = process_input(inp_type, inp, var)
        if stop:
            break
    print('Bye!')


def read_input():
    line = input().strip()
    if line.startswith('/'):
        return TYPE_CMD, line[1:]
    if len(line) == 0:
        return TYPE_NONE, None
    if "=" in line:
        return TYPE_ASSIGN, line
    return TYPE_EXPR, line


def process_input(inp_type, inp, var):
    stop = False
    if inp_type == TYPE_CMD:
        stop = do_cmd(inp)
    elif inp_type == TYPE_ASSIGN:
        try_process_assign(inp, var)
    elif inp_type == TYPE_EXPR:
        try_process_expr(inp, var)
    return stop


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


def try_process_assign(inp, var):
    toks = inp.split(sep='=')
    if len(toks) != 2:
        print("Invalid assignment")
        return
    left = toks[0].strip()
    right = toks[1].strip()
    if not is_valid_identifier(left):
        print("Invalid identifier")
        return
    if not is_int_literal(right) and not is_valid_identifier(right):
        print("Invalid assignment")
        return
    rval = value_of_term(right, var)
    if rval is not None:
        var[left] = rval


def is_valid_identifier(term):
    return all(c.isalpha() for c in term)


def try_process_expr(expr, var):
    res = None
    try:
        res = evaluate_expr(expr, var)
    except ValueError:
        print("Invalid expression")
        res = None
    finally:
        if res is not None:
            print(res)


def evaluate_expr(expr, var):
    buf = None
    op = None
    toks = expr.split()
    for term in toks:
        if not buf:
            buf = value_of_term(term, var)
            if buf is None:
                return None
        elif not op:
            op = simplify_op(term)
            if not op:
                print("Invalid expression")
                return None
        else:
            val2 = value_of_term(term, var)
            if val2 is None:
                return None
            buf = evaluate(op, buf, val2)
            op = None
    return buf


def value_of_term(term, var):
    if is_int_literal(term):
        return int(term)
    if is_known_var(term, var):
        return var[term]
    print("Unknown variable")
    return None


def is_int_literal(term):
    return all(c.isdigit() for c in term)


def is_known_var(v, var):
    return v in var


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
