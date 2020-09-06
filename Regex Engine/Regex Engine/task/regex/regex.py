# write your code here
def run():
    toks = input().split("|")
    res = check(toks[0], toks[1])
    print(res)


def check(re, s):
    if (re == ''):
        return True
    if re[0] == '^':
        return match(re[1:], s)
    return find(re, s)


def find(re, s):
    re_len = len(re) - 1 if re[-1] == '$' else len(re)

    for i in range(len(s) - re_len + 1):
        if match(re, s[i:]):
            return True
    return False


def match(re, s):
    if re == '':
        return True
    if re == '$':
        return s == ''
    if s == '':
        return False

    return match_one(re[0], s[0]) and match(re[1:], s[1:])


def match_one(re, s):
    if re == '.':
        return True
    return re == s


run()
