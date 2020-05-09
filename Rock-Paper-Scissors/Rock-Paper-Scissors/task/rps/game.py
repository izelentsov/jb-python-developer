# Write your code here
def choose(user_opt):
    if user_opt == "paper":
        return "scissors"
    if user_opt == "rock":
        return "paper"
    return "rock"


def run():
    user_option = input()
    option = choose(user_option)
    print(f'Sorry, but computer chose {option}')


run()
