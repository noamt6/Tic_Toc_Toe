"""
This is the main file of the Tic Tac Toe project. 
It starts the game by connecting the logic (GameBoard) and the graphics (TurtleInterface).
"""
from game_board import GameBoard
from interface import TurtleInterface
import turtle

def main():
   # Creates the game logic and the user interface and shows past game history
   board = GameBoard()
   try:
       with open("game_history.txt", "r") as f:
           print("\n=== FULL GAME HISTORY (PREVIOUS GAMES) ===")
           print(f.read())
           print("==========================================\n")
   except FileNotFoundError:
       print("\n--- No history found yet ---\n")
   gui = TurtleInterface(board)
   turtle.mainloop() # keeps the window open

if __name__ == "__main__":
  main()