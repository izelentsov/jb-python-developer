# Write your code here

import sqlite3
import random

CMD_NEXT = 0
CMD_STOP = 1

ACT_EXIT = 0
ACT_CREATE = 1
ACT_LOGIN = 2

ACT_CARD_EXIT = 0
ACT_CARD_BALANCE = 1
ACT_CARD_LOGOUT = 2


class Database:
    def __init__(self, conn):
        self.conn = conn
        self.cur = conn.cursor()
        self.cache = {}

    def create(self):
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS card (
              id INTEGER,
              number TEXT,
              pin TEXT,
              balance INTEGER DEFAULT 0
              );
            """)
        self.conn.commit()

    def add_card(self, card):
        self.cur.execute('INSERT INTO card (id, number, pin, balance) ' +
                         f'VALUES (0, {card.num}, {card.pin}, {card.balance});')
        self.conn.commit()
        self.cache[card.num] = card

    def get_card(self, num):
        return self.cache[num] if num in self.cache else None


class Card:
    def __init__(self, num, pin, balance=0):
        self.num = num
        self.pin = pin
        self.balance = balance


def main():
    db = Database(sqlite3.connect('card.s3db'))
    db.create()
    active = None
    while True:
        if active is None:
            active, cmd = main_menu(db)
        else:
            active, cmd = card_menu(active)
        print()
        if cmd == CMD_STOP:
            break


def main_menu(db):
    action = ask_action()
    print()
    if action == ACT_CREATE:
        create_account(db)
        return None, CMD_NEXT
    elif action == ACT_LOGIN:
        card = login(db)
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


def create_account(db):
    num = generate_card_num()
    pin = generate_pin()
    card = Card(num, pin, 0)
    print('Your card has been created')
    print('Your card number:')
    print(num)
    print('Your card PIN:')
    print(pin)
    save(db, card)


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


def save(db, card):
    db.add_card(card)


def login(db):
    num = input('Enter your card number: ')
    pin = input('Enter your PIN: ')
    print()
    card = db.get_card(num)
    if card is not None and pin == card.pin:
        print('You have successfully logged in!')
        return card
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
