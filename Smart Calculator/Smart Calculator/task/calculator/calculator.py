# write your code here
from collections import deque


TYPE_NONE = 0
TYPE_CMD = 1
TYPE_ASSIGN = 2
TYPE_EXPR = 3

CMD_EXIT = "exit"
CMD_HELP = "help"

PRIORITIES = {
    1: ['+', '-'],
    2: ['*', '/']
}


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


def value_of_term(term, var):
    if is_int_literal(term):
        return int(term)
    if is_known_var(term, var):
        return var[term]
    print("Unknown variable", term)
    return None


def is_int_literal(term):
    return all(c.isdigit() for c in term)


def is_known_var(v, var):
    return v in var


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
    toks = tokenize(expr)
    postfix = to_postfix(toks)
    if postfix is not None:
        return eval_postfix(postfix, var)
    return None


def tokenize(expr):
    buf = deque()
    res = deque()
    op = None
    for c in expr:
        if c == ' ':
            flush(buf, op, res)
            op = None
        elif is_op(c):
            if c != op:
                flush(buf, op, res)
                op = c
            buf.append(c)
        elif is_paren(c):
            flush(buf, op, res)
            op = None
            res.append(c)
        else:
            if op is not None:
                flush(buf, op, res)
                op = None
            buf.append(c)

    flush(buf, op, res)
    return res


def flush(buf, op, res):
    if len(buf) > 0:
        tok = ''.join(buf)
        if op is not None:
            tok = simplify_op(tok)
        res.append(tok)
        buf.clear()


def simplify_op(op):
    if op.startswith("+") and all(c == "+" for c in op):
        return "+"
    if op.startswith("-") and all(c == "-" for c in op):
        return "-" if op.count("-") % 2 == 1 else "+"
    if op.startswith("*") and len(op) == 1:
        return "*"
    if op.startswith("/") and len(op) == 1:
        return "/"
    return None


def to_postfix(expr):
    res = deque()
    ops = deque()
    for tok in expr:
        if is_op(tok):
            res = op_to_postfix(tok, res, ops)
        elif is_paren(tok):
            res = paren_to_postfix(tok, res, ops)
        else:
            res.append(tok)
        # print('tok', tok)
        # print('res', res)
        # print('ops', ops)

        if res is None:
            return None

    if '(' in ops:
        print('Invalid expression')
        return None

    while len(ops) > 0:
        res.append(ops.pop())

    # print('res', res)
    # print('ops', ops)

    return res


def op_to_postfix(op, res, ops):
    if len(ops) == 0:
        ops.append(op)
    else:
        while len(ops) > 0:
            top = ops[-1]
            if lteq(op, top) and top != '(':
                res.append(ops.pop())
            else:
                break
        ops.append(op)
    return res


def lteq(op1, op2):
    return prio_of(op1) <= prio_of(op2)


def prio_of(op):
    for prio, ops in PRIORITIES.items():
        if op in ops:
            return prio
    return 0


def paren_to_postfix(paren, res, ops):
    if paren == '(':
        ops.append(paren)
    else:
        top = None
        while len(ops) > 0:
            top = ops.pop()
            if top != '(':
                res.append(top)
            else:
                break
        if top != '(':
            print('Invalid expression')
            return None
    return res


def is_op(c):
    return c in ['+', '-', '*', '/']


def is_paren(c):
    return c in ['(', ')']


def eval_postfix(postfix, var):
    # print('eval')
    res = deque()
    for term in postfix:
        if is_op(term):
            if len(res) < 2:
                print("Invalid expression")
                return None
            b = res.pop()
            a = res.pop()
            r = evaluate(term, a, b)
            res.append(r)
        else:
            val = value_of_term(term, var)
            if val is None:
                return None
            res.append(val)
        # print('term', term)
        # print('res', res)
    return res[-1]


def evaluate(op, a, b):
    if op == "-":
        return a - b
    if op == "+":
        return a + b
    if op == '*':
        return a * b
    if op == '/':
        return a // b
    return None


main()
