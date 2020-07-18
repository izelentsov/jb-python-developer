# Write your code here

import random

CMD_NEXT = 0
CMD_STOP = 1

ACT_EXIT = 0
ACT_CREATE = 1
ACT_LOGIN = 2

ACT_CARD_EXIT = 0
ACT_CARD_BALANCE = 1
ACT_CARD_LOGOUT = 2

db = {}


class Card:
    def __init__(self, num, pin, balance=0):
        self.num = num
        self.pin = pin
        self.balance = balance


def main():
    active = None
    while True:
        if active is None:
            active, cmd = main_menu()
        else:
            active, cmd = card_menu(active)
        print()
        if cmd == CMD_STOP:
            break


def main_menu():
    action = ask_action()
    print()
    if action == ACT_CREATE:
        create_account()
        return None, CMD_NEXT
    elif action == ACT_LOGIN:
        card = login()
        return card, CMD_NEXT
    elif action == ACT_EXIT:
        return None, CMD_STOP
    print()


def ask_action():
    print('1. Create an account')
    print('2. Log into account')
    print('0. Exit')

    try:
        action = int(input())
    except ValueError:
        print("Cannot parse")
        return None
    else:
        if ACT_EXIT <= action <= ACT_LOGIN:
            return action
        else:
            print("Invalid option")
            return None


def create_account():
    num = generate_card_num()
    pin = generate_pin()
    card = Card(num, pin, 0)
    print('Your card has been created')
    print('Your card number:')
    print(num)
    print('Your card PIN:')
    print(pin)
    save(card)


def generate_card_num():
    bid = [4, 0, 0, 0, 0, 0]
    aid = [random.randint(0, 9) for _ in range(9)]
    num = bid + aid
    luhn = calc_luhn(num)
    checksum = 10 - luhn % 10
    num.append(checksum)
    return ''.join([str(x) for x in num])


def calc_luhn(num):
    res = 0
    for n in range(0, len(num)):
        if n % 2 == 0:
            x = num[n] * 2
            res += x if x <= 9 else x - 9
        else:
            res += num[n]
    return res


def generate_pin():
    return ''.join([str(random.randint(0, 9)) for _ in range(4)])


def save(card):
    db[card.num] = card


def login():
    card = input('Enter your card number: ')
    pin = input('Enter your PIN: ')
    print()
    if card in db and pin == db[card].pin:
        print('You have successfully logged in!')
        return db[card]
    else:
        print('Wrong card number or PIN!')
        return None


def card_menu(card):
    action = ask_card_action()
    print()
    if action == ACT_CARD_EXIT:
        return None, CMD_STOP
    elif action == ACT_CARD_BALANCE:
        print_balance(card)
        return card, CMD_NEXT
    elif action == ACT_CARD_LOGOUT:
        print('You have successfully logged out!')
        return None, CMD_NEXT


def ask_card_action():
    print('1. Balance')
    print('2. Log out')
    print('0. Exit')

    try:
        action = int(input())
    except ValueError:
        print("Cannot parse")
        return None
    else:
        if ACT_CARD_EXIT <= action <= ACT_CARD_LOGOUT:
            return action
        else:
            print("Invalid option")
            return None


def print_balance(card):
    print(f'Balance: {card.balance}')


main()
