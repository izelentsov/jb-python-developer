import math
import argparse
import sys


TYPE_ANNUITY = 'annuity'
TYPE_DIFF = 'diff'

ANN_PRINCIPAL = 'p'
ANN_PAYMENT = 'a'
ANN_PERIODS = 'n'
ANN_INTEREST = 'i'


class Params:
    def __init__(self, principal, payment, periods, interest):
        self.principal = principal
        self.payment = payment
        self.periods = periods
        self.interest = interest

    def what(self):
        if not self.principal:
            return ANN_PRINCIPAL
        if not self.payment:
            return ANN_PAYMENT
        if not self.periods:
            return ANN_PERIODS
        return None


def main():

    args = parse_args()
    if not args_good(args):
        print('Incorrect parameters')
        return

    if args.type == TYPE_ANNUITY:
        annuity(args)
    elif args.type == TYPE_DIFF:
        diff(args)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--type")
    parser.add_argument("--payment", type=float)
    parser.add_argument("--principal", type=float)
    parser.add_argument("--periods", type=float)
    parser.add_argument("--interest", type=float)
    return parser.parse_args()


def args_good(args):
    if not args.type or args.type != TYPE_ANNUITY and args.type != TYPE_DIFF:
        return False
    if args.type == TYPE_DIFF and args.payment:
        return False
    if len(sys.argv) < 4:
        return False
    if args.type == TYPE_ANNUITY and not args.interest:
        return False
    return True


def annuity(args):
    params = Params(args.principal, args.payment, args.periods, args.interest)
    what = params.what()
    if what == ANN_PERIODS:
        calculate_periods(params)
    elif what == ANN_PAYMENT:
        calculate_monthly_payment(params)
    else:
        calculate_principal(params)


def calculate_periods(p):
    rate = p.interest / 100.0 / 12
    months = math.ceil(math.log(p.payment / (p.payment - rate * p.principal), 1 + rate))
    ym = years_and_months(months)
    print('')
    print(f'It takes {ym} to repay the credit!')
    over = math.ceil(p.payment * months - p.principal)
    print(f'Overpayment = {over}')


def calculate_monthly_payment(p):
    rate = p.interest / 100.0 / 12
    xn = (1 + rate) ** p.periods
    pay = math.ceil(p.principal * (rate * xn) / (xn - 1))
    print(f'Your annuity payment = {pay}!')
    over = math.ceil(pay * p.periods - p.principal)
    print(f'Overpayment = {over}')


def calculate_principal(p):
    rate = p.interest / 100.0 / 12
    xn = (1 + rate) ** p.periods
    pr = p.payment / ((rate * xn) / (xn - 1))
    print('')
    print(f'Your credit principal = {math.floor(pr)}!')
    over = math.ceil(p.payment * p.periods - pr)
    print(f'Overpayment = {over}')


def years_and_months(months):
    years = months // 12
    m = months % 12
    text = ''
    if years > 0:
        text += n_smth(years, 'year')
    if m > 0:
        if len(text) > 0:
            text += ' and '
        text += n_smth(m, 'month')
    return text


def n_smth(n, smth):
    s = smth if n == 1 else smth + 's'
    return f'{n} {s}'


def diff(args):
    total = 0
    for m in range(int(args.periods)):
        dm = math.ceil(diff_payment(m + 1, args.principal, args.periods, args.interest))
        print(f'Month {m + 1}: paid out {dm}')
        total += dm
    over = math.ceil(total - args.principal)
    print(f'Overpayment = {over}')


def diff_payment(m, p, n, interest):
    i = interest / 100.0 / 12
    return p / n + i * (p - p * (m - 1) / n)


main()
