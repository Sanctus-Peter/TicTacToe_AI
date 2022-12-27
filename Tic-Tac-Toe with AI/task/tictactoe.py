import random


def x_count(board: list[list[str]]) -> int:
    count = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == "X":
                count += 1
    return count


def o_count(board: list[list[str]]) -> int:
    count = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == "O":
                count += 1
    return count


class TicTacToe:
    def __init__(self):
        self.board = [[' ' for i in range(3)] for j in range(3)]
        self.player_turn = 1
        self.PLAY_ON = -1
        self.DRAW = 0
        self.loop()

    def display_board(self):
        board = self.board
        print("---------")
        print("|", board[0][0], board[0][1], board[0][2], "|")
        print("|", board[1][0], board[1][1], board[1][2], "|")
        print("|", board[2][0], board[2][1], board[2][2], "|")
        print("---------")

    def clear_board(self):
        self.board = [[' ' for i in range(3)] for j in range(3)]

    def check_board_state(self) -> int:
        if x_count(self.board) + o_count(self.board) == 9:
            return self.DRAW
        else:
            return self.PLAY_ON

    def check_for_win(self):
        board = self.board
        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] != " ":
                return board[i][0]
            elif board[0][i] == board[1][i] == board[2][i] != " ":
                return board[0][i]
        if board[0][0] == board[1][1] == board[2][2] != " ":
            return board[0][0]
        elif board[0][2] == board[1][1] == board[2][0] != " ":
            return board[0][2]
        else:
            return None

    def is_valid_move(self, x: int, y: int) -> bool:
        return self.board[x][y] == " "

    def winning_move(self, player_choice: str):
        board = self.board
        for i in range(3):
            for j in range(3):
                if self.is_valid_move(i, j):
                    board[i][j] = player_choice
                    if self.check_for_win() == player_choice:
                        return i, j
                    board[i][j] = " "
        return None

    def computer_medium_move(self, player_choice: str):
        move = self.winning_move(player_choice)
        if move:
            self.board[move[0]][move[1]] = player_choice
            return
        move = self.winning_move("X" if player_choice == "O" else "O")
        if move:
            self.board[move[0]][move[1]] = player_choice
            return
        self.computer_move(player_choice)

    def computer_move(self, player_choice: str):
        move = [str(random.randint(1, 3)), str(random.randint(1, 3))]
        while not self.is_valid_move(int(move[0]) - 1, int(move[1]) - 1):
            move = [str(random.randint(1, 3)), str(random.randint(1, 3))]
        self.board[int(move[0]) - 1][int(move[1]) - 1] = player_choice

    def make_move(self, player_choice: str):
        while True:
            move = input("Enter the coordinates: ").split()
            if not move[0].isdigit() or not move[1].isdigit():
                print("You should enter numbers!")
            elif int(move[0]) not in range(1, 4) or int(move[1]) not in range(1, 4):
                print("Coordinates should be from 1 to 3!")
            elif self.board[int(move[0]) - 1][int(move[1]) - 1] != " ":
                print("This cell is occupied! Choose another one!")
            else:
                self.board[int(move[0]) - 1][int(move[1]) - 1] = player_choice
                break

    def get_best_move(self, player_choice: str):
        best_score = float("-inf")
        best_move = None
        for row in range(3):
            for col in range(3):
                if self.is_valid_move(row, col):
                    self.board[row][col] = player_choice
                    score = self.minimax(player_choice,  False)
                    self.board[row][col] = " "
                    if score > best_score:
                        best_score = score
                        best_move = row, col
        return best_move

    def minimax(self, player_choice: str,  is_maximizing: bool):
        result = self.check_for_win()
        opponent = "X" if player_choice == "O" else "O"
        if result == player_choice:
            return 10
        elif result == opponent:
            return -10
        elif self.check_board_state() == self.DRAW:
            return 0

        if is_maximizing:
            best_score = float("-inf")
            for row in range(3):
                for col in range(3):
                    if self.is_valid_move(row, col):
                        self.board[row][col] = player_choice
                        score = self.minimax(player_choice,  False)
                        self.board[row][col] = " "
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float("inf")
            for row in range(3):
                for col in range(3):
                    if self.is_valid_move(row, col):
                        self.board[row][col] = "O" if player_choice == "X" else "X"
                        score = self.minimax(player_choice,  True)
                        self.board[row][col] = " "
                        best_score = min(score, best_score)
            return best_score

    def play(self, player_1: str, player_2: str):
        self.clear_board()
        self.player_turn = 1
        self.display_board()
        while self.check_board_state() == self.PLAY_ON:
            player_choice = "X" if self.player_turn % 2 == 1 else "O"
            if player_2 == "easy" and player_choice == "O" or player_1 == "easy" and player_choice == "X":
                print("Making move level \"easy\"")
                self.computer_move(player_choice)
            elif player_2 == "medium" and player_choice == "O" or player_1 == "medium" and player_choice == "X":
                print("Making move level \"medium\"")
                self.computer_medium_move(player_choice)
            elif player_2 == "hard" and player_choice == "O" or player_1 == "hard" and player_choice == "X":
                print("Making move level \"hard\"")
                move = self.get_best_move(player_choice)
                self.board[move[0]][move[1]] = player_choice
            else:
                self.make_move(player_choice)
            self.player_turn += 1
            self.display_board()
            winner = self.check_for_win()
            if winner:
                print(winner, "wins")
                break
            elif self.check_board_state() == self.DRAW:
                print("Draw")
                break

    def loop(self):
        while True:
            input_cmd = input("Input command: ")
            if input_cmd == "exit":
                break
            elif len(input_cmd.split()) != 3 or input_cmd.split()[0] != "start":
                print("Bad parameters!")
            elif input_cmd.split()[1] not in ["user", "easy", "medium", "hard"] \
                    or input_cmd.split()[2] not in ["user", "easy", "medium", "hard"]:
                print("Bad parameters!")
            else:
                player_1, player_2 = input_cmd.split()[1:]
                self.play(player_1, player_2)


if __name__ == "__main__":
    game = TicTacToe()
