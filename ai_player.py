"""
This file controls how the computer plays.
The AIPlayer class has methods to pick moves, either randomly or using strategy.
"""
import random

class AIPlayer:
   def __init__(self):
       pass

   def get_random_move(self, game_board):
       # Picks an empty cell on the board at random
       empty_cells = [(r, c) for r in range(3) for c in range(3) if game_board.board[r][c] == ' ']
       return random.choice(empty_cells) if empty_cells else None

   def get_best_move(self, game_board):
       # Tries to win or block the player, otherwise takes the center or a random spot
       move = self.find_critical(game_board, 'O') # Try to win
       if move: return move
       move = self.find_critical(game_board, 'X') # Block player
       if move: return move
       if game_board.board[1][1] == ' ': return (1, 1)
       return self.get_random_move(game_board)

   def find_critical(self, game_board, symbol):
       # Looks for a line with two symbols and an empty space
       for r in range(3):
           row = [game_board.board[r][c] for c in range(3)]
           if row.count(symbol) == 2 and row.count(' ') == 1: return (r, row.index(' '))
       for c in range(3):
           col = [game_board.board[r][c] for r in range(3)]
           if col.count(symbol) == 2 and col.count(' ') == 1: return (col.index(' '), c)
       d1 = [game_board.board[i][i] for i in range(3)]
       if d1.count(symbol) == 2 and d1.count(' ') == 1: return (d1.index(' '), d1.index(' '))
       d2 = [game_board.board[i][2-i] for i in range(3)]
       if d2.count(symbol) == 2 and d2.count(' ') == 1:
           idx = d2.index(' '); return (idx, 2 - idx)
       return None