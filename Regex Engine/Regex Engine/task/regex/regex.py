# write your code here
def run():
    toks = input().split("|")
    res = check(toks[0], toks[1])
    print(res)


def check(re, s):
    if re == '':
        return True
    if s == '':
        return False
    if re == '.':
        return True
    return re == s


run()
