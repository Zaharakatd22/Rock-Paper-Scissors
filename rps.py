class RPS:
    def __init__(self):
        self.user_chose: list[str] = []
        self.computer_chose: list[str] = []

    def __repr__(self):
        pass

    def __str__(self):
        pass

    def user_chosen(self, user_chose):
        self.user_chose.append(user_chose)
        if self.user_chose[-1] == "rock":
            self.computer_chose.append("paper")
        elif self.user_chose[-1] == "paper":
            self.computer_chose.append("scissors")
        else:  # self.user_chose[-1] == "scissors"
            self.computer_chose.append("rock")

    def get_last_game_result(self):
        print(f"Sorry, but computer chose {self.computer_chose[-1]}")

    def play(self, user_chose):
        self.user_chosen(user_chose)
        self.get_last_game_result()


def main():
    rock_paper_scissors = RPS()
    user_inp = input("> ")
    rock_paper_scissors.play(user_inp)


if __name__ == "__main__":
    main()
