# Write your code here
import random


class Rules:
    def __init__(self, options):
        self.opts = options

    def is_valid(self, option):
        return option in self.opts

    def result(self, us, them):
        if us == them:
            return RES_DRAW
        i = self.opts.index(us)
        j = self.opts.index(them)
        half = (len(self.opts) - 1) / 2
        if i < j:
            if i + half < j:
                return RES_WIN
            return RES_LOSE
        else:
            if (i + 1 + half) % len(self.opts) < j:
                return RES_WIN
            return RES_LOSE


OPT_SCIS = 'scissors'
OPT_ROCK = 'rock'
OPT_PAPR = 'paper'

RES_WIN = 'win'
RES_DRAW = 'draw'
RES_LOSE = 'lose'

SCORES = {
    RES_WIN: 100,
    RES_DRAW: 50,
    RES_LOSE: 0
}


MSG = {RES_WIN: 'Well done. Computer chose {} and failed',
       RES_DRAW: 'There is a draw ({})',
       RES_LOSE: 'Sorry, but computer chose {}'}


def run():
    uname = input("Enter your name: ")
    print(f'Hello, {uname}')
    score = restore_rating(uname)
    rules = read_rules()
    print("Okay, let's start")

    while True:
        user_option = input()
        if user_option == '!exit':
            break
        if user_option == '!rating':
            print(f'Your rating: {score}')
            continue

        if rules.is_valid(user_option):
            score = play(user_option, rules, score)
        else:
            print('Invalid input')

    print('Bye!')


def restore_rating(name):
    f = open('rating.txt', 'r')
    r = dict()
    for line in f:
        u, rating = line.split()
        r[u] = int(rating)
    return r[name] if name in r else 0


def read_rules():
    line = input()
    if len(line.strip()) == 0:
        options = ['rock', 'paper', 'scissors']
    else:
        options = line.split(',')
    return Rules(options)


def play(user_option, rules, score):
    comp_option = choose(rules)
    res = rules.result(user_option, comp_option)
    score += score_for(res)
    print(msg(res, comp_option))
    return score


def choose(rules):
    return random.choice(rules.opts)


def score_for(res):
    return SCORES[res]


def msg(res, comp_opt):
    return MSG[res].format(comp_opt)


run()
