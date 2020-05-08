# Write your code here


def print_state(st):
    print('The coffee machine has:')
    print(f'{st[0]} of water')
    print(f'{st[1]} of milk')
    print(f'{st[2]} of coffee beans')
    print(f'{st[3]} of disposable cups')
    print(f'{st[4]} of money')


def check_supply(st, need):
    if st[0] < need[0]:
        return 'Sorry, not enough water!'
    if st[1] < need[1]:
        return 'Sorry, not enough milk!'
    if st[2] < need[2]:
        return 'Sorry, not enough coffee beans!'
    if st[3] < need[3]:
        return 'Sorry, not enough disposable cups!'
    return None


ESPRESSO = [250, 0, 16, 1]
LATTE = [350, 75, 20, 1]
CAPPUCCINO = [200, 100, 12, 1]


def make_coffee(st, need, price):
    st[0] -= need[0]
    st[1] -= need[1]
    st[2] -= need[2]
    st[3] -= need[3]
    st[4] += price


def buy(st):
    what = input('What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu:')
    if what == '1':
        need = ESPRESSO
        price = 4
    elif what == '2':
        need = LATTE
        price = 7
    elif what == '3':
        need = CAPPUCCINO
        price = 6
    elif what == 'back':
        return

    error = check_supply(st, need)
    if error:
        print(error)
    else:
        print('I have enough resources, making you a coffee!')
        make_coffee(st, need, price)


def fill(st):
    w = int(input('Write how many ml of water do you want to add: '))
    m = int(input('Write how many ml of milk do you want to add: '))
    b = int(input('Write how many grams of coffee beans do you want to add: '))
    c = int(input('Write how many disposable cups of coffee do you want to add: '))
    st[0] += w
    st[1] += m
    st[2] += b
    st[3] += c


def take(st):
    print(f'I gave you ${st[4]}')
    st[4] = 0



def run():
    state = [400, 540, 120, 9, 550]

    while True:
        action = input('Write action (buy, fill, take, remaining, exit): ')

        if action == 'buy':
            buy(state)
        elif action == 'fill':
            fill(state)
        elif action == 'take':
            take(state)
        elif action == 'remaining':
            print()
            print_state(state)
        elif action == 'exit':
            break

        print()


run()

