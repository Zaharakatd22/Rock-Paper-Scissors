import random
from typing import TextIO


class RPS:

    def __init__(self):
        self.user_choice: list = []
        self.computer_choice: list = []
        self.option: list = ["rock", "paper", "scissors"]
        self.is_play: bool = False
        self.user_name: str = ""
        self.user_score: int = 0
        self.rating_file: TextIO = open("rating.txt", "r", encoding="utf-8")
        self.game_rules: dict = {}
        self.game_rules_tmp: list = [{}, []]

    def __repr__(self):
        pass

    def __str__(self):
        pass

    def add_user_points(self, points: int = 0):
        self.user_score += points

    def get_user_point(self):
        for user in self.rating_file:
            if self.user_name in user:
                self.user_score = int(user.split()[1])
                break

    def get_current_rating(self):
        print(f"Your rating: {self.user_score}")

    def generate_random_game_rules(self):
        #  generate basis of game_rules
        for elem in self.option:
            self.game_rules[elem] = list(self.option)
            self.game_rules[elem].remove(elem)
            self.game_rules_tmp[0][elem] = len(self.option) - 1

        while len(self.game_rules_tmp[0]) != 0:
            # option key with minimum number of selected relations
            min_key: str = min(self.game_rules_tmp[0], key=lambda x: self.game_rules_tmp[0][x])

            if self.game_rules_tmp[0][min_key] > (len(self.option) - 1) // 2:
                for i in range(0, self.game_rules_tmp[0][min_key] // 2):
                    # generate list with index of option to select
                    self.game_rules_tmp[1] = [i for i in range(0, self.game_rules_tmp[0][min_key])]
                    del_option_index: int = random.choice(self.game_rules_tmp[1])
                    self.game_rules_tmp[1].remove(del_option_index)
                    self.game_rules[min_key].pop(del_option_index)
                    self.game_rules_tmp[0][min_key] -= 1

            for option in self.game_rules[min_key]:
                if min_key in self.game_rules[option]:
                    self.game_rules[option].remove(min_key)
                    self.game_rules_tmp[0][option] -= 1
            self.game_rules_tmp[0].pop(min_key)

    def user_choice_option(self, user_choice: str):
        self.user_choice.append(user_choice)

    def computer_choice_option(self):
        self.computer_choice.append(random.choice(self.option))

    def get_last_game_result(self):
        if self.user_choice[-1] == self.computer_choice[-1]:
            print(f"There is a draw ({self.computer_choice[-1]})")
            self.add_user_points(50)
        elif self.user_choice[-1] == "rock" and self.computer_choice[-1] == "scissors" \
                or self.user_choice[-1] == "scissors" and self.computer_choice[-1] == "paper" \
                or self.user_choice[-1] == "paper" and self.computer_choice[-1] == "rock":
            print(f"Well done. Computer chose {self.computer_choice[-1]} and failed")
            self.add_user_points(100)
        else:  # player lose (inversion of win)
            print(f"Sorry, but computer chose {self.computer_choice[-1]}")

    def play(self, user_choice: str):
        if user_choice == "!exit":
            self.is_play = False
            self.rating_file.close()
            print("Bye!")
        elif user_choice == "!rating":
            self.get_current_rating()
        elif user_choice in self.option:
            self.user_choice_option(user_choice)
            self.computer_choice_option()
            self.get_last_game_result()
        else:  # incorrect input
            print("Invalid input")

    def start(self, user_name: str, game_mode: str):
        self.is_play = True
        self.user_name = user_name
        self.option = game_mode.split(",")
        self.get_user_point()
        self.generate_random_game_rules()
        print("Okay, let's start")
        print("g", self.game_rules)


def main():
    user_name: str = input("Enter your name: ")
    print(f"Hello, {user_name}")
    game_mode: str = input("> ")
    rock_paper_scissors = RPS()
    rock_paper_scissors.start(user_name, game_mode)
    while rock_paper_scissors.is_play:
        user_inp: str = input("> ")
        rock_paper_scissors.play(user_inp)


if __name__ == "__main__":
    main()
