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
ACT_CARD_INCOME = 2
ACT_CARD_TRANSFER = 3
ACT_CARD_CLOSE = 4
ACT_CARD_LOGOUT = 5


class Database:
    def __init__(self, conn):
        self.conn = conn
        self.cur = conn.cursor()

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

    def get_card(self, num):
        self.cur.execute('SELECT number, pin, balance FROM card ' +
                         f'WHERE number = {num};')
        row = self.cur.fetchone()
        return Card(row[0], row[1], row[2]) if row is not None else None

    def income(self, num, amount):
        self.cur.execute(f'UPDATE card SET balance = balance + {amount} ' +
                         f'WHERE number = {num}')
        self.conn.commit()

    def transfer(self, from_num, to_num, amount):
        self.cur.execute(f'UPDATE card SET balance = balance - {amount} ' +
                         f'WHERE number = {from_num}')
        self.cur.execute(f'UPDATE card SET balance = balance + {amount} ' +
                         f'WHERE number = {to_num}')
        self.conn.commit()

    def delete_card(self, num):
        self.cur.execute(f'DELETE FROM card WHERE number = {num};')
        self.conn.commit()


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
            active, cmd = card_menu(active, db)
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
    checksum = calc_luhn(num)
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
    return 0 if res % 10 == 0 else (10 - res % 10)


def check_luhn(num):
    checked = [int(c) for c in num[:15]]
    checksum = calc_luhn(checked)
    return int(num[15]) == checksum


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
        return num
    else:
        print('Wrong card number or PIN!')
        return None


def card_menu(num, db):
    action = ask_card_action()
    print()
    if action == ACT_CARD_EXIT:
        return None, CMD_STOP
    elif action == ACT_CARD_BALANCE:
        print_balance(num, db)
        return num, CMD_NEXT
    elif action == ACT_CARD_INCOME:
        income(num, db)
        return num, CMD_NEXT
    elif action == ACT_CARD_TRANSFER:
        transfer(num, db)
        return num, CMD_NEXT
    elif action == ACT_CARD_CLOSE:
        close_account(num, db)
        return num, CMD_NEXT
    elif action == ACT_CARD_LOGOUT:
        print('You have successfully logged out!')
        return None, CMD_NEXT


def ask_card_action():
    print('1. Balance')
    print('2. Add income')
    print('3. Do transfer')
    print('4. Close account')
    print('5. Log out')
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


def print_balance(num, db):
    card = db.get_card(num)
    if card is not None:
        print(f'Balance: {card.balance}')
    else:
        print(f'No card info')


def income(num, db):
    amount = int(input('Enter income: '))
    db.income(num, amount)


def transfer(num, db):
    print('Transfer')
    other = input('Enter card number: ')

    if not check_luhn(other):
        print('Probably you made mistake in the card number. Please try again!')
        return

    other_card = db.get_card(other)
    if other_card is None:
        print('Such a card does not exist.')
        return

    amount = int(input('Enter how much money you want to transfer: '))
    card = db.get_card(num)
    if amount > card.balance:
        print('Not enough money!')
        return

    db.transfer(num, other, amount)


def close_account(num, db):
    db.delete_card(num)


main()
