import tkinter as tk
from tkinter import messagebox

class Game9x5:
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
        
        self.master.title("Fanorona 9x5")
        
        self.canvas = tk.Canvas(game_frame, width=900, height=600, bg="white")
        self.canvas.pack(pady=20)
        
        self.score_frame = tk.Frame(game_frame)
        self.score_frame.pack(pady=20)
        
        self.setup_scoreboard()
        self.setup_board()
        self.setup_menu()
        
        self.positions = {
            player1_name: [(i, 0) for i in range(9)] + [(i, 1) for i in range(9)],
            player2_name: [(i, 3) for i in range(9)] + [(i, 4) for i in range(9)]
        }
        self.original_positions = {k: list(v) for k, v in self.positions.items()}
        
        self.moves_count = {player1_name: {pos: 0 for pos in self.positions[player1_name]},
                            player2_name: {pos: 0 for pos in self.positions[player2_name]}}

        self.turn = player1_name
        self.selected_boule = None
        self.draw_boules()
        self.draw_highlight()
        
        self.canvas.bind("<Button-1>", self.click_handler)
    
    def setup_menu(self):
        menu = tk.Menu(self.master)
        self.master.config(menu=menu)
        game_menu = tk.Menu(menu)
        menu.add_cascade(label="Jeu", menu=game_menu)
        game_menu.add_command(label="Recommencer la Partie", command=self.reset_game)
        game_menu.add_command(label="Quitter", command=self.quit_game)
        game_menu.add_command(label="Retour au Menu", command=self.show_menu)
    
    def setup_scoreboard(self):
        self.score_label = tk.Label(self.game_frame, text=f"Manche {self.current_round} sur {self.num_rounds}", font=("Arial", 16))
        self.score_label.pack()
        
        self.player1_label = tk.Label(self.game_frame, text=f"{self.player1_name}: {self.scores[self.player1_name]} points", fg=self.player1_color, font=("Arial", 14))
        self.player1_label.pack(side="left", padx=20)
        
        self.player2_label = tk.Label(self.game_frame, text=f"{self.player2_name}: {self.scores[self.player2_name]} points", fg=self.player2_color, font=("Arial", 14))
        self.player2_label.pack(side="right", padx=20)
    
    def update_scoreboard(self):
        self.score_label.config(text=f"Manche {self.current_round} sur {self.num_rounds}")
        self.player1_label.config(text=f"{self.player1_name}: {self.scores[self.player1_name]} points")
        self.player2_label.config(text=f"{self.player2_name}: {self.scores[self.player2_name]} points")
    
    def setup_board(self):
        self.draw_movement_lines()
    
    def draw_movement_lines(self):
        # Drawing grid lines
        for i in range(1, 9):
            self.canvas.create_line(i * 100, 0, i * 100, 500, fill="green", dash=(4, 2))
        for i in range(1, 5):
            self.canvas.create_line(0, i * 100, 900, i * 100, fill="green", dash=(4, 2))
        # Diagonals
        self.canvas.create_line(0, 0, 900, 500, fill="green", dash=(4, 2))
        self.canvas.create_line(0, 500, 900, 0, fill="green", dash=(4, 2))
    
    def draw_boules(self):
        self.canvas.delete("boule")
        for player in self.positions:
            color = self.player1_color if player == self.player1_name else self.player2_color
            for pos in self.positions[player]:
                x, y = pos[1] * 100 + 50, pos[0] * 100 + 50
                self.canvas.create_oval(x-25, y-25, x+25, y+25, fill=color, outline="black", tags="boule")
    
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
        if 0 <= row < 9 and 0 <= col + 1 < 5 and (row, col + 1) not in self.positions[self.player1_name] and (row, col + 1) not in self.positions[self.player2_name]:
            valid_moves.add((row, col + 1))
        if 0 <= row < 9 and 0 <= col - 1 < 5 and (row, col - 1) not in self.positions[self.player1_name] and (row, col - 1) not in self.positions[self.player2_name]:
            valid_moves.add((row, col - 1))
        
        # Check horizontal movements
        if 0 <= row + 1 < 9 and (row + 1, col) not in self.positions[self.player1_name] and (row + 1, col) not in self.positions[self.player2_name]:
            valid_moves.add((row + 1, col))
        if 0 <= row - 1 < 9 and (row - 1, col) not in self.positions[self.player1_name] and (row - 1, col) not in self.positions[self.player2_name]:
            valid_moves.add((row - 1, col))
        
        # Check diagonals
        if row - 1 >= 0 and col - 1 >= 0 and (row - 1, col - 1) not in self.positions[self.player1_name] and (row - 1, col - 1) not in self.positions[self.player2_name]:
            valid_moves.add((row - 1, col - 1))
        if row + 1 < 9 and col + 1 < 5 and (row + 1, col + 1) not in self.positions[self.player1_name] and (row + 1, col + 1) not in self.positions[self.player2_name]:
            valid_moves.add((row + 1, col + 1))
        
        if row - 1 >= 0 and col + 1 < 5 and (row - 1, col + 1) not in self.positions[self.player1_name] and (row - 1, col + 1) not in self.positions[self.player2_name]:
            valid_moves.add((row - 1, col + 1))
        if row + 1 < 9 and col - 1 >= 0 and (row + 1, col - 1) not in self.positions[self.player1_name] and (row + 1, col - 1) not in self.positions[self.player2_name]:
            valid_moves.add((row + 1, col - 1))
        
        return valid_moves
    
    def check_winner(self, player):
        positions = self.positions[player]

        # Check rows
        for row in range(9):
            if all((row, col) in positions for col in range(5)):
                if all(self.moves_count[player][(row, col)] > 0 for col in range(5)):
                    return True

        # Check columns
        for col in range(5):
            if all((row, col) in positions for row in range(9)):
                if all(self.moves_count[player][(row, col)] > 0 for row in range(9)):
                    return True

        # Check diagonals
        if all((i, i) in positions for i in range(min(9, 5))):
            if all(self.moves_count[player][(i, i)] > 0 for i in range(min(9, 5))):
                return True
        if all((i, 4 - i) in positions for i in range(min(9, 5))):
            if all(self.moves_count[player][(i, 4 - i)] > 0 for i in range(min(9, 5))):
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
    
    def quit_game(self):
        self.master.quit()
    
    def show_menu(self):
        self.game_frame.pack_forget()
        self.menu_frame.pack()
