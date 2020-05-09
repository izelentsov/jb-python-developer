# Write your code here


class Supplies:
    def __init__(self, water, milk, beans, cups):
        self.water = water
        self.milk = milk
        self.beans = beans
        self.cups = cups

    def add(self, supp):
        self.water += supp.water
        self.milk += supp.milk
        self.beans += supp.beans
        self.cups += supp.cups

    def remove(self, supp):
        self.water -= supp.water
        self.milk -= supp.milk
        self.beans -= supp.beans
        self.cups -= supp.cups


class CM:

    ESPRESSO_ING = Supplies(water=250, milk=0, beans=16, cups=1)
    ESPRESSO_PRICE = 4
    LATTE_ING = Supplies(water=350, milk=75, beans=20, cups=1)
    LATTE_PRICE = 7
    CAPPUCCINO_ING = Supplies(water=200, milk=100, beans=12, cups=1)
    CAPPUCCINO_PRICE = 6

    ST_ACTION = 0
    ST_COFFEE_TYPE = 1
    ST_FILL_WATER = 2
    ST_FILL_MILK = 3
    ST_FILL_BEANS = 4
    ST_FILL_CUPS = 5

    def __init__(self, supplies, money, state):
        self.supplies = supplies
        self.money = money
        self.state = state
        self.fill_amount = Supplies(water=0, milk=0, beans=0, cups=0)

    def print_rem(self):
        print('The coffee machine has:')
        print(f'{self.supplies.water} of water')
        print(f'{self.supplies.milk} of milk')
        print(f'{self.supplies.beans} of coffee beans')
        print(f'{self.supplies.cups} of disposable cups')
        print(f'{self.money} of money')

    def check_rem(self, need):
        if self.supplies.water < need.water:
            return 'Sorry, not enough water!'
        if self.supplies.milk < need.milk:
            return 'Sorry, not enough milk!'
        if self.supplies.beans < need.beans:
            return 'Sorry, not enough coffee beans!'
        if self.supplies.cups < need.cups:
            return 'Sorry, not enough disposable cups!'
        return None

    def make_coffee(self, ing, pay):
        self.supplies.remove(ing)
        self.money += pay

    def buy(self, ing, price):
        error = self.check_rem(ing)
        if error:
            print(error)
        else:
            print('I have enough resources, making you a coffee!')
            self.make_coffee(ing, price)

    def fill(self, supplies):
        self.supplies.add(supplies)

    def take(self):
        print(f'I gave you ${self.money}')
        self.money = 0

    def action_input(self, action):
        if action == 'buy':
            self.state = CM.ST_COFFEE_TYPE
            return True
        if action == 'fill':
            self.state = CM.ST_FILL_WATER
            return True
        if action == 'take':
            self.take()
            return True
        if action == 'remaining':
            print()
            self.print_rem()
            return True
        if action == 'exit':
            return False

    def coffee_input(self, what):
        if what == '1':
            ing = CM.ESPRESSO_ING
            pay = CM.ESPRESSO_PRICE
        elif what == '2':
            ing = CM.LATTE_ING
            pay = CM.LATTE_PRICE
        elif what == '3':
            ing = CM.CAPPUCCINO_ING
            pay = CM.CAPPUCCINO_PRICE
        else:
            self.state = CM.ST_ACTION
            return True

        self.buy(ing, pay)
        self.state = CM.ST_ACTION
        return True

    def water_fill_input(self, inp):
        self.fill_amount.water = int(inp)
        self.state = CM.ST_FILL_MILK
        return True

    def milk_fill_input(self, inp):
        self.fill_amount.milk = int(inp)
        self.state = CM.ST_FILL_BEANS
        return True

    def beans_fill_input(self, inp):
        self.fill_amount.beans = int(inp)
        self.state = CM.ST_FILL_CUPS
        return True

    def cups_fill_input(self, inp):
        self.fill_amount.cups = int(inp)
        self.fill(self.fill_amount)
        self.state = CM.ST_ACTION
        return True

    def prompt(self):
        if self.state == CM.ST_ACTION:
            return 'Write action (buy, fill, take, remaining, exit): '
        if self.state == CM.ST_COFFEE_TYPE:
            return 'What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu: '
        if self.state == CM.ST_FILL_WATER:
            return 'Write how many ml of water do you want to add: '
        if self.state == CM.ST_FILL_MILK:
            return 'Write how many ml of milk do you want to add: '
        if self.state == CM.ST_FILL_BEANS:
            return 'Write how many grams of coffee beans do you want to add: '
        if self.state == CM.ST_FILL_CUPS:
            return 'Write how many disposable cups of coffee do you want to add: '
        return 'STATE ERROR'

    def handle(self, inp):
        if self.state == CM.ST_ACTION:
            return self.action_input(inp)
        if self.state == CM.ST_COFFEE_TYPE:
            return self.coffee_input(inp)
        if self.state == CM.ST_FILL_WATER:
            return self.water_fill_input(inp)
        if self.state == CM.ST_FILL_MILK:
            return self.milk_fill_input(inp)
        if self.state == CM.ST_FILL_BEANS:
            return self.beans_fill_input(inp)
        if self.state == CM.ST_FILL_CUPS:
            return self.cups_fill_input(inp)
        return False


def run():
    init_sup = Supplies(water=400, milk=540, beans=120, cups=9)
    cm = CM(init_sup, money=550, state=CM.ST_ACTION)
    running = True

    while running:
        prompt = cm.prompt()
        inp = input(prompt)
        running = cm.handle(inp)
        print()


run()
