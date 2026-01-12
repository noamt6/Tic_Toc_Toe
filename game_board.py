"""
This file handles the rules and the data of the game.
The GameBoard class tracks symbols on the board, checks for winners, and handles saving files.
"""
import pickle

class GameBoard:
   def __init__(self):
       # Initializes a clean board
       self.reset_board()

   def reset_board(self):
       # Clears all data to start a new game
       self.board = [[' ' for _ in range(3)] for _ in range(3)]
       self.current_turn, self.winner, self.is_game_over = 'X', None, False
       self.winning_line, self.saved_game_mode = None, 0
       self.player_x, self.player_o = "PLAYER X", "PLAYER O"

   def make_move(self, row, col):
       # Places a symbol and updates the turn if the move is valid
       if self.board[row][col] != ' ' or self.is_game_over: return False
       self.board[row][col] = self.current_turn
       if self.check_winner(): self.winner, self.is_game_over = self.current_turn, True
       elif self.check_draw(): self.is_game_over = True
       else: self.current_turn = 'O' if self.current_turn == 'X' else 'X'
       return True

   def check_winner(self):
       # Checks all rows, columns, and diagonals for three identical symbols
       lines = []
       for i in range(3):
           lines.append({'cells': [self.board[i][j] for j in range(3)], 'coords': [(i, 0), (i, 2)]})
           lines.append({'cells': [self.board[j][i] for j in range(3)], 'coords': [(0, i), (2, i)]})
       lines.append({'cells': [self.board[0][0], self.board[1][1], self.board[2][2]], 'coords': [(0, 0), (2, 2)]})
       lines.append({'cells': [self.board[0][2], self.board[1][1], self.board[2][0]], 'coords': [(0, 2), (2, 0)]})
       for line in lines:
           if line['cells'][0] != ' ' and all(cell == line['cells'][0] for cell in line['cells']):
               self.winning_line = line['coords']; return True
       return False

   def check_draw(self):
       # Checks if the board is full without a winner
       return all(cell != ' ' for row in self.board for cell in row)

   def log_game_result(self):
       # Writes the winner and names to a text file
       try:
           with open("game_history.txt", "a") as f:
               w_name = self.player_x if self.winner == 'X' else self.player_o
               res = f"WINNER: {w_name}" if self.winner else "DRAW"
               f.write(f"{res} | {self.player_x} VS {self.player_o}\n")
       except IOError: pass

   def get_history(self):
       # Reads the last 10 games from the history file
       try:
           with open("game_history.txt", "r") as f:
               return list(reversed(f.readlines()[-10:]))
       except FileNotFoundError: return ["No history available."]

   def save_game(self):
       # Saves the whole GameBoard object to a binary file
       try:
           with open("game_data.pkl", "wb") as f: pickle.dump(self, f)
           return True
       except: return False

   def load_game(self):
       # Loads game data from the file and updates current state
       try:
           with open("game_data.pkl", "rb") as f: data = pickle.load(f)
           self.__dict__.update(data.__dict__)
           return True
       except: return False