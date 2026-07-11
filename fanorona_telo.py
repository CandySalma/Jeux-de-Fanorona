import tkinter as tk
from tkinter import messagebox

class Game3x3:
    def __init__(self, master, player1_name, player2_name, player1_color, player2_color, num_rounds, menu_frame, game_frame):
        self.master = master
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.player1_color = player1_color
        self.player2_color = player2_color
        self.num_rounds = num_rounds
        self.current_round = 1
        self.scores = {player1_name: 0, player2_name: 0}

        self.menu_frame = menu_frame
        self.game_frame = game_frame

        self.master.title("Fanorona 3x3")

        # Frame for buttons
        self.button_frame = tk.Frame(self.game_frame)
        self.button_frame.pack(side="top", fill="x", pady=10)

        self.back_button = tk.Button(self.button_frame, text="Quitter", command=self.confirm_exit)
        self.back_button.pack(side="left", padx=10)

        self.restart_button = tk.Button(self.button_frame, text="Restart Game", command=self.reset_game)
        self.restart_button.pack(side="right", padx=10)

        # Canvas for drawing the game board
        self.canvas = tk.Canvas(self.game_frame, width=300, height=300)
        self.canvas.pack(pady=20)

        # Frame for displaying the scores
        self.score_frame = tk.Frame(self.game_frame)
        self.score_frame.pack(pady=20)

        self.setup_scoreboard()
        self.setup_board()

        self.positions = {
            player1_name: [(2, 0), (2, 1), (2, 2)],
            player2_name: [(0, 0), (0, 1), (0, 2)]
        }
        self.original_positions = {k: list(v) for k, v in self.positions.items()}

        self.moves_count = {player1_name: {pos: 0 for pos in self.positions[player1_name]},
                            player2_name: {pos: 0 for pos in self.positions[player2_name]}}

        self.turn = player1_name
        self.selected_boule = None
        self.draw_boules()
        self.draw_highlight()

        self.canvas.bind("<Button-1>", self.click_handler)

    def setup_scoreboard(self):
        self.score_label = tk.Label(self.score_frame, text=f"Round {self.current_round} of {self.num_rounds}", font=("Arial", 16))
        self.score_label.pack()

        self.player1_label = tk.Label(self.score_frame, text=f"{self.player1_name}: {self.scores[self.player1_name]} points", fg=self.player1_color, font=("Arial", 14))
        self.player1_label.pack(side="left", padx=20)

        self.player2_label = tk.Label(self.score_frame, text=f"{self.player2_name}: {self.scores[self.player2_name]} points", fg=self.player2_color, font=("Arial", 14))
        self.player2_label.pack(side="right", padx=20)

    def update_scoreboard(self):
        self.score_label.config(text=f"Round {self.current_round} of {self.num_rounds}")
        self.player1_label.config(text=f"{self.player1_name}: {self.scores[self.player1_name]} points")
        self.player2_label.config(text=f"{self.player2_name}: {self.scores[self.player2_name]} points")

    def setup_board(self):
        self.draw_movement_lines()

    def draw_movement_lines(self):
        self.canvas.create_line(50, 50, 50, 250, fill="green", dash=(4, 2))
        self.canvas.create_line(150, 50, 150, 250, fill="green", dash=(4, 2))
        self.canvas.create_line(250, 50, 250, 250, fill="green", dash=(4, 2))
        self.canvas.create_line(50, 50, 250, 50, fill="green", dash=(4, 2))
        self.canvas.create_line(50, 150, 250, 150, fill="green", dash=(4, 2))
        self.canvas.create_line(50, 250, 250, 250, fill="green", dash=(4, 2))
        self.canvas.create_line(50, 50, 250, 250, fill="green", dash=(4, 2))
        self.canvas.create_line(50, 250, 250, 50, fill="green", dash=(4, 2))

    def draw_boules(self):
        self.canvas.delete("boule")
        for player in self.positions:
            color = self.player1_color if player == self.player1_name else self.player2_color
            for pos in self.positions[player]:
                x, y = pos[1] * 100 + 50, pos[0] * 100 + 50
                self.canvas.create_oval(x-20, y-20, x+20, y+20, fill=color, outline="black", tags="boule")
    
    def draw_highlight(self):
        self.canvas.delete("highlight")
        for pos in self.positions[self.turn]:
            x, y = pos[1] * 100 + 50, pos[0] * 100 + 50
            self.canvas.create_oval(x-25, y-25, x+25, y+25, outline="white", width=2, tags="highlight")
        if self.selected_boule:
            x, y = self.selected_boule[1] * 100 + 50, self.selected_boule[0] * 100 + 50
            self.canvas.create_oval(x-25, y-25, x+25, y+25, outline="green", width=2, tags="highlight")

    def click_handler(self, event):
        row, col = event.y // 100, event.x // 100
        clicked_pos = (row, col)

        if self.selected_boule is None:
            if clicked_pos in self.positions[self.turn]:
                self.selected_boule = clicked_pos
                self.draw_highlight()
            else:
                messagebox.showerror("Erreur", "Veuillez cliquer sur une boule de votre propre joueur.")
        else:
            if self.is_valid_move(self.selected_boule, clicked_pos) or clicked_pos in self.positions[self.turn]:
                if clicked_pos in self.positions[self.turn]:
                    self.selected_boule = clicked_pos
                    self.draw_highlight()
                else:
                    self.move_boule(self.selected_boule, clicked_pos)
                    if self.check_winner(self.turn):
                        self.scores[self.turn] += 1
                        messagebox.showinfo("Victoire", f"{self.turn} a gagné cette manche!")
                        if self.current_round < self.num_rounds:
                            self.current_round += 1
                            self.reset_board()
                        else:
                            self.end_game()
                    else:
                        self.turn = self.player1_name if self.turn == self.player2_name else self.player2_name
                    self.selected_boule = None
                    self.draw_highlight()
            else:
                messagebox.showerror("Erreur", "Déplacement non valide.")
                self.selected_boule = None
                self.draw_highlight()

    def move_boule(self, from_pos, to_pos):
        player = self.turn
        self.positions[player].remove(from_pos)
        self.positions[player].append(to_pos)
        self.moves_count[player][from_pos] += 1
        self.moves_count[player][to_pos] = self.moves_count[player].pop(from_pos)
        self.draw_boules()

    def is_valid_move(self, from_pos, to_pos):
        # Check if 'to_pos' is on a valid movement line from 'from_pos'
        return to_pos in self.get_valid_moves_from(from_pos)

    def get_valid_moves_from(self, pos):
        valid_moves = set()
        row, col = pos

        # Check vertical movements
        if col == 0 and (row, col + 1) not in self.positions[self.player1_name] and (row, col + 1) not in self.positions[self.player2_name]:
            valid_moves.add((row, col + 1))
        elif col == 1:
            if (row, col - 1) not in self.positions[self.player1_name] and (row, col - 1) not in self.positions[self.player2_name]:
                valid_moves.add((row, col - 1))
            if (row, col + 1) not in self.positions[self.player1_name] and (row, col + 1) not in self.positions[self.player2_name]:
                valid_moves.add((row, col + 1))
        elif col == 2 and (row, col - 1) not in self.positions[self.player1_name] and (row, col - 1) not in self.positions[self.player2_name]:
            valid_moves.add((row, col - 1))

        # Check horizontal movements
        if row == 0 and (row + 1, col) not in self.positions[self.player1_name] and (row + 1, col) not in self.positions[self.player2_name]:
            valid_moves.add((row + 1, col))
        elif row == 1:
            if (row - 1, col) not in self.positions[self.player1_name] and (row - 1, col) not in self.positions[self.player2_name]:
                valid_moves.add((row - 1, col))
            if (row + 1, col) not in self.positions[self.player1_name] and (row + 1, col) not in self.positions[self.player2_name]:
                valid_moves.add((row + 1, col))
        elif row == 2 and (row - 1, col) not in self.positions[self.player1_name] and (row - 1, col) not in self.positions[self.player2_name]:
            valid_moves.add((row - 1, col))

        if row == col:  # top-left to bottom-right diagonal
            if row > 0 and (row - 1, col - 1) not in self.positions[self.player1_name] and (row - 1, col - 1) not in self.positions[self.player2_name]:
                valid_moves.add((row - 1, col - 1))
            if row < 2 and (row + 1, col + 1) not in self.positions[self.player1_name] and (row + 1, col + 1) not in self.positions[self.player2_name]:
                valid_moves.add((row + 1, col + 1))
                
        if row + col == 2:  # bottom-left to top-right diagonal
            if row > 0 and (row - 1, col + 1) not in self.positions[self.player1_name] and (row - 1, col + 1) not in self.positions[self.player2_name]:
                valid_moves.add((row - 1, col + 1))
            if row < 2 and (row + 1, col - 1) not in self.positions[self.player1_name] and (row + 1, col - 1) not in self.positions[self.player2_name]:
                valid_moves.add((row + 1, col - 1))

        return valid_moves

    def check_winner(self, player):
        positions = self.positions[player]

        # Check rows
        for row in range(3):
            if all((row, col) in positions for col in range(3)):
                if all(self.moves_count[player][(row, col)] > 0 for col in range(3)):
                    return True

        # Check columns
        for col in range(3):
            if all((row, col) in positions for row in range(3)):
                if all(self.moves_count[player][(row, col)] > 0 for row in range(3)):
                    return True

        # Check diagonals
        if all((i, i) in positions for i in range(3)):
            if all(self.moves_count[player][(i, i)] > 0 for i in range(3)):
                return True
        if all((i, 2 - i) in positions for i in range(3)):
            if all(self.moves_count[player][(i, 2 - i)] > 0 for i in range(3)):
                return True

    def reset_game(self):
        self.current_round = 1
        self.scores = {self.player1_name: 0, self.player2_name: 0}
        self.reset_board()

    def reset_board(self):
        self.positions = {k: list(v) for k, v in self.original_positions.items()}
        self.moves_count = {player: {pos: 0 for pos in positions} for player, positions in self.positions.items()}
        self.turn = self.player1_name
        self.selected_boule = None
        self.draw_boules()
        self.update_scoreboard()

    def end_game(self):
        winner = max(self.scores, key=self.scores.get)
        messagebox.showinfo("Fin de jeu", f"{winner} a gagné la partie avec {self.scores[winner]} points!")
        self.reset_game()

    def confirm_exit(self):
        if messagebox.askyesno("Confirm Exit", "Are you sure you want to return to the main menu?"):
            self.show_menu()

    def show_menu(self):
        self.game_frame.destroy()
        self.menu_frame()
