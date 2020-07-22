import random


class RPS:
    def __init__(self):
        self.user_choice: list = []
        self.computer_choice: list = []
        self.option: list = ["rock", "paper", "scissors"]

    def __repr__(self):
        pass

    def __str__(self):
        pass

    def user_choice_option(self, user_choice):
        self.user_choice.append(user_choice)

    def computer_choice_option(self):
        self.computer_choice.append(random.choice(self.option))

    def get_last_game_result(self):
        if self.user_choice[-1] == self.computer_choice[-1]:
            print(f"There is a draw ({self.computer_choice[-1]})")
        elif self.user_choice[-1] == "rock" and self.computer_choice[-1] == "scissors" \
            or self.user_choice[-1] == "scissors" and self.computer_choice[-1] == "paper" \
                or self.user_choice[-1] == "paper" and self.computer_choice[-1] == "rock":
            print(f"Well done. Computer chose {self.computer_choice[-1]} and failed")
        else:  # player lose (inversion of win)
            print(f"Sorry, but computer chose {self.computer_choice[-1]}")

    def play(self, user_choice):
        self.user_choice_option(user_choice)
        self.computer_choice_option()
        self.get_last_game_result()


def main():
    rock_paper_scissors = RPS()
    user_inp = input("> ")
    rock_paper_scissors.play(user_inp)


if __name__ == "__main__":
    main()