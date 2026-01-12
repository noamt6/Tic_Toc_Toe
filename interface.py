"""
This file handles the visual part of the game.
The TurtleInterface class draws the screen, buttons, and handles mouse and keyboard inputs.
"""
import turtle
from ai_player import AIPlayer
import time

class TurtleInterface:
  def __init__(self, game_board):
      # Sets up the initial game settings and screen
      self.game_board = game_board
      self.ai = AIPlayer()
      self.game_state = "MENU"
      self.game_mode = 0
      self.previous_state = "MENU"
      self.is_keyboard_active = False
      self.screen = turtle.Screen()
      self.screen.title("Tic Tac Toe")
      self.screen.setup(width=600, height=600)
      self.screen.bgcolor("#1A1A1A")
      self.screen.tracer(0)
      self.screen.listen()
      # Define keys for menu and game actions
      self.screen.onkey(lambda: self.menu_action(1), "1")
      self.screen.onkey(lambda: self.menu_action(2), "2")
      self.screen.onkey(lambda: self.menu_action(3), "3")
      self.screen.onkey(lambda: self.menu_action(4), "4")
      self.screen.onkey(lambda: self.menu_action(5), "5")
      self.screen.onkey(self.save_game_action, "s")
      self.screen.onkey(self.save_game_action, "S")
      self.screen.onkey(self.show_history_action, "h")
      self.screen.onkey(self.show_history_action, "H")
      self.screen.onkey(self.exit_to_menu_action, "e")
      self.screen.onkey(self.exit_to_menu_action, "E")
      self.screen.onkey(self.go_back_action, "b")
      self.screen.onkey(self.go_back_action, "B")
      self.screen.onkey(self.activate_keyboard_mode, "space")
      self.pen = turtle.Turtle()
      self.pen.hideturtle()
      self.pen.speed(0)
      self.screen.onclick(self.handle_click)
      self.draw_menu()

  def popup_input(self, title, prompt):
      # Opens a small window to get text from the player (beyond turtle)
      try:
          root = self.screen.getcanvas().winfo_toplevel()
          root.attributes('-topmost', 1)
          root.attributes('-topmost', 0)
          root.focus_force()
      except: pass
      return self.screen.textinput(title, prompt)

  def activate_keyboard_mode(self):
      # Starts the keyboard input mode for moves
      if self.game_state == "GAME" and not self.game_board.is_game_over:
          self.is_keyboard_active = True
          self.run_manual_turn()

  def draw_menu(self):
      # Draws the main menu screen with all options
      self.game_state = "MENU"
      self.is_keyboard_active = False
      self.pen.clear()
      self.pen.penup()
      self.pen.goto(0, 200)
      self.pen.color("#00D2FF")
      self.pen.write("TIC TAC TOE", align="center", font=("Courier", 36, "bold"))
      self.pen.goto(0, 165)
      self.pen.color("#BDC3C7")
      self.pen.write("Press 1-5 or use the mouse to start", align="center", font=("Arial", 11, "normal"))
      self.draw_button(0, 120, 380, 45, "1. PLAYER VS PLAYER", "#2980B9")
      self.draw_button(0, 55, 380, 45, "2. PLAYER VS RANDOM AI", "#2980B9")
      self.draw_button(0, -10, 380, 45, "3. PLAYER VS STRATEGIC AI", "#2980B9")
      self.draw_button(0, -75, 380, 45, "4. LOAD GAME", "#27AE60")
      self.draw_button(0, -140, 380, 45, "5. SHOW HISTORY", "#8E44AD")
      self.screen.update()
      self.screen.listen()

  def menu_action(self, option):
      # Handles what happens when a menu option is selected
      if self.game_state != "MENU": return
      if option in [1, 2, 3]:
          self.game_mode = option
          self.get_player_names()
          self.start_game()
      elif option == 4: self.load_existing_game()
      elif option == 5: self.show_history_screen()

  def save_game_action(self):
      # Saves the game to a file when the player clicks save
      if self.game_state == "GAME" and not self.game_board.is_game_over:
          self.game_board.saved_game_mode = self.game_mode
          if self.game_board.save_game(): self.show_save_feedback()
      self.screen.listen()

  def show_history_action(self):
      # Switches to the history screen
      self.is_keyboard_active = False
      self.show_history_screen()

  def exit_to_menu_action(self):
      # Quits the game and goes back to the menu
      self.is_keyboard_active = False
      self.return_to_menu()

  def go_back_action(self):
      # Returns to the previous screen from history
      if self.game_state == "HISTORY":
          if self.previous_state == "GAME":
              self.game_state = "GAME"
              self.render_screen()
          else: self.return_to_menu()

  def draw_button(self, x, y, width, height, text, color="#34495E"):
      # Draws a clickable button with a 3D effect
      self.pen.penup(); self.pen.color("#000000")
      self.draw_rect(x + 4, y - 4, width, height)
      self.pen.color(color); self.draw_rect(x, y, width, height)
      self.pen.color("white"); self.pen.goto(x, y - 12)
      self.pen.write(text, align="center", font=("Verdana", 12, "bold"))

  def draw_rect(self, x, y, width, height):
      # Helper function to draw a filled rectangle
      self.pen.penup()
      self.pen.goto(x - width / 2, y + height / 2)
      self.pen.begin_fill()
      self.pen.pendown()
      self.pen.goto(x + width / 2, y + height / 2)
      self.pen.goto(x + width / 2, y - height / 2)
      self.pen.goto(x - width / 2, y - height / 2)
      self.pen.goto(x - width / 2, y + height / 2)
      self.pen.end_fill()
      self.pen.penup()

  def show_history_screen(self):
      # Draws the history screen and shows the last games
      if self.game_state != "HISTORY": self.previous_state = self.game_state
      self.game_state = "HISTORY"
      self.pen.clear()
      self.pen.penup()
      self.pen.color("white")
      self.pen.goto(0, 220)
      self.pen.write("HISTORY", align="center", font=("Verdana", 24, "bold"))
      history = self.game_board.get_history()
      y_pos = 150
      for line in history:
          self.pen.goto(0, y_pos); self.pen.write(line.strip(), align="center", font=("Consolas", 11, "normal"))
          y_pos -= 30
      self.draw_button(0, -230, 120, 45, "BACK (B)", "#C0392B")
      self.screen.update()
      self.screen.listen()

  def handle_click(self, x, y):
      # Manages mouse clicks on buttons and the game board
      if self.game_state == "GAME" and not self.game_board.is_game_over: self.is_keyboard_active = False
      if self.game_state == "MENU":
          if -190 < x < 190:
              if 97.5 < y < 142.5: self.menu_action(1)
              elif 32.5 < y < 77.5: self.menu_action(2)
              elif -32.5 < y < 12.5: self.menu_action(3)
              elif -97.5 < y < -52.5: self.menu_action(4)
              elif -162.5 < y < -117.5: self.menu_action(5)
          return
      if self.game_state == "HISTORY":
          if -60 < x < 60 and -252.5 < y < -207.5: self.go_back_action()
          return
      if self.game_state == "GAME":
          if 240 < y < 285:
              if -285 < x < -195: self.save_game_action()
              elif -60 < x < 60: self.show_history_action()
              elif 195 < x < 285: self.exit_to_menu_action()
          elif not self.game_board.is_game_over: self.process_move(x, y)
      elif self.game_state == "GAME_OVER":
          if -90 < x < 90 and -177.5 < y < -122.5: self.return_to_menu()

  def show_end_message(self):
      # Displays the winner or draw message at the end of the game
      self.game_state = "GAME_OVER"
      self.is_keyboard_active = False
      winner = self.game_board.player_x if self.game_board.winner == 'X' else self.game_board.player_o
      msg = f"{winner} WINS!" if self.game_board.winner else "IT'S A DRAW!"
      self.pen.penup()
      self.pen.color("white")
      self.draw_rect(0, 85, 420, 80)
      self.pen.penup()
      self.pen.goto(0, 70)
      self.pen.color("#1A1A1A")
      self.pen.write(msg, align="center", font=("Verdana", 26, "bold"))
      self.draw_button(0, -150, 200, 55, "BACK TO MENU (E)", "#2980B9")
      self.screen.listen()

  def render_screen(self):
      # Redraws the entire board and the game state
      self.pen.clear()
      self.draw_grid()
      self.draw_game_buttons()
      for r in range(3):
          for c in range(3):
              val = self.game_board.board[r][c]
              if val != ' ':
                  tx, ty = self.get_cell_coords(r, c)
                  if val == 'X': self.draw_x(tx, ty)
                  else: self.draw_o(tx, ty)
      if self.game_board.is_game_over:
          if self.game_board.winner: self.draw_winning_line()
          self.game_board.log_game_result()
          self.show_end_message()
      if not self.game_board.is_game_over:
          self.pen.penup()
          self.pen.goto(0, -280); self.pen.color("gray")
          self.pen.write("Press SPACE to enter coordinates with keyboard", align="center", font=("Arial", 9, "italic"))
      self.screen.update()
      self.screen.listen()

  def draw_grid(self):
      # Draws the lines for the Tic Tac Toe board
      self.pen.width(4); self.pen.color("#34495E")
      for i in [-85, 85]:
          self.pen.penup(); self.pen.goto(i, 260); self.pen.pendown(); self.pen.goto(i, -260)
          self.pen.penup(); self.pen.goto(-260, i); self.pen.pendown(); self.pen.goto(260, i)

  def draw_game_buttons(self):
      # Draws the buttons during a match like save and exit
      self.draw_button(-240, 260, 100, 40, "SAVE (S)", "#27AE60")
      self.draw_button(0, 260, 130, 40, "HISTORY (H)", "#8E44AD")
      self.draw_button(240, 260, 100, 40, "EXIT (E)", "#C0392B")

  def draw_x(self, x, y):
      # Draws the 'X' symbol in a specific cell
      self.pen.color("#00D2FF")
      self.pen.width(10)
      self.pen.penup()
      self.pen.goto(x - 45, y + 45)
      self.pen.pendown()
      self.pen.goto(x + 45, y - 45)
      self.pen.penup()
      self.pen.goto(x - 45, y - 45)
      self.pen.pendown()
      self.pen.goto(x + 45, y + 45)
      self.pen.penup()

  def draw_o(self, x, y):
      # Draws the 'O' symbol in a specific cell
      self.pen.color("#FF007F"); self.pen.width(10)
      self.pen.penup()
      self.pen.goto(x, y - 45)
      self.pen.setheading(0)
      self.pen.pendown()
      self.pen.circle(45)
      self.pen.penup()

  def draw_winning_line(self):
      # Draws a yellow line through the winning symbols
      self.pen.color("#F1C40F"); self.pen.width(15)
      start = self.get_cell_coords(self.game_board.winning_line[0][0], self.game_board.winning_line[0][1])
      end = self.get_cell_coords(self.game_board.winning_line[1][0], self.game_board.winning_line[1][1])
      self.pen.penup()
      self.pen.goto(start)
      self.pen.pendown()
      self.pen.goto(end)
      self.pen.penup()

  def get_player_names(self):
      # Asks the players for their names before starting
      root = self.screen.getcanvas().winfo_toplevel()
      nx = self.popup_input("Setup", "Player X Name:")
      self.game_board.player_x = nx.upper() if nx else "PLAYER X"
      if self.game_mode == 1:
          root.update()
          time.sleep(0.1)
          no = self.popup_input("Setup", "Player O Name:")
          self.game_board.player_o = no.upper() if no else "PLAYER O"
      elif self.game_mode == 2: self.game_board.player_o = "RANDOM AI"
      else: self.game_board.player_o = "STRATEGIC AI"
      self.screen.listen()

  def start_game(self):
      # Updates the game state and renders the board to begin
      self.game_state = "GAME"
      self.render_screen()

  def return_to_menu(self):
      # Resets the board and returns to the main menu
      self.game_board.reset_board()
      self.game_state = "MENU"
      self.draw_menu()

  def process_move(self, x, y):
      # Checks which cell was clicked and updates the game board
      col, row = (0 if x < -85 else 1 if x < 85 else 2), (0 if y > 85 else 1 if y > -85 else 2)
      if self.game_board.make_move(row, col):
          self.render_screen()
          if not self.game_board.is_game_over and self.game_mode > 1: self.ai_turn()

  def ai_turn(self):
      # Makes a move for the AI player based on the game mode
      move = self.ai.get_best_move(self.game_board) if self.game_mode == 3 else self.ai.get_random_move(self.game_board)
      if move:
          self.game_board.make_move(move[0], move[1]); self.render_screen()
          if self.is_keyboard_active and not self.game_board.is_game_over: self.screen.ontimer(self.run_manual_turn, 300)

  def show_save_feedback(self):
      # Shows a small green 'SAVED!' text on the screen
      self.pen.penup()
      self.pen.goto(-240, 225)
      self.pen.color("#2ECC71")
      self.pen.write("SAVED!", align="center", font=("Verdana", 8, "bold"))
      self.screen.update()

  def load_existing_game(self):
      # Tries to load a saved game from the file
      if self.game_board.load_game():
          self.game_mode = self.game_board.saved_game_mode; self.game_state = "GAME"; self.render_screen()
      else:
          self.pen.penup(); self.pen.goto(0, -230); self.pen.color("#E74C3C")
          self.pen.write("NO SAVE DATA", align="center", font=("Verdana", 12, "bold")); self.screen.update()

  def get_cell_coords(self, r, c):
      # Converts board row and column into screen pixels
      return (c - 1) * 170, (1 - r) * 170

  def run_manual_turn(self):
      # Make sure the game is still running
      if self.game_board.is_game_over or self.game_state != "GAME":
          return
      root = self.screen.getcanvas().winfo_toplevel()
      while True:
          msg = f"{self.game_board.current_turn} - Enter Row,Col (e.g. 1,2)\nS=Save, H=History, E=Exit"
          user_input = self.popup_input("Your Turn", msg)
          self.screen.listen()
          # If the player clicks 'Cancel'
          if user_input is None:
              self.is_keyboard_active = False
              return
          choice = user_input.upper().strip()
          if choice == 'S':
              self.save_game_action()
          elif choice == 'H':
              self.show_history_action();
              return
          elif choice == 'E':
              self.exit_to_menu_action();
              return
          elif choice == 'B':
              self.go_back_action();
              return
          # Check for board moves (Row, Col)
          parts = [p for p in choice.replace(" ", ",").replace("-", ",").split(",") if p]

          if len(parts) == 2 and all(p.isdigit() for p in parts):
              r, c = int(parts[0]), int(parts[1])

              if 1 <= r <= 3 and 1 <= c <= 3:
                  # Try to place the symbol on the board
                  if self.game_board.make_move(r - 1, c - 1):
                      self.render_screen()

                      if not self.game_board.is_game_over:
                          if self.game_mode > 1:
                              self.ai_turn()
                          elif self.is_keyboard_active:
                              self.screen.ontimer(self.run_manual_turn, 300)
                      break

          # If input was wrong or cell taken, refresh and try again
          root.update()
          time.sleep(0.1)