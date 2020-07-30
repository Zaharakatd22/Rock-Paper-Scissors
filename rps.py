import random
from typing import TextIO


class RPS:

    def __init__(self):
        self.user_choice: list = []
        self.computer_choice: list = []
        self.option: list = []
        self.is_play: bool = False
        self.user_name: str = ""
        self.user_score: int = 0
        self.is_new_user: bool = False
        self.rating_file: TextIO = open("rating.txt", "r+", encoding="utf-8")
        self.local_rating: dict = {}
        self.game_mode: str = ""
        self.game_rules: dict = {}
        self.game_rules_tmp: list = [{}, []]

    def __repr__(self):
        pass

    def __str__(self):
        pass

    def add_user_points(self, points: int = 0):
        self.user_score += points

    def get_user_point(self):
        for user_rating in self.rating_file:
            user, score = user_rating.strip().split()
            self.local_rating[user] = int(score)
            if self.user_name == user:
                self.user_score = int(score)
                break
        else:
            self.is_new_user = True

        for user_rating in self.rating_file:
            user, score = user_rating.strip().split()
            self.local_rating[user] = int(score)

    def get_current_rating(self):
        print(f"Your rating: {self.user_score}")

    def get_full_current_rating(self):
        self.update_local_rating()
        for i, user_info in enumerate(self.sort_local_rating(self.local_rating)):
            if self.user_name == user_info[0]:
                print("YOU -> " + str(i + 1) + ":  ", user_info[0], user_info[1])
            else:
                print(str(i + 1) + ":  ", user_info[0], user_info[1])

    def update_local_rating(self):
        self.local_rating[self.user_name] = self.user_score

    @staticmethod
    def sort_local_rating(l_rating) -> list:
        local_rating_list: list = list(l_rating.items())
        local_rating_list.sort(key=lambda x: x[1], reverse=True)

        return local_rating_list

    def update_file_rating(self):
        self.update_local_rating()
        self.rating_file.truncate(0)
        for user, score in self.sort_local_rating(self.local_rating):
            self.rating_file.write(user + " " + str(score) + "\n")

    def generate_user_mode_game_rules(self):
        #  generate basis of game_rules
        for elem in self.option:
            self.game_rules[elem] = list(self.option)
            self.game_rules[elem].remove(elem)
            self.game_rules_tmp[0][elem] = len(self.option) - 1

        while len(self.game_rules_tmp[0]) != 0:
            # option key with minimum number of selected relations
            min_key: str = min(self.game_rules_tmp[0], key=lambda x: self.game_rules_tmp[0][x])

            if self.game_rules_tmp[0][min_key] > (len(self.option) - 1) // 2:
                while self.game_rules_tmp[0][min_key] != (len(self.option) - 1) // 2:
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
        elif self.computer_choice[-1] in self.game_rules[self.user_choice[-1]]:
            print(f"Well done. Computer chose {self.computer_choice[-1]} and failed")
            self.add_user_points(100)
        else:  # player lose (inversion of win)
            print(f"Sorry, but computer chose {self.computer_choice[-1]}")

    def play(self, user_choice: str):
        if user_choice == "!exit":
            self.is_play = False
            self.update_file_rating()
            self.rating_file.close()
            print("Bye!")
        elif user_choice == "!rating":
            self.get_current_rating()
        elif user_choice == "!full_rating":
            self.get_full_current_rating()
        elif user_choice in self.option:
            self.user_choice_option(user_choice)
            self.computer_choice_option()
            self.get_last_game_result()
        else:  # incorrect input
            print("Invalid input")

    def start(self, user_name: str, game_mode: str, game_option: str):
        self.is_play = True
        self.user_name = user_name
        self.game_mode = game_mode
        self.option = game_option.split(",")
        self.get_user_point()
        if self.game_mode == "classic_mode":
            self.game_rules = {
                "paper": ["rock"],
                "rock": ["scissors"],
                "scissors": ["paper"]
                }
        elif self.game_mode == "big_bang_theory_mode":
            self.game_rules = {
                "rock": ["lizard", "scissors"],
                "paper": ["rock", "spock"],
                "scissors": ["paper", "lizard"],
                "lizard": ["spock", "paper"],
                "spock": ["scissors", "rock"]
            }
        else:
            self.generate_user_mode_game_rules()
            print(self.game_rules)
        print("Okay, let's start")


def main():
    user_name: str = input("Enter your name: > ")
    print(f"Hello, {user_name}")
    game_mode: str = input("Choose a game mode(user_mode, big_bang_theory_mode, classic_mode) > ")
    if game_mode == "user_mode":
        game_option: str = input("Please, enter your option (option_1,option_2,option_3,...,option_n): > ")
    elif game_mode == "big_bang_theory_mode":
        game_option: str = "rock,paper,scissors,lizard,spock"
    elif game_mode == "classic_mode" or game_mode == "":
        game_option: str = "rock,paper,scissors"
        game_mode = "classic_mode"
    else:  # incorrect input
        print("I don't know this game mode, that go play classic mode!!!")
        game_option: str = "rock,paper,scissors"
        game_mode = "classic_mode"

    rock_paper_scissors = RPS()
    rock_paper_scissors.start(user_name, game_mode, game_option)
    while rock_paper_scissors.is_play:
        user_inp: str = input("> ")
        rock_paper_scissors.play(user_inp)


if __name__ == "__main__":
    main()
