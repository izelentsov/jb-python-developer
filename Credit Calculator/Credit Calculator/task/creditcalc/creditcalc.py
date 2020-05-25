import math


def main():
    principal = int(input('Enter the credit principal: '))
    print('What do you want to calculate?')
    print('type "m" - for count of months,')
    print('type "p" - for monthly payment')
    q = input()
    if q == 'm':
        calculate_months(principal)
    else:
        calculate_monthly_payment(principal)


def calculate_months(principal):
    pay = int(input('Enter monthly payment: '))
    months = math.ceil(principal / pay)
    print('')
    print(f'It takes {n_months(months)} months to repay the credit')


def calculate_monthly_payment(principal):
    months = int(input('Enter count of months: '))
    pay = math.ceil(principal / months)
    last = None
    if principal % months != 0:
        last = principal - (months - 1) * pay
    print('')
    print(f'Your monthly payment = {pay}' +
          (f' with last month payment = {last}' if last else ''))


def n_months(n):
    return f'{n} month' + ('s' if n > 1 else '')

main()
