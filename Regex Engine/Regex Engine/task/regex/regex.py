# write your code here

def run():
    toks = input().split("|")
    res = check(toks[0], toks[1])
    print(res)


def check(re, s):
#    print("check", re, s)
    if re == '':
        return True
    if re[0] == '^':
        return match(re[1:], s, 0)
    return find(re, s)


def find(re, s):
    for i in range(len(s)):
        if match(re, s[i:], 0):
            return True
    return False


def match(re, s, running):
    # print(re, "|", s)
    if re == '':
        return True
    if re == '$':
        return s == ''

    op = ''
    if len(re) > 1:
        op = re[1]

    if op == '?':
        cons_re, cons_s = match_question(re, s)
    elif op == '*':
        cons_re, cons_s = match_star(re, s)
    elif op == '+':
        cons_re, cons_s = match_plus(re, s, running)
    else:
        cons_re, cons_s = match_one(re, s)

    if cons_re == 0:
        running += cons_s
    else:
        running = 0

    # print("cons_re", cons_re, "cons_s", cons_s, "running", running)
    res = (cons_re > 0 or cons_s > 0) and match(re[cons_re:], s[cons_s:], running)

    # if star or plus applied and failed, try consume it and proceed
    if not res and cons_re == 0 and cons_s > 0:
        cons_re = 2
        cons_s = 1
        running = 0
        res = match(re[cons_re:], s[cons_s:], running)

    return res


def match_one(re, s):
    if match_char(re, s):
        return 1, 1
    return 0, 0


def match_question(re, s):
    if match_char(re, s):
        return 2, 1
    return 2, 0


def match_star(re, s):
    if match_char(re, s):
        return 0, 1
    return 2, 0


def match_plus(re, s, running):
    if match_char(re, s):
        return 0, 1
    if running == 0:
        return 0, 0
    return 2, 0


def match_char(re, s):
    return s != '' and (re[0] == '.' or re[0] == s[0])


run()
