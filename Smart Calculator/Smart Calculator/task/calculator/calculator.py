# write your code here

CMD_EXIT = "exit"
CMD_HELP = "help"


def main():
    while True:
        cmd, operands = read_input()
        if cmd == CMD_EXIT:
            break
        if cmd == CMD_HELP:
            print_help()
        if len(operands) > 0:
            print(sum(operands))
    print('Bye!')


def read_input():
    line = input().strip()
    if line.startswith('/'):
        return line[1:], []
    tokens = line.split()
    if len(tokens) >= 1:
        return None, [int(x) for x in tokens]
    return None, []


def print_help():
    print('The program calculates the sum of numbers')


main()
